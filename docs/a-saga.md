# A saga da ConectaSaúde, em quatro aulas

Este repositório é o último capítulo. Ele só faz sentido se você souber como
chegamos aqui.

## Aula 1 · Do problema ao requisito

Mariana (médica), Jorge (DPO) e Cleusa (recepção) querem coisas diferentes do
mesmo sistema. A ata da reunião tem frases como "o sistema deve ser rápido".
A turma transforma isso em requisito verificável: o "rápido" vira **p95 abaixo
de 2 segundos com 200 usuários concorrentes**.

A lição: requisito sem número não dá para testar.

## Aula 2 · Qualidade não começa no teste

Trinta dias depois, o comitê de release olha a primeira versão. Ela funciona na
demo. A pergunta passa a ser outra: funciona, mas tem qualidade? Aparecem o
scan, a dívida técnica e a frase que atravessa o resto da série:

> a ponte só abre quando existe evidência.

O DPO registra o veto: nenhuma mensagem ao paciente pode citar especialidade
médica.

## Aula 3 · Do requisito ao teste

O QA saiu da empresa. A turma assume a cadeira. O RF-12 chega para teste na
véspera do go-live, com duas horas de homologação e 13 casos candidatos. Cabem
cinco. Os outros ficam declarados como risco aberto.

A build v0.9 falhou em dois casos (hoje recusado como retroativo, 31/06 aceito).
A v1.0 diz que corrigiu, e ninguém retestou. A turma decide **NO-GO do pacote e
GO-condicional com dono e prazo**.

É o vermelho desta aula que você consegue reproduzir aqui:

```bash
BUILD=v0.9 SENHA_TESTE="$SENHA_TESTE" python3 app/servidor.py
```

## Aula 4 · QA na era da IA

O go-live da Rede Vitalle está a um dia. São 87 clínicas, SLA de 99,5% e multa
de 20%. O CTO pergunta quem vai rodar os 500 testes de novo, toda semana.

A resposta é a esteira: Newman para a regra de negócio, Selenium para o fluxo da
tela, e uma pipeline que dispara a cada commit e guarda a evidência, verde ou
vermelha. A IA escreve o script; quem responde por ele continua sendo gente.

É o que está em `.github/workflows/regressao.yml`.

## O fio

Em quatro aulas a evidência mudou de estado quatro vezes: não existia, virou
critério de decisão, passou a ser fabricada com técnica, e agora é fabricada
sozinha. O que não mudou foi quem assina.

---

A ConectaSaúde, a Rede Vitalle, os personagens e os números são ficção, criados
para a disciplina. O método é o que o mercado usa.
