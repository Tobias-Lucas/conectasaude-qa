package com.conectasaude;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.WebDriverWait;

import static java.time.Duration.ofSeconds;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.openqa.selenium.support.ui.ExpectedConditions.visibilityOfElementLocated;

/**
 * O login da Dra. Mariana, slide 12 da Aula Nacional 4.
 *
 * A receita e sempre a mesma: abrir, encontrar, agir, verificar.
 *
 * Este arquivo mantem as linhas do slide na mesma ordem. O que foi preciso
 * acrescentar para rodar de verdade esta em docs/diferencas-dos-slides.md.
 */
class LoginTest {

    private WebDriver driver;

    /** Onde a ConectaSaude de laboratorio esta rodando. */
    private static final String BASE_URL =
            System.getProperty("baseUrl", "http://127.0.0.1:8800");

    @BeforeEach
    void abrirNavegador() {
        ChromeOptions opcoes = new ChromeOptions();
        if (Boolean.parseBoolean(System.getProperty("headless", "false"))) {
            // Na esteira nao ha tela. Chrome sem janela.
            opcoes.addArguments("--headless=new", "--no-sandbox",
                    "--disable-dev-shm-usage", "--window-size=1280,900");
        }
        driver = new ChromeDriver(opcoes);
    }

    @AfterEach
    void fecharNavegador() {
        if (driver != null) {
            driver.quit();
        }
    }

    @Test
    @DisplayName("A Dra. Mariana entra e ve a mensagem de boas-vindas")
    void loginComSucesso() {
        driver.get(BASE_URL + "/login");

        WebDriverWait wait = new WebDriverWait(driver, ofSeconds(10));
        wait.until(visibilityOfElementLocated(
                By.cssSelector("[data-testid=email]")))
                .sendKeys("mariana@conectasaude.test");
        driver.findElement(By.cssSelector("[data-testid=senha]"))
                .sendKeys(senhaDoAmbiente()); // secret da esteira
        driver.findElement(By.cssSelector("[data-testid=entrar]")).click();

        String msg = wait.until(visibilityOfElementLocated(
                By.cssSelector("[data-testid=boas-vindas]"))).getText();
        assertEquals("Bem-vinda, Dra. Mariana", msg);
    }

    @Test
    @DisplayName("Senha errada nao abre a agenda")
    void senhaErradaNaoEntra() {
        driver.get(BASE_URL + "/login");

        WebDriverWait wait = new WebDriverWait(driver, ofSeconds(10));
        wait.until(visibilityOfElementLocated(
                By.cssSelector("[data-testid=email]")))
                .sendKeys("mariana@conectasaude.test");
        driver.findElement(By.cssSelector("[data-testid=senha]"))
                .sendKeys("nao-e-essa");
        driver.findElement(By.cssSelector("[data-testid=entrar]")).click();

        String erro = wait.until(visibilityOfElementLocated(
                By.cssSelector("[data-testid=erro]"))).getText();
        assertEquals("Usuário ou senha inválidos.", erro);
    }

    /**
     * A senha nao mora no codigo. Vem do ambiente na sua maquina e de um
     * secret do repositorio na esteira. Se estiver vazia, o teste para aqui
     * dizendo o que falta, em vez de passar por engano.
     */
    private static String senhaDoAmbiente() {
        String senha = System.getenv("SENHA_TESTE");
        if (senha == null || senha.isEmpty()) {
            throw new IllegalStateException(
                    "SENHA_TESTE esta vazia. Na sua maquina: export SENHA_TESTE='...'. "
                  + "No GitHub: Settings > Secrets and variables > Actions > "
                  + "New repository secret, com o nome SENHA_TESTE.");
        }
        return senha;
    }
}
