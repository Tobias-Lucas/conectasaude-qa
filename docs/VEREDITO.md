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
| Suíte de API (14 asserts) | | artefato `evidencias/newman.xml` do run |
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

## Sua parte: o teste que falta

O caso **C-11** cobre o WhatsApp caindo para SMS. O RF-12 pede mais um passo:
**se o SMS também falhar, o lembrete entra na fila de contato manual.** Esse
caminho não tem teste e nem existe no servidor de laboratório.

Faça você:

1. Em `app/regras.py`, deixe o SMS poder falhar (um segundo stub, parecido com
   o `?simular=whatsapp_429`), e registre o lembrete como `manual`.
2. Em `testes-api/conectasaude.postman_collection.json`, escreva o **C-11b**:
   WhatsApp 429 e SMS indisponível, o lembrete tem que terminar em `manual`.
3. Rode a suíte. Ela passa de 14 para 15 asserts.
4. Commit, e o seu fork deixa de ser cópia.
