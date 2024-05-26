import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def test_analysis_page(driver):
    url = "http://localhost:3000"
    driver.get(url)

    try:
        # Espera até que o elemento da página de landing esteja visível
        landing_page_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))  # Substitua por um seletor específico da sua página
        )
        print("Página de análises carregada com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar a página de análises: {e}")
    finally:
        time.sleep(2)  # Aguarda 2 segundos para visualização
        
def test_admin(driver):
    url = "http://localhost:3000"
    driver.get(url)

    try:
        # Espera até que o ícone de administração esteja visível
        admin_icon = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.nav-link[href="https://github.com/gaformario/admin-code-bna"]'))
        )

        # Clica no ícone de administração
        admin_icon.click()

        print("Administrador com acesso aos códigos de raspagem e modelagem do BD.")
    except Exception as e:
        print(f"Erro ao clicar no ícone de administração: {e}")
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

def test_favorite_functionality(driver):
    url = "http://localhost:3000/obra/listarObras"
    driver.get(url)

    try:
        # Espera até que a tabela esteja visível
        table = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "tabela"))
        )

        # Encontra a linha da obra "Guerra Civil"
        obra_linha = None
        table_rows = table.find_elements(By.CSS_SELECTOR, "tr")
        for row in table_rows:
            if 'Guerra Civil' in row.text:
                obra_linha = row
                break

        assert obra_linha is not None, "A obra 'Guerra Civil' não foi encontrada na tabela"

        # Encontra e clica no botão de favoritar na linha da obra "Guerra Civil"
        favorite_button = obra_linha.find_element(By.CSS_SELECTOR, 'button.btn.btn-outline-secondary, button.btn.btn-danger')
        ActionChains(driver).move_to_element(favorite_button).click(favorite_button).perform()

        # Aguarda um momento para garantir que a ação foi processada
        time.sleep(2)

        # Navega para a página de favoritos
        driver.get('http://localhost:3000/obra/meusFavoritos')

        # Espera até que a lista de favoritos seja carregada
        favorites_table = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "tabela"))
        )

        # Verifica se a obra "Guerra Civil" está na lista de favoritos
        obras_favoritadas = favorites_table.find_elements(By.CSS_SELECTOR, 'tr')
        obra_encontrada = False
        for obra in obras_favoritadas:
            if 'Guerra Civil' in obra.text:
                obra_encontrada = True
                break

        # Assert para garantir que a obra favoritada foi encontrada
        assert obra_encontrada, "A obra 'Guerra Civil' não foi encontrada na lista de favoritos"
        print("A obra 'Guerra Civil' foi encontrada na lista de favoritos.")
    except Exception as e:
        print(f"Erro ao favoritar a obra e verificar a lista de favoritos: {e}")
    finally:
        time.sleep(2)  # Aguarda 2 segundos para visualização

def test_notification_form(driver):
    url = "http://localhost:3000/obra/vazioForm"
    driver.get(url)

    try:
        # Espera até que o formulário esteja visível
        form = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "form"))
        )

        # Preenche o formulário
        email_input = driver.find_element(By.ID, "email")
        nome_input = driver.find_element(By.ID, "nome")
        telefone_input = driver.find_element(By.ID, "telefone")

        email_input.send_keys("teste@example.com")
        nome_input.send_keys("Teste Nome")
        telefone_input.send_keys("123456789")

        # Envia o formulário
        form.submit()

         # Espera pelo alerta de sucesso
        alert_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.swal2-confirm.btn.btn-success'))
        )

        # Clica no botão de confirmação do SweetAlert2
        alert_button.click()

        print("Formulário enviado e mensagem de sucesso exibida corretamente.")


    finally:
        time.sleep(2)  # Aguarda 2 segundos para visualização

if __name__ == "__main__":
    # Configura o WebDriver do Chrome
    driver = webdriver.Edge()

    try:
        test_analysis_page(driver)
        test_listar_obras_page(driver)
        test_filter_functionality(driver)
        test_info_button(driver)
        test_favorite_functionality(driver)
        test_notification_form(driver)
        test_admin(driver)
    finally:
        driver.quit()
