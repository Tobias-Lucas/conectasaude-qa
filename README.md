# ConectaSaúde · QA do requisito à esteira

A última aula do Notável Mestre termina com uma frase para você dizer numa
entrevista:

> "Decidi um go-live com testes automatizados e declarei o que não tinha evidência."

Este repositório existe para que a frase tenha onde apontar. É a ConectaSaúde
das quatro aulas, pequena o suficiente para caber na cabeça e completa o
suficiente para rodar: o requisito RF-12, a suíte de API, os testes de tela e
a pipeline que dispara a cada commit.

**Disciplina:** Engenharia de Requisitos, Teste e Qualidade de Software ·
Notável Mestre · ADS · Grupo Ser Educacional.

> A ConectaSaúde, a Rede Vitalle, os personagens e os números são ficção,
> criados para a disciplina. O método é o que o mercado usa.

## Rodar em dois minutos

Você precisa de Python 3.8+ e Node 18+. Para os testes de tela, também do
**JDK** 21 (não basta o JRE: Maven precisa do `javac`), do **Maven** 3.9+ e do
Chrome instalado.

```bash
# Ubuntu/Debian, se faltar algum
sudo apt install openjdk-21-jdk maven
```

```bash
# 1. a senha não mora no código
export SENHA_TESTE='a-que-voce-escolher'

# 2. sobe a ConectaSaúde de laboratório
python3 app/servidor.py
```

Em outro terminal:

```bash
# 3. a regra de negócio, 14 asserts
npx newman@6 run testes-api/conectasaude.postman_collection.json \
  -e testes-api/homologacao.postman_environment.json

# 4. o fluxo da tela, 3 testes
cd testes-tela && mvn -B test
```

O terminal do Newman termina assim, que é o mesmo número do slide da Aula 4:

```
assertions   14   0 failed
```

## Ver o vermelho da Aula 3

A build v0.9 tinha dois defeitos: recusava o dia de hoje como retroativo e
aceitava 31/06. Suba o servidor com ela:

```bash
BUILD=v0.9 SENHA_TESTE="$SENHA_TESTE" python3 app/servidor.py
```

Rode a suíte de novo e três asserts caem. Dois deles, palavra por palavra, são
o vermelho que está no slide do Postman:

```
expected response to have status code 201 but got 422
expected undefined to deeply equal '27/10/2026'
```

Esse é o ponto da série inteira. O esperado foi escrito antes do clique, então
o vermelho não é opinião: é evidência.

## O que tem aqui

```
app/                    a ConectaSaúde de laboratório (só stdlib do Python)
  regras.py             o RF-12: R1 a R5 e o veto do DPO
  servidor.py           a API e duas telas
testes-api/             a collection do Postman, executável pelo Newman
testes-tela/            Selenium WebDriver em Java, com Maven
.github/workflows/      a pipeline que roda tudo a cada commit
docs/
  RF-12.md              o requisito, e o que ele não responde
  casos-de-teste.md     C-01 a C-13, a técnica de cada um e por que C-13 fica manual
  a-saga.md             as quatro aulas em uma página
  diferencas-dos-slides.md   tudo que foi preciso acrescentar para o slide rodar
  VEREDITO.md           o template que você preenche e assina
```

## Fazer deste repositório o seu

1. **Fork.** Botão no canto superior direito.
2. **Ligue o Actions.** Em fork novo o GitHub pede uma confirmação na aba
   Actions antes de rodar qualquer coisa.
3. **Crie o secret.** Settings > Secrets and variables > Actions > New
   repository secret, com o nome `SENHA_TESTE` e o valor que você quiser. Sem
   ele a pipeline para no primeiro passo e diz o que falta. É de propósito: a
   senha da Dra. Mariana não pode estar no código, e você precisa sentir isso
   uma vez.
4. **Rode a pipeline.** Aba Actions > regressao-conectasaude > Run workflow.
5. **Escreva o teste que falta.** Está em `docs/VEREDITO.md`, no fim: o caminho
   do SMS que também falha. São 15 asserts quando você terminar.
6. **Assine o veredito.** Preencha `docs/VEREDITO.md` e faça commit.

O passo 5 é o que separa um fork de um portfólio.

## A pirâmide, na prática

Os números deste repositório mostram o formato que o slide desenha: muita
verificação barata embaixo, pouca verificação cara em cima.

| Camada | Quantos | Quanto custa |
|---|---|---|
| API (Newman) | 14 asserts | milissegundos, roda em qualquer lugar |
| Tela (Selenium) | 3 testes | segundos, precisa de navegador |
| Visual (C-13) | 0 | fica com o humano, de propósito |

## Licença

MIT. Use em aula, use no seu portfólio, adapte para a sua turma.
