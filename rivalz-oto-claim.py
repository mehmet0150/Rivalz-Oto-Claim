from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
from web3 import Web3
from pyvirtualdisplay import Display
from termcolor import colored

import time
import sys
import os
import platform
import urllib.request
import shutil

private_key = None
password = None
frag_URL = "https://rivalz.ai/fragmentz"  # mint sayfası
dashboard_URL = "https://rivalz.ai/dashboard"
addNetwork_URL = "chrome-extension://opfgelmcmbiajamepnmloijbpoleiama/popup.html#/settings/networks/"
RPC_URL = "https://rivalz2.rpc.caldera.xyz/http"
MAX_LOG_SIZE = 15 * 1024 * 1024  # 15 MB # Maksimum dosya boyutu (örneğin, 5 MB)

# Xvfb sanal ekranı başlat
display = Display(visible=False, size=(1920, 1080))
display.start()

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for file in self.files:
            file.write(obj)
            file.flush()  # Anında dosyaya yazılması için flush işlemi

    def flush(self):
        for file in self.files:
            file.flush()

def env_load():
    env_file = find_dotenv() # .env dosyasının var olup olmadığını kontrol et
    if env_file:
        load_dotenv() # .env dosyasını yükle
        # Hassas bilgileri .env dosyasından al
        global private_key, password
        private_key = os.getenv("PRIVATE_KEY")
        password = os.getenv("PASSWORD")
        if not private_key or not password:
            print(
                "Private Key veya parola bilgisine ulaşılamadı. Lütfen .env dosyasında bu bilgilerin olduğundan emin olun ve programı tekrar başlatın.")
            sys.exit()
    else:
        print(
            ".env dosyasına ulaşılamadı. Lütfen otomatik kurulum scriptini (install_and_run.sh) çalıştırın ve kurulum sonrası bir .env dosyası oluşturulması için gereken bilgileri girin.")
        sys.exit()

# Dosya varsa boyutunu kontrol et
if os.path.exists("output_log.txt") and os.path.getsize("output_log.txt") > MAX_LOG_SIZE:
    with open("output_log.txt", "w") as log_file:
        log_file.write("Log dosyası sıfırlandı.")  # Dosyayı sıfırla
        log_file.close
    log_file = open("output_log.txt", "a") # Dosyayı açıyoruz (appending mode ile açıyoruz, yani eski içerik üzerine yazmadan ekliyoruz)
else:
    log_file = open("output_log.txt", "a") # Dosyayı açıyoruz (appending mode ile açıyoruz, yani eski içerik üzerine yazmadan ekliyoruz)
sys.stdout = Tee(sys.stdout, log_file) # Ekran ve dosya çıktıları için Tee sınıfını kullanıyoruz

def center_text(text, width):
    return text.center(width)

def print_mk_gradient():
    mk_art = [
        " M     M   K   K   ",
        " MM   MM   K  K    ",
        " M M M M   K K     ",
        " M  M  M   KK      ",
        " M     M   K K     ",
        " M     M   K  K    ",
        " M     M   K   K   "
    ]
    # Renkler (Gradyan)
    colors = ["blue", "yellow", "green", "cyan", "blue", "magenta", "white"]

    # Terminalin genişliğini al
    terminal_width = shutil.get_terminal_size().columns
    print()
    print()

    # Her satırı ortalayarak yazdır
    for i, line in enumerate(mk_art):
        color = colors[i % len(colors)]  # Renkleri sırayla uygula
        print(center_text(colored(line, color), terminal_width))

    time.sleep(1)  # Bir süre bekleyerek efektin görünmesini sağla


# Rivalz Fragmentz Oto Claim yazısını ortalı şekilde yazdırma
def print_rivalz_text():
    # Rivalz Fragmentz Oto Claim metni
    text = "Rivalz Fragmentz v2 Oto Claim"
    terminal_width = shutil.get_terminal_size().columns
    print(center_text(colored(text, "blue"), terminal_width))
    print()
    print()


def clear_terminal():
    # Eğer Windows ise cls komutunu kullan
    if platform.system().lower() == "windows":
        os.system("cls")
    else:
        os.system("clear")


