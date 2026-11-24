# Veredito · o go-live abre amanhã?

> Preencha este arquivo no seu fork, faça commit e deixe no repositório. É a
> peça de portfólio: não a suíte verde, mas a decisão que você assina em cima
> dela.

**Quem assina:**
**Data:**
**Build avaliada:** (v1.2 ou v0.9)
**Run do Actions:** (link para a execução que você está usando como evidência)

---

## 1 · A decisão

Marque uma:

- [ ] **GO** · sobe amanhã
- [ ] **GO-condicional** · sobe com condição, dono e prazo
- [ ] **NO-GO** · não sobe

## 2 · A evidência

Que número você está usando, e de onde ele veio?

| O que verifiquei | Resultado | Onde está a prova |
|---|---|---|
| Suíte de API (15 asserts) | | artefato `evidencias/newman.xml` do run |
| Testes de tela (3) | | `testes-tela/target/surefire-reports/` |
| | | |

## 3 · O que ficou sem evidência

Verde não absolve buraco. O que esta suíte **não** verifica, e qual o risco de
subir assim mesmo?

- C-13 (cor e alinhamento do botão): avaliação visual, fora do RF-12.
-
-

## 4 · Se foi GO-condicional

| Condição | Dono | Prazo |
|---|---|---|
| | | |

## 5 · A frase

Escreva em uma linha o que você diria numa entrevista sobre esta decisão.
A da Aula 4 era assim:

> "Decidi um go-live com 232 testes automatizados e declarei o que não tinha evidência."

A sua:

>

---

## C-11b — fallback para contato manual

O caso **C-11** verifica a queda do WhatsApp para SMS. Para completar o fluxo
previsto no RF-12, foi acrescentada a simulação em que os dois canais falham.

- Simulação: `?simular=whatsapp_429,sms_503`.
- Resultado esperado: HTTP 201, com `lembrete.canal = manual` e
  `lembrete.estado = pendente`.
- O cenário foi incluído na collection do Postman e a suíte passa a ter 15
  asserts. O resultado da nova execução deve ser registrado na tabela de
  evidências acima antes da decisão final.
