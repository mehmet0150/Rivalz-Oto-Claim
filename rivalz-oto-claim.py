from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time
import os
import urllib.request
# .env dosyasını yükle
load_dotenv()

# Hassas bilgileri .env dosyasından al
recovery_phrase = os.getenv("RECOVERY_PHRASE")
password = os.getenv("PASSWORD")
frag_URL = "https://rivalz.ai/fragmentz" #mint sayfası
dashboard_URL = "https://rivalz.ai/dashboard"

# Metamask uzantı dosyasını indirme fonksiyonu
def download_metamask_extension():
    print('Setting up Metamask extension. Metamask extention downloading. Please wait...')
    url = 'https://clients2.googleusercontent.com/crx/blobs/AYA8Vyx63VqZeuXodFV0KRL5uSXw2QHxi-rflMuVH3zJlut5HkIsd8YNlwvK9WJ4_2FAQLa65CbbaChOxq5EAL-bGmNZEJLC0a-TUNFJ59C3P3oz6T23GOh3QJQiLjEQ1iWJAMZSmuW2iyNFOmPuT4P7jcUqjpWVMWh6Tw/metamask_12_5_0_0.crx'
    extension_path = os.path.join(os.getcwd(), 'metamaskExtension.crx')
    urllib.request.urlretrieve(url, extension_path)
    print('Metamask extension downloaded.')
    return extension_path

# Selenium WebDriver başlatma ve uzantıyı yükleme fonksiyonu
def launch_selenium_webdriver():
    chrome_options = Options()
    # Headless modda çalıştırmak için aşağıdaki satırı ekle
    chrome_options.add_argument("--headless")  # Tarayıcı arayüzü olmadan çalıştırır
    chrome_options.add_argument("--no-sandbox")  # Sandbox'ı devre dışı bırak
    chrome_options.add_argument("--disable-dev-shm-usage")  # Geliştirme paylaşımlı bellek hatalarını önler
    chrome_options.add_argument("window-size=1920x1080")  # Ekran boyutunu ayarla

    extension_path = download_metamask_extension()
    chrome_options.add_extension(extension_path)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    time.sleep(1)
    print("Chrome with Metamask extension loaded.")
    return driver

# Metamask hesap ayarlama
def metamask_setup(driver, password):
    # Sekme açılmasını bekle
    initial_tab_count = len(driver.window_handles)

    # Yeni sekmenin açılmasını bekle
    try:
        WebDriverWait(driver, 30).until(lambda d: len(d.window_handles) > initial_tab_count)
        print("Metamask tab is opened.")

        # Yeni sekmeye geç
        driver.switch_to.window(driver.window_handles[1])
        print("Switched to new tab...")

        # Elementin varlığını bekle ve tıkla
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "onboarding__terms-checkbox"))).click()

        # Diğer butonlar için benzer şekilde devam et
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/ul/li[2]/button'))).click()

        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button[1]'))).click()

        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input'))).send_keys(password)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input'))).send_keys(password)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[3]/label/span[1]/input'))).click()

        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button'))).click()

        # İlgili diğer butonlar için benzer şekilde devam et
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button[1]'))).click()

        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="popover-content"]/div/div/section/div[1]/div/div/label/input'))).click()

        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="popover-content"]/div/div/section/div[2]/div/button[2]'))).click()

        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'))).click()

        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'))).click()

        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'))).click()

        print("Wallet has been created successfully.")

        # add_network_metamask fonksiyonuna geç
        add_network_metamask(driver)
    except Exception as e:
        print("Could not open a new tab or switch:", str(e))

# Metamask'te yeni ağ ekleme fonksiyonu

def add_network_metamask(driver):
    print("The network addition process has started...")
    try:
        #time.sleep(20)
        # MetaMask yeni ağ ekleme
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[1]/button/span[1]'))
        )
        driver.execute_script("arguments[0].click();", element)

        # Butona tıklamak için var olmasını bekle
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/section/div[2]/button'))
        ).click()

        # Ağ bilgilerini doldurma
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="networkName"]'))
        ).send_keys("Rivalz2")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/section/div/div[1]/div[2]/div[1]'))
        ).click()

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/section/div/div[1]/div[2]/div[2]/div/div/button'))
        ).click()

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="rpcUrl"]'))
        ).send_keys("https://rivalz2.rpc.caldera.xyz/http")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="rpcName"]'))
        ).send_keys("Rivalz2")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/section/div/div[2]/button'))
        ).click()

        chain_id_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="chainId"]'))
        )
        chain_id_input.send_keys("6966")

        symbol_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="nativeCurrency"]'))
        )
        symbol_input.send_keys("ETH")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/section/div/div[1]/div[5]/div[1]'))
        ).click()

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/section/div/div[1]/div[5]/div[2]/div/div/button'))
        ).click()

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="additional-rpc-url"]'))
        ).send_keys("https://rivalz2.explorer.caldera.xyz")

        # Ekle düğmesine tıklama
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/section/div/div[2]/button'))
        ).click()

        # Kaydet düğmesine tıklama
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/section/div/div[2]/button'))
        ).click()

        print("Network added successfully.")
        change_metamask_network(driver, "Rivalz2")

    except Exception as e:
        print("An error occurred while adding the network:", str(e))
