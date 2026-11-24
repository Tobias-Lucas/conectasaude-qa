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
 * Quem nao fez login nao ve agenda de paciente.
 *
 * Segundo e ultimo teste de tela. O topo da piramide tem poucos testes de
 * proposito: sao os mais caros de manter e os mais lentos de rodar.
 */
class AgendaProtegidaTest {

    private WebDriver driver;

    private static final String BASE_URL =
            System.getProperty("baseUrl", "http://127.0.0.1:8800");

    @BeforeEach
    void abrirNavegador() {
        ChromeOptions opcoes = new ChromeOptions();
        if (Boolean.parseBoolean(System.getProperty("headless", "false"))) {
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
    @DisplayName("Abrir /agenda sem sessao devolve o pedido de login")
    void semSessaoNaoAbreAgenda() {
        driver.get(BASE_URL + "/agenda");

        WebDriverWait wait = new WebDriverWait(driver, ofSeconds(10));
        String aviso = wait.until(visibilityOfElementLocated(
                By.cssSelector("[data-testid=erro]"))).getText();
        assertEquals("Faça login para ver a agenda.", aviso);
    }
}