# Rainbow uzantı dosyasını indirme fonksiyonu
def download_rainbow_extension():
    # Uzantının indirileceği dosya yolu
    extension_path = os.path.join(os.getcwd(), 'RainbowExtension.crx')

    # Uzantının zaten indirilip indirilmediğini kontrol et
    if os.path.exists(extension_path):
        print('Uzantı daha önce indirilmiş, tekrar indirilmeyecek.')
        return extension_path

    # Uzantıyı indirmek için URL
    print('Chrome için Rainbow Wallet uzantısı indirliyor. Lütfen bekleyiniz...')
    url = 'https://clients2.googleusercontent.com/crx/blobs/AYA8VyzQJMBDG2siRj4AO7PQ4u8gsHE1LzeybYgCJymjMypaLnUP7xJ5rLiYd__IxdIWSRQJhxgw22bRfjVRcGZGpXg-sslgH7GnE-lJtcXE8mHdiKMuWbx_aJPaX3F59_2_AMZSmuUve8gayBaxZNWfIUK4yD2vhFwDXQ/OPFGELMCMBIAJAMEPNMLOIJBPOLEIAMA_1_5_58_0.crx'

    # Dosyayı indir
    urllib.request.urlretrieve(url, extension_path)
    print('Uzantı indirme işlemi tamamlandı.')

    return extension_path


# Selenium WebDriver başlatma ve uzantıyı yükleme fonksiyonu
def launch_selenium_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")  # Sandbox'ı devre dışı bırak
    chrome_options.add_argument("--disable-dev-shm-usage")  # Geliştirme paylaşımlı bellek hatalarını önle
    chrome_options.add_argument("window-size=1920x1080")  # Ekran boyutunu ayarla

    extension_path = download_rainbow_extension()
    chrome_options.add_extension(extension_path)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    time.sleep(1)
    print("Rainbow Wallet uzantısı Chrome'a yüklendi.")
    return driver

def launch_driver():
    env_load()
    driver=launch_selenium_webdriver()    # Driver nesnesini başlat ve chrome çalıştır
    driver.maximize_window()    # chrome tam ekran yap
    rainbow_setup(driver, password)    # cüzdan içe aktarma işlemlerini başlat

# Rainbow cüzdan içe aktarma
def rainbow_setup(driver, password):
    try:
        WebDriverWait(driver, 30).until(lambda d: len(d.window_handles) > 1)        # Rainbow ayarlama sekmesinin açılmasını bekle
        print("Rainbow sekmesi açıldı.")
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])        # Yeni sekmeye geç
        print("Rainbow sekmesi aktif sekme olarak belirlendi ve içe aktarma işlemine başlandı...")

        # Elementlerin varlığını bekle ve tıkla
        if driver.title == "Rainbow Wallet":
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/button/div/div/div'))).click()
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[3]/div/div[1]/div/div[1]/div[2]/div/div[1]'))).click()
            time.sleep(1)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div/div/div[2]/div/div/div[3]/div/div[3]/div/div[1]/div[2]/div/div[1]'))).click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/input'))).send_keys(private_key)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div/button/div/div/div[2]'))).click()
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div[2]/div/div[1]/input'))).send_keys(password)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div[1]/input'))).send_keys(password)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div/button'))).click()
            web3 = Web3(Web3.HTTPProvider(RPC_URL))
            account = web3.eth.account.from_key(private_key)            # Private key ile cüzdan adresini alınıyor.
            print(f"Cüzdan içe aktarma işlemi tamamlandı. Cüzdan adresi {account.address}")
            time.sleep(2)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])            # İlk sekmeyi aktif et ve işlemlere oradan devam et
            add_network_rainbow(driver)            # add_network_rainbow fonksiyonuna geç
        else:
            print("Geçerli sayfa Rainbow Wallet sayfası değil. Tekrar denenecek...")
            rainbow_setup(driver, password)
    except Exception as e:
        print("Cüzdan içe aktarma fonksiyonunda bir hata oluştu. Hata: ", str(e))
        driver.quit()
        launch_driver()


