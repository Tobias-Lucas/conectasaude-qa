# Casos de teste

Os candidatos são os mesmos da atividade da Aula Nacional 3, "Os 5 testes antes
do go-live". Lá a turma escolhe 5 para executar em 2 horas de homologação, e
justifica a escolha. Aqui estão todos, porque a esteira não tem janela de duas
horas: ela roda a cada commit.

> A escolha dos 5 e a justificativa são a atividade. Este arquivo lista os
> casos e o que cada um espera, que é o que o enunciado já entrega ao aluno.
> A técnica de cada caso e a leitura de risco ficam com o professor.

## Os candidatos do RF-12

| ID | Cenário | Esperado | Onde roda |
|---|---|---|---|
| C-01 | Agendar para hoje (27/10/2026), 14:00, vaga livre | 201 + JSON + lembrete pendente | API |
| C-02 | Agendar para ontem (26/10/2026) | 422 · data retroativa | API |
| C-03 | Agendar para 30/11/2026, 10:00 | 201 + JSON | API |
| C-04 | Agendar para 15/12/2026, 10:00 | 201 + JSON | API |
| C-05 | Data 31/06/2027 | 422 · data inválida | API |
| C-06 | Data no formato 2026-10-30 | 422 · formato inválido | API |
| C-07 | Data vazia | 422 · campo obrigatório | API |
| C-08 | Horário 07:15 | 422 · fora do passo de 30 min | API |
| C-09 | Horário 19:30 | 422 · fora do expediente | API |
| C-10 | Duas recepcionistas confirmam o mesmo horário com o mesmo profissional | um 201 e um 409 | API (C-10a e C-10b) |
| C-11 | WhatsApp responde 429 no envio do lembrete | SMS enviado | API |
| C-12 | Texto do lembrete que chega ao paciente | não contém especialidade médica | API |
| C-13 | Cor e alinhamento do botão "Agendar" | conforme o protótipo | **não automatizado** |

**C-13 não está automatizado.** O botão não faz parte do RF-12, e o critério da
Aula 4 para automatizar é estável, repetitivo, determinístico e caro se falhar.
Esse caso não passa no "determinístico".

## A contagem

A suíte roda **14 requisições, 13 delas com teste, e 14 asserts**. A requisição
sem teste é o `setup`, que zera a agenda para a execução não depender de ordem.
São 14 asserts porque o C-01 verifica duas coisas (o status e o corpo) e o C-10
é dividido em duas requisições.

É o mesmo número que aparece no terminal do slide 8 da Aula 4:
`14 passed · 0 failed`.

## Os dois defeitos da v0.9

A atividade da Aula 3 registra que, na build v0.9, **C-01 e C-05 falharam**:
hoje foi recusado como retroativo, e 31/06 foi aceito. A v1.0 disse que corrigiu
os dois, e ninguém retestou. Essa era a aposta da turma.

Aqui dá para ver os dois defeitos de novo:

```bash
BUILD=v0.9 SENHA_TESTE="$SENHA_TESTE" python3 app/servidor.py
```

Rodando a suíte contra ela saem três falhas, as duas do C-01 e a do C-05:

```
expected response to have status code 201 but got 422
expected undefined to deeply equal '27/10/2026'
expected response to have status code 422 but got 201
```

As duas primeiras são, palavra por palavra, o vermelho que está no slide do
Postman da Aula 3.

## Os testes de tela

Três, e é de propósito: é o topo da pirâmide.

| Teste | O que verifica |
|---|---|
| `LoginTest.loginComSucesso` | a Dra. Mariana entra e vê "Bem-vinda, Dra. Mariana" |
| `LoginTest.senhaErradaNaoEntra` | senha errada não abre a agenda |
| `AgendaProtegidaTest.semSessaoNaoAbreAgenda` | `/agenda` sem sessão pede login |

## Numeração: um aviso

Os slides usam dois prefixos para os mesmos casos. A atividade da Aula 3 numera
**C-01 a C-13**, e é a numeração completa, então é a que este repositório segue.
Os slides mostram **CT-07** para o caso "agendar para hoje" (que na atividade é
o C-01) e **CT-01, CT-02 e CT-11** no terminal do Newman da Aula 4. Vale
unificar nas próximas aulas.
