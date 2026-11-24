# O que mudou do slide para o código

Os slides mostram o trecho que ensina. Este repositório mostra o trecho que
roda. Tudo o que foi preciso acrescentar está listado aqui, para ninguém achar
que o slide estava errado nem que o código é outro assunto.

## O sistema sob teste não existia

Nos slides, a ConectaSaúde é o case. Selenium precisa de uma tela e Newman
precisa de uma API, então este repositório traz uma ConectaSaúde de laboratório
em `app/`: só biblioteca padrão do Python, nada para instalar. Ela implementa o
RF-12 e duas telas, e mais nada.

É uma fatia. Os 500 testes da regressão e os 232 verdes do go-live são da
ficção da aula. Aqui são 14 asserts de API e 3 testes de tela.

## `app.conectasaude.test` não resolve

O slide 12 abre `https://app.conectasaude.test/login`. Esse domínio não existe,
e `.test` é reservado justamente para isso. O teste usa `baseUrl`, que aponta
para `http://127.0.0.1:8800` por padrão:

```java
private static final String BASE_URL = System.getProperty("baseUrl", "http://127.0.0.1:8800");
```

As linhas seguintes do slide, do `WebDriverWait` ao `assertEquals`, estão na
mesma ordem. A única mudança nelas é a senha: no slide,
`System.getenv("SENHA_TESTE")` vai direto para o `sendKeys`; aqui passa por um
método que explica o que fazer quando a variável está vazia.

## `new ChromeDriver()` não sabe o que é `-Dheadless`

O slide 10 roda `mvn -B test -Dheadless=true`, e o slide 12 abre o navegador com
`new ChromeDriver()`. As duas coisas não se conversam sozinhas: a flag precisa
virar `ChromeOptions`.

```java
ChromeOptions opcoes = new ChromeOptions();
if (Boolean.parseBoolean(System.getProperty("headless", "false"))) {
    opcoes.addArguments("--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1280,900");
}
driver = new ChromeDriver(opcoes);
```

Também não há `driver.quit()` solto no fim do método: ele está no `@AfterEach`,
para fechar o navegador mesmo quando o teste falha. Navegador que fica aberto
depois do vermelho é vazamento de recurso, e na esteira vira runner travado.

## A pipeline do slide não sobe o servidor

O YAML do slide 10 vai direto ao `newman run`. Falta o passo que coloca a
aplicação no ar e espera ela responder, senão a suíte bate numa porta fechada.
O `.github/workflows/regressao.yml` tem esse passo, mais um que verifica se o
secret existe antes de tudo. Também foi acrescentado `workflow_dispatch`, porque
num fork novo o Actions precisa de um disparo manual na primeira vez.

## A condição de corrida roda em sequência

O C-10 é descrito como duas recepcionistas confirmando ao mesmo tempo. Corrida
de verdade não é determinística, e teste que às vezes passa é pior que teste que
não existe (é a "oscilação" do slide 14). Aqui o C-10 vira duas requisições em
sequência para a mesma vaga: a primeira pega o 201, a segunda tem que bater no
409. Verifica a regra R3, que é o que importa, e não pisca.

## O 429 do WhatsApp é um stub

Não há API de WhatsApp aqui. O C-11 pede o fallback com
`POST /agendamento?simular=whatsapp_429`. É superfície só de teste, e está
documentada de propósito: esconder um stub é pior que assumir um.

## A data é fixa

`HOJE` vale `27/10/2026`, o dia da Aula 3, e vem do ambiente. Sem isso, o C-01
("agendar para hoje") e o C-02 ("agendar para ontem") mudariam de resultado a
cada dia, e ainda poderiam divergir entre o fuso do aluno e o UTC do runner.

## O que mais foi acrescentado

Coisas pequenas, listadas para a lista ser mesmo completa:

- **Mais testes de tela que o slide.** O slide mostra um. Aqui são três: o login
  feliz, a senha errada e o acesso a `/agenda` sem sessão.
- **`actions/setup-python@v5`** no YAML, que o slide não tem, porque o servidor
  de laboratório é Python.
- **`pull_request` e `workflow_dispatch`** além do `on: push` do slide.
- **O caminho do artefato** não é `newman/`, como no slide, e sim
  `evidencias/newman.xml` mais `testes-tela/target/surefire-reports/` e o
  `servidor.log`. O slide guardava só a pasta do Newman.
- **Um passo que confere o secret** antes de qualquer coisa, para a pipeline
  falhar dizendo o que falta em vez de falhar no meio.

## A senha

O slide já mostra `System.getenv("SENHA_TESTE")`. O que foi acrescentado é o que
acontece quando a variável está vazia: o servidor se recusa a subir e o teste
para com uma mensagem dizendo onde criar o secret. Sem isso, os dois lados
comparariam string vazia com string vazia, o login passaria, e a lição do slide
sumiria no silêncio.