# Rainbow'a yeni ağ ekleme fonksiyonu
def add_network_rainbow(driver):
    print("Rivalz2 ağını cüzdana ekleme işlemi başlatıldı...")
    driver.get(addNetwork_URL)

    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div/div/div'))).click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id=":r4:"]'))).send_keys("Rivalz2")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div/div/div[2]/div/div/div/div[2]/div/div/input'))).send_keys("https://rivalz2.rpc.caldera.xyz/http")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div/div/div[2]/div/div/div/div[3]/div/div/input'))).send_keys("ETH")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div/div/div[2]/div/div/div/div[4]/div/div/input'))).send_keys("https://rivalz2.explorer.caldera.xyz")
        time.sleep(5)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div/div/div[2]/div/div/div/div[7]/div/button/div/div/div'))).click()
        print("Ağ ekleme işlemi başarıyla tamamlandı.")
        connect_to_website(driver)        # Siteye bağlanma fonksiyonuna git.
    except Exception as e:
        print("Ağ ekleme fonksiyonunda bir hata oluştu. İşlemler tekrar başlatılıyor... Hata: ", str(e))
        driver.quit()
        launch_driver()


# Siteye bağlanma fonksiyonu
def connect_to_website(driver):
    driver.get(dashboard_URL)
    print('Rivalz Dashboard sayfası yüklendi.')

    try:
        print('Cüzdanı siteye bağlama işlemine başlanıyor...')
        # Wallet connect butonunu kontrol et ve tıkla
        wallet_connect_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div[1]/button'))
        )
        wallet_connect_btn.click()
        # Rainbow butonunu kontrol et ve tıkla
        rainbow_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/div[3]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div/button/div/div/div[2]/div'))
        )
        rainbow_btn.click()

        # Popup onay penceresinin açılmasını bekle
        WebDriverWait(driver, 30).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[1])
        rainbow_approve = (WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 '//*[@id="main"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div[2]/div[1]/button/div/div/div[1]/div/div/div'))))
        rainbow_approve.click()
        time.sleep(2)

        # Popup sign penceresinin açılmasını bekle
        WebDriverWait(driver, 30).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[1])
        rainbow_sign = (WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 '//*[@id="main"]/div/div/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/button/div/div/div[1]/div/div/div'))))
        rainbow_sign.click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0])
        print("Cüzdan websitesine başarıyla bağlandı.")
        eth_balance(driver)        # Bakiye sorgulama fonksiyonuna git
    except Exception as e:
        print("Websitesine bağlanırken bir hata oluştu. İşlemler tekrar başlatılıyor... Hata: ", str(e))
        driver.quit()
        launch_driver()


# ETH bakiye sorgulama fonksiyonu
def eth_balance(driver):
    try:
        print("İşlem ücretleri için bakiye sorgulaması yapılıyor...")
        web3 = Web3(Web3.HTTPProvider(RPC_URL))
        account = web3.eth.account.from_key(private_key)        # Private key ile bir cüzdan adresi oluşturun
        # ETH miktarını al
        while True:
            balance = web3.eth.get_balance(account.address)
            eth_balance = web3.from_wei(balance, 'ether')            # Wei cinsinden bakiyeyi Ether cinsine dönüştür
            if eth_balance > 0.00005:
                print(
                    f"Sorgulama başarı ile tamamlandı. Bakiye yeterli. ({eth_balance:.11f} ETH) İşlemlere devam ediliyor...")
                break
            else:
                print(
                    f"Cüzdanda işlem ücretlerini karşılayacak kadar bakiye bulunmuyor. Mevcut bakiye: ({eth_balance:.11f} ETH) Lütfen https://rivalz2.hub.caldera.xyz/ adresinden {account.address} için faucet alın ve işlemin devam etmesini bekleyin.")
                time.sleep(30)
        mint_frag(driver)
    except Exception as e:
        print("Bakiye sorgulaması sırasında bir hata oluştu. İşlemler tekrar başlatılıyor... Hata: ", str(e))
        driver.quit()
        launch_driver()


