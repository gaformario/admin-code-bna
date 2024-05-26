import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def test_landing_page(driver):
    url = "http://localhost:3000"
    driver.get(url)

    try:
        # Espera até que o elemento da página de landing esteja visível
        landing_page_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))  # Substitua por um seletor específico da sua página
        )
        print("Página de landing carregada com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar a página de landing: {e}")
    finally:
        time.sleep(2)  # Aguarda 2 segundos para visualização

def test_listar_obras_page(driver):
    url = "http://localhost:3000/obra/listarObras"
    driver.get(url)

    try:
        # Espera até que o elemento da página /listarObras esteja visível
        listar_obras_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))  # Substitua por um seletor específico da sua página
        )
        print("Página /listarObras carregada com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar a página /listarObras: {e}")
    finally:
        time.sleep(2)  # Aguarda 2 segundos para visualização

def test_filter_functionality(driver):
    url = "http://localhost:3000/obra/listarObras"
    driver.get(url)

    try:
        # Espera até que o campo de filtro esteja visível
        filter_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.form-control.form-control-sm.input-sm.upper'))
        )

        # Escreve um texto no campo de filtro
        filter_text = "Guerra Civil"
        filter_input.send_keys(filter_text)

        # Aguarda um momento para permitir que a tabela seja atualizada
        time.sleep(2)  # Ajuste conforme necessário

        # Verifica se a tabela reflete o filtro
        # Substitua '#tabela' pelo ID ou classe do elemento da tabela, se diferente
        table = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "tabela"))
        )

        # Verifica se as linhas da tabela contêm o texto filtrado
        table_rows = table.find_elements(By.CSS_SELECTOR, "tr")
        for row in table_rows:
            if filter_text.lower() in row.text.lower():
                print(f"Linha encontrada com o texto '{filter_text}': {row.text}")

        print("Teste de filtro concluído.")
    except Exception as e:
        print(f"Erro ao testar o filtro: {e}")
    finally:
        time.sleep(2)  # Aguarda 2 segundos para visualização

def test_info_button(driver):
    url = "http://localhost:3000/obra/listarObras"
    driver.get(url)

    try:
        # Espera até que a tabela esteja visível
        table = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "tabela"))
        )

        # Encontra e clica no botão "+ Info"
        info_button = table.find_element(By.CSS_SELECTOR, 'a.btn.btn-outline-warning')
        ActionChains(driver).move_to_element(info_button).click(info_button).perform()

        # Aguarda um novo guia/janela ser aberta
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

        # Alterna para a nova guia/janela
        driver.switch_to.window(driver.window_handles[1])

        # Verifica se a nova página foi carregada corretamente
        new_page_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))
        )
        print("Nova página aberta com sucesso.")
    except Exception as e:
        print(f"Erro ao abrir a nova página: {e}")
    finally:
        time.sleep(2)  # Aguarda 2 segundos para visualização

if __name__ == "__main__":
    # Configura o WebDriver do Chrome
    driver = webdriver.Edge()

    try:
        #test_landing_page(driver)
        #test_listar_obras_page(driver)
        #test_filter_functionality(driver)
        test_info_button(driver)
    finally:
        driver.quit()
