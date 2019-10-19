from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Deixe o programa rodar e controlar as abas do navegador. Não minimize nem clique em nelas se for possível, pode atrapalhar.
# Let the program run and control your navigator tabs. Don't minimize the navigator and neither click on something, this can confuse the bot

linkPlaylistSpotify = "Link of Spotify playlist that you want to clone" # Ex: https://open.spotify.com/playlist/4nE6NVcObcxBs2hQjD0WL3?si=swWhfQAORwyyVxIyFgyR4g
nomePlaylist = "Name that you want for your youtube playlist" # Ex: Sad Songs
emailYoutube = "Your email of youtube" # Ex: YOUREMAIL@GMAIL.COM
passwordYoutube = "Your password of youtube" # Ex: PASSWORD
path = "D:\Selenium\chromedriver.exe" # You need to have chromedriver.exe of your chrome version


def logarYoutube(navegador, email, senha):

    WebDriverWait(navegador, 20).until(EC.element_to_be_clickable((By.XPATH, "//ytd-button-renderer[@class='style-scope ytd-masthead style-suggestive size-small']"))).click()
    WebDriverWait(navegador, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='email']"))).send_keys(email)
    WebDriverWait(navegador, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='identifierNext']"))).click()
    WebDriverWait(navegador, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys(senha)
    WebDriverWait(navegador, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='passwordNext']"))).click()
    if "youtube.com" not in navegador.current_url:
        print("Não redirecionou pro yt")
        navegador.get('https://www.youtube.com/?gl=BR')
        time.sleep(2)


def criarPlaylist(navegador, input, nomePlaylist):

    input.send_keys(nomePlaylist)
    WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.XPATH, "//ytd-button-renderer[@class='style-scope ytd-add-to-playlist-create-renderer style-blue-text size-default']"))).click()
    time.sleep(0.5)


def adicionarMusica(navegador, nomeMusica, bandaMusicaNome, isPrimeiraVez, nomePlaylist):
    barraPesquisa = WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.ID, 'search')))
    botaoPesquisar = WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.ID, 'search-icon-legacy')))
    barraPesquisa.send_keys(Keys.CONTROL + "a")
    barraPesquisa.send_keys(Keys.DELETE)
    barraPesquisa.send_keys(nomeMusica + " " + bandaMusicaNome)
    botaoPesquisar.click()
    time.sleep(1)
    # caixaVideo = WebDriverWait(navegador, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//ytd-video-renderer[@class='style-scope ytd-item-section-renderer']")))[0]
    elementoMusica = WebDriverWait(navegador, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'ytd-video-renderer')))[0]
    hover = ActionChains(navegador).move_to_element(elementoMusica)
    hover.perform()
    botaoExpandirOpcoes = WebDriverWait(elementoMusica, 20).until(EC.visibility_of_element_located((By.XPATH, ".//yt-icon-button[@id='button']/button")))
    botaoExpandirOpcoes.click()
    time.sleep(0.25)
    botaoAdicionarPlaylist = WebDriverWait(navegador, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//yt-formatted-string[text()='Salvar na playlist']")))
    botaoAdicionarPlaylist.click()
    if isPrimeiraVez:
        WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                           "//ytd-add-to-playlist-create-renderer[@class='style-scope ytd-add-to-playlist-renderer']"))).click()
        inputNomePlaylist = WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='style-scope paper-input' and @placeholder='Insira o nome da playlist...']")))
        criarPlaylist(navegador, inputNomePlaylist, nomePlaylist)
        time.sleep(1)
    else:
        elementoPlaylist = WebDriverWait(navegador, 20).until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='checkbox-label']/yt-formatted-string[text()='" + nomePlaylist + "']")))
        elementoPlaylist.click()
        xSair = WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.XPATH, "//yt-icon-button[@id='close-button']")))
        xSair.click()
        time.sleep(1)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
driver = webdriver.Chrome(path, options=chrome_options)
driver.get(linkPlaylistSpotify)
tabSpotify = driver.window_handles[0]
driver.execute_script("window.open('https://www.youtube.com/?gl=BR','_blank');")
WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))
newWindow = driver.window_handles
tabYoutube = newWindow[1]
driver.switch_to.window(tabYoutube)
logarYoutube(driver, emailYoutube, passwordYoutube)
time.sleep(1)
driver.switch_to.window(tabSpotify)
musicas = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tracklist-row")))
print("Quantidade de musicas na playlist: {}".format(len(musicas)))

for x in range(0, len(musicas), 1):
    Musica = WebDriverWait(musicas[x], 20).until(EC.presence_of_element_located((By.CLASS_NAME, "tracklist-name")))
    nomeMusica = Musica.text
    bandaMusica = WebDriverWait(musicas[x], 20).until(EC.presence_of_element_located((By.CLASS_NAME, "tracklist-row__artist-name-link")))
    bandaMusicaNome = bandaMusica.text
    print(str(x) + " - Nome da música = {}\nNome da banda = {}".format(nomeMusica, bandaMusicaNome))
    driver.switch_to.window(tabYoutube)
    time.sleep(0.5)
    if x == 0:
        adicionarMusica(driver, nomeMusica, bandaMusicaNome, True, nomePlaylist)
    else:
        adicionarMusica(driver, nomeMusica, bandaMusicaNome, False, nomePlaylist)
    time.sleep(0.5)
    driver.switch_to.window(tabSpotify)

driver.quit()