# Fragmentz mintleme hazırlık fonksiyonu
def mint_frag(driver):
    try:
        driver.get(frag_URL)
        print("Rivalz Fragmentz sayfası yüklendi.")
        while True:
            time.sleep(5)
            # Geri sayım sayacının varlığı kontrol ediliyor.
            control = driver.find_elements(By.CSS_SELECTOR, 'p.css-fboh26')
            if control:
                # Mintlenebilr fragmentz sayısının kaç olduğu belirleniyor
                element = driver.find_elements(By.CSS_SELECTOR, 'div.css-1m6litc')
                if element:
                    frag_count = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-1m6litc'))
                    )
                    frag_count_number = int(frag_count.text.split()[0])  # "20 mint" -> 20
                    print(f"Mintlenebilir Fragmentz sayısı: {frag_count_number} - Mintleme işlemine başlanıyor...")
                    for i in range(1, frag_count_number+1):
                        # mint işlemini yap
                        mint_process(driver)
                        toast_description = WebDriverWait(driver, 60).until( # mintleme fonksiyonu sonrası dönen bilgilendirme metnini bekle ve al
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-161kwbg')))
                        if toast_description:
                            toast_text = toast_description.text
                            if toast_text == "Claimed successfully!":
                                print(f"{i}. Mint işlemi başarıyla tamamlandı.")
                            elif toast_text == "transaction failed":
                                print(f"{i}. Mint işlemi sırasında bir sorun oluştu. Tekrar denenecek.")
                            elif toast_text == "Please sign message with your wallet":
                                print(f"Cüzdandan imza işlemi gerekiyor. İmzalama işlemi deneniyor...")
                                driver.quit()
                                launch_driver()
                        else:
                            print(f"Uyarı: Mint işlemi sonrası bilgilendirme mesajı alınamadı. Sonuç bilinmiyor.")
                        time.sleep(5) # mint işlemi denemesinden sonra 5 saniye bekle
                    element2 = driver.find_elements(By.CSS_SELECTOR, 'div.css-1m6litc') # mintlenebilir fragmentz sayısı var mı diye bak
                    if not element2:
                        print("Mintlenebilir Fragmentz bulunamadı. İşlem tamamlandı.")
                else:
                    time.sleep(5)
                    wait_time = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'p.css-fboh26'))
                    )
                    wait = datetime.strptime(wait_time.text, "%H:%M.%S") # Süreyi datetime objesine çevir
                    total_seconds = wait.hour * 3600 + wait.minute * 60 + wait.second # Toplam saniyeyi hesapla
                    current_time = datetime.now() # Şimdiki zamanı al
                    added_time = timedelta(seconds=total_seconds) # wait nesnesinin toplam süre değerini al
                    new_time = current_time + added_time # Şimdiki zamanın üzerine ekle
                    print(
                        f"Mint için kalan süre: {wait_time.text} Bu süre sonunda otomatik olarak tekrar denenecek. Tahmini deneme zamanı: {new_time.strftime('%d.%m.%Y - %H:%M:%S')}")
                    driver.quit()
                    time.sleep(total_seconds)
                    launch_driver()
            else:
                print("Rivalz Fragmentz mint sayfasında değiliz. Tekrar denenecek. Mevcut adres: " + driver.current_url)
                eth_balance(driver)
    except Exception as e:
        driver.save_screenshot("mint_frag_error.png")
        print("Mint işlemine hazırlık sırasında bir hata oluştu. İşlemler tekrar başlatılıyor... Hata: ", str(e))
        driver.quit()
        launch_driver()

def mint_process(driver):
    try:
        mint_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div.css-1m6litc'))
        )
        tab_count = len(driver.window_handles)
        mint_btn.click()
        WebDriverWait(driver, 30).until(lambda d: len(d.window_handles) > tab_count)
        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        approve_btn = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//*[@id="main"]/div/div/div[1]/div/div/div/div/div/div[2]/div[4]/div[2]/button/div/div/div[1]/div/div/div'))
        )
        tab_count = len(driver.window_handles)
        approve_btn.click()
        WebDriverWait(driver, 30).until(lambda d: len(d.window_handles) < tab_count)
        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
    except Exception as e:
        driver.save_screenshot('mint_error.png')
        print("Mint işlemi sırasında bir hata oluştu. İşlem başarısız oldu. Hata: ", str(e))


# Ana işlev
def main():
    clear_terminal()
    print_mk_gradient()
    print_rivalz_text()
    time.sleep(1)
    launch_driver()

if __name__ == "__main__":
    main()