# Ağı değiştirme fonksiyonu
def change_metamask_network(driver, network_name):
    # opening network
    try:
        print("Changing network...")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[1]/button/span[1]'))
        ).click()

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH,  f"//p[contains(text(), '{network_name}')]"))
        ).click()
        print(f"Switched to '{network_name}' network.")
        metamask_wallet_import(driver, recovery_phrase)

    except Exception as e:
        print("An error occurred while changing network:", str(e))


def metamask_wallet_import(driver, recovery_phrase):
    print("Setting up Mint wallet...")
    try:
        # Cüzdanı içe aktarma işlemleri
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[2]/button/span[1]/span'))
        ).click()

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/section/div[2]/button'))
        ).click()

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/section/div/div[2]/button'))
        ).click()

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="private-key-box"]'))
        ).send_keys(recovery_phrase)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/section/div/div/div[2]/button[2]'))
        ).click()
        time.sleep(1)
        # Hesap seçimini kontrol et
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'multichain-account-picker__label')]"))
        )
        actual_text = driver.execute_script(
            "return document.querySelector('span.multichain-account-picker__label').innerText;")

        # Karşılaştırma yap
        expected_text = "Account 2"
        if actual_text == expected_text:
            print("Adding wallet was successful. Successfully migrated to Mint wallet.")
            connect_to_website(driver)
        else:
            print(actual_text)
            print("Adding wallet failed. Run the program again.")

    except Exception as e:
        print("An error occurred while importing the wallet:", str(e))

# Siteye bağlanma fonksiyonu
def connect_to_website(driver):
    print('Connecting to the site...')
    driver.get(dashboard_URL)
    try:
        # İlk butonu kontrol et ve tıkla
        button1 = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div[1]/button'))
        )
        button1.click()
        metamask = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div/button/div/div/div[2]/div'))
        )
        metamask.click()
        while True:
            tab_count= len(driver.window_handles)
            if tab_count<4:
                time.sleep(1)
            else:
                driver.switch_to.window(driver.window_handles[3])
                next = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app-content"]/div/div/div/div[3]/div[2]/footer/button[2]'))
                )
                next.click()
                time.sleep(1)
                connect = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app-content"]/div/div/div/div[3]/div[2]/footer/button[2]'))
                )
                connect.click()
                while True:
                    tab_count2 = len(driver.window_handles)
                    if tab_count2<4:
                        time.sleep(1)
                    else:
                        driver.switch_to.window(driver.window_handles[3])
                        sign = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="app-content"]/div/div/div/div/div[3]/button[2]'))
                        )
                        sign.click()
                        time.sleep(3)
                        print('Site connected to Metamask.')
                        driver.switch_to.window(driver.window_handles[1])
                        break
                break
    except Exception as e:
        print("Run the program again. An error occurred:", str(e))

def mint(driver):
    print("Going to Rivalz Fragmentz page...")
    driver.get(frag_URL)

    while True:
        time.sleep(5)
        # sayacın varlığı kontrol ediliyor.
        control = driver.find_elements(By.CSS_SELECTOR, 'p.css-fboh26')
        if control:
            element = driver.find_elements(By.CSS_SELECTOR, 'div.css-1m6litc')
            if element:
                frag_count = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-1m6litc'))
                )
                frag_count_number = int(frag_count.text.split()[0])  # "20 mint" -> 20
                print(f"Number of mintable fragments:{frag_count_number} - Starting the Mint process...")
                for i in range(0,frag_count_number):
                    mint_btn = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, 'div.css-1m6litc'))
                    )
                    mint_btn.click()
                    while True:
                        tab_count = len(driver.window_handles)
                        if tab_count < 4:
                            time.sleep(1)
                        else:
                            driver.switch_to.window(driver.window_handles[3])
                            approve_btn = WebDriverWait(driver, 30).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '//*[@id="app-content"]/div/div/div/div/div[3]/button[2]'))
                            )
                            approve_btn.click()
                            driver.switch_to.window(driver.window_handles[1])
                            print(f"{i+1}. Mint transaction completed.")
                            break
                    time.sleep(5)
                element2 = driver.find_elements(By.CSS_SELECTOR, 'div.css-1m6litc')
                if not element2:
                    print("Fragmentz minting process is over.")
            else:
                time.sleep(5)
                wait_time = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'p.css-fboh26'))
                )
                # Süreyi datetime objesine çevir
                wait = datetime.strptime(wait_time.text, "%H:%M.%S")
                # Toplam saniyeyi hesapla
                total_seconds = wait.hour * 3600 + wait.minute * 60 + wait.second
                # Şimdiki zamanı al
                current_time = datetime.now()
                # wait nesnesinin toplam süre değerini al
                added_time = timedelta(seconds=total_seconds)
                # Şimdiki zamanın üzerine ekle
                new_time = current_time + added_time
                print(
                    f"Mint için kalan süre: {wait_time.text} Bu süre sonunda otomatik olarak tekrar denenecek. Tahmini deneme zamanı: {new_time.strftime('%d.%m.%Y - %H:%M:%S')}")
                time.sleep(total_seconds)
        else:
            print(driver.current_url)
            print("We are not on the Mint page. Trying again.")
            mint(driver)

# Ana işlev
def main():
    driver = launch_selenium_webdriver()
    driver.maximize_window()
    metamask_setup(driver, password)
    while True:
        mint(driver)


if __name__ == "__main__":
    main()
