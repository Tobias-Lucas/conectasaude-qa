# -*- coding: utf-8 -*-
"""RF-12 - POST /agendamento, da Aula Nacional 3.

Só biblioteca padrão. Este arquivo é o sistema sob teste: as regras R1 a R5
e o veto do DPO, escritas do jeito mais direto possível, para dar para ler.

R1  data_agendamento: formato DD/MM/AAAA, obrigatório. Não aceita data retroativa.
R2  Horários das 07:00 às 19:00, em passos de 30 minutos.
R3  Não permite dois agendamentos no mesmo horário com o mesmo profissional.
R4  Ao confirmar, agenda o lembrete: WhatsApp 24h antes. Se falhar, SMS.
    Se o SMS falhar, registra para contato manual.
R5  Sucesso: 201 + JSON. Erro de validação: 422 + motivo. Conflito: 409.

Veto registrado (Jorge, DPO): nenhuma mensagem ao paciente pode conter
especialidade médica.
"""

import calendar
import datetime
import os
import uuid

# A build que está rodando. v1.2 é a corrigida; v0.9 traz de volta os dois
# defeitos que a turma encontrou na Aula 3.
BUILD = os.environ.get("BUILD", "v1.2")

# O "hoje" do caso. Fixo por padrão para o teste não apodrecer com o calendário
# nem mudar de resultado entre o fuso do aluno e o do runner.
HOJE = os.environ.get("HOJE", "27/10/2026")

HORA_ABRE = datetime.time(7, 0)
HORA_FECHA = datetime.time(19, 0)

ESPECIALIDADES = (
    "cardiologia", "cardiologista", "dermatologia", "dermatologista",
    "psiquiatria", "psiquiatra", "oncologia", "oncologista",
    "ginecologia", "ginecologista", "ortopedia", "ortopedista",
)

# agenda[(profissional_id, data, horario)] = agendamento_id
agenda = {}
# tudo o que foi agendado, por id
agendamentos = {}


def _hoje():
    return datetime.datetime.strptime(HOJE, "%d/%m/%Y").date()


class Recusado(Exception):
    """Pedido recusado. status é 422 (validação) ou 409 (conflito)."""

    def __init__(self, status, motivo):
        super().__init__(motivo)
        self.status = status
        self.motivo = motivo


def _data(valor):
    """R1: formato DD/MM/AAAA, obrigatório, não retroativa."""
    if valor is None or str(valor).strip() == "":
        raise Recusado(422, "data_agendamento é obrigatório")
    texto = str(valor)
    try:
        data = datetime.datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError:
        # Cai aqui tanto o formato errado (2026-10-30) quanto a data que não
        # existe no calendário (31/06/2027).
        partes = texto.split("/")
        parece_formato_certo = (
            len(partes) == 3
            and len(partes[0]) == 2 and len(partes[1]) == 2 and len(partes[2]) == 4
            and all(p.isdigit() for p in partes)
        )
        if not parece_formato_certo:
            raise Recusado(422, "data_agendamento fora do formato DD/MM/AAAA")
        if BUILD == "v0.9":
            # Defeito C-05 da v0.9: em vez de recusar o dia que não existe, a
            # rotina "conserta" para o último dia do mês e segue em frente.
            dia, mes, ano = (int(p) for p in partes)
            try:
                ultimo = calendar.monthrange(ano, mes)[1]
            except calendar.IllegalMonthError:
                raise Recusado(422, "data_agendamento inválida: esta data não existe")
            data = datetime.date(ano, mes, min(dia, ultimo))
        else:
            raise Recusado(422, "data_agendamento inválida: esta data não existe")

    if BUILD == "v0.9":
        # Defeito C-01 da v0.9: a comparação usa > em vez de >=, então o próprio
        # dia de hoje é tratado como retroativo.
        if data <= _hoje():
            raise Recusado(422, "data_agendamento retroativa")
    else:
        if data < _hoje():
            raise Recusado(422, "data_agendamento retroativa")
    return data


def _horario(valor):
    """R2: das 07:00 às 19:00, em passos de 30 minutos."""
    if valor is None or str(valor).strip() == "":
        raise Recusado(422, "horario é obrigatório")
    try:
        hora = datetime.datetime.strptime(str(valor), "%H:%M").time()
    except ValueError:
        raise Recusado(422, "horario fora do formato HH:MM")
    if hora < HORA_ABRE or hora > HORA_FECHA:
        raise Recusado(422, "horario fora do expediente (07:00 às 19:00)")
    if hora.minute not in (0, 30):
        raise Recusado(422, "horario fora do passo de 30 minutos")
    return hora


def _lembrete(data, horario, profissional_id, especialidade, canal_whatsapp_ok):
    """R4 e o veto do DPO: o texto que chega ao paciente."""
    quando = datetime.datetime.combine(data, horario) - datetime.timedelta(hours=24)
    texto = "Lembrete: você tem consulta amanhã, às %s, na ConectaSaúde." % horario.strftime("%H:%M")

    if canal_whatsapp_ok:
        canal, estado = "whatsapp", "pendente"
    else:
        # WhatsApp respondeu 429. Cai para SMS. Se o SMS também falhar,
        # entra na fila de contato manual.
        canal, estado = "sms", "pendente"

    lembrete = {
        "canal": canal,
        "estado": estado,
        "enviar_em": quando.strftime("%d/%m/%Y %H:%M"),
        "texto": texto,
        "profissional_id": profissional_id,
    }
    # O veto do DPO é verificado aqui, no último ponto antes de o texto sair.
    for palavra in ESPECIALIDADES:
        if palavra in texto.lower():
            raise Recusado(422, "o texto do lembrete não pode conter especialidade médica")
    if especialidade and especialidade.lower() in texto.lower():
        raise Recusado(422, "o texto do lembrete não pode conter especialidade médica")
    return lembrete


def agendar(pedido, whatsapp_ok=True):
    """Recebe o corpo do POST /agendamento e devolve (status, corpo)."""
    data = _data(pedido.get("data_agendamento"))
    horario = _horario(pedido.get("horario"))

    paciente_id = str(pedido.get("paciente_id") or "").strip()
    profissional_id = str(pedido.get("profissional_id") or "").strip()
    if not paciente_id:
        raise Recusado(422, "paciente_id é obrigatório")
    if not profissional_id:
        raise Recusado(422, "profissional_id é obrigatório")

    # R3: a mesma vaga não vai para dois pacientes.
    chave = (profissional_id, data.isoformat(), horario.strftime("%H:%M"))
    if chave in agenda:
        raise Recusado(409, "já existe agendamento para este profissional neste horário")

    lembrete = _lembrete(
        data, horario, profissional_id,
        pedido.get("especialidade"), whatsapp_ok,
    )

    novo = {
        "id": "AG-" + uuid.uuid4().hex[:8].upper(),
        "data_agendamento": data.strftime("%d/%m/%Y"),
        "horario": horario.strftime("%H:%M"),
        "paciente_id": paciente_id,
        "profissional_id": profissional_id,
        "estado": "confirmado",
        "lembrete": lembrete,
        "build": BUILD,
    }
    agenda[chave] = novo["id"]
    agendamentos[novo["id"]] = novo
    return 201, novo


def zerar():
    """Limpa a agenda. O teste chama isto para não depender de ordem."""
    agenda.clear()
    agendamentos.clear()
