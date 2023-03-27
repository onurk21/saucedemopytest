import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


options = Options()
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")

@pytest.fixture(scope="module")
def driver():
     driver = webdriver.Chrome(options=options)
     driver.maximize_window() 
     driver.get("https://www.saucedemo.com/")
     yield driver
#sürekli tarayıcı acıp kaptmaktansa çıkış işlemi yapmaya yarar
def logout(driver):
    try:
        menu_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn")))
        menu_button.click()
        logout_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link")))
        logout_button.click()
        sleep(1)
    except:
        pass

#screenshot kaydı yapar
def save_screenshot(driver, name):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    directory = now.split('_')[0]
    if not os.path.exists(directory):
        os.mkdir(directory)
    filename = f"{directory}/{name}_{now}.png"
    driver.save_screenshot(filename)
#boş veri girilerek test yapar
def test_kullanici_adi_ve_sifre_bos_iken_Hata_donmesi(driver):
    
    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")
    

    username.send_keys("")
    password.send_keys("")
    
    login_button.click()
    error_message_container = driver.find_element(By.CLASS_NAME, "error-message-container")

    expected_message = "Epic sadface: Username is required"
    current_message = error_message_container.text
    status = expected_message == current_message

    assert status
    save_screenshot(driver,"kullanici_adi_ve_sifre_bos_iken_Hata_donmesi.png")
#şifre boşken gelen hatayı görüntüler
def test_sifre_bos_iken_Hata_donmesi(driver):
    driver.refresh()
    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")
    

    username.send_keys("deneme")
    password.send_keys("")
    

    login_button.click()
    error_message_container = driver.find_element(By.CLASS_NAME, "error-message-container")

    expected_message = "Epic sadface: Password is required"
    current_message = error_message_container.text
    status = expected_message == current_message

    assert status
    save_screenshot(driver,"sifre_bos_iken_Hata_donmesi.png")
#kilitli kullanıcadaki hatayı gösterir
def test_kilitli_kullanici_girildiginde_Hata_donmesi(driver):
    driver.refresh()
    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")
    

    username.send_keys("locked_out_user")
    password.send_keys("secret_sauce")
    

    login_button.click()
    error_message_container = driver.find_element(By.CLASS_NAME, "error-message-container")

    expected_message = "Epic sadface: Sorry, this user has been locked out."
    current_message = error_message_container.text
    status = expected_message == current_message

    assert status
    save_screenshot(driver,"kilitli_kullanici_girildiginde_Hata_donmesi.png")

# x butonuna basar
def test_X_iconuna_tiklama(driver):
     driver.refresh()

     username = driver.find_element(By.ID, "user-name")
     password = driver.find_element(By.ID, "password")
     login_button = driver.find_element(By.ID, "login-button")


     username.send_keys("")
     password.send_keys("")
     sleep(1)

     login_button.click()
     error_message_container = driver.find_element(
        By.CLASS_NAME, "error-message-container")
     error_button = driver.find_element(By.CLASS_NAME, "error-button")

     sleep(1)

     error_button.click()

     sleep(3)
     save_screenshot(driver, "X_iconuna_tiklama.png")

#https://www.saucedemo.com/inventory.html  açılıyormu ona bakar
def test_standart_kullanici_girildiginde_inventoryhtml_donmesi(driver):
    driver.refresh()
    logout(driver)
    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")
    

    username.send_keys("standard_user")
    password.send_keys("secret_sauce")
    

    login_button.click()
    

    current_url = driver.current_url
    expected_url = "https://www.saucedemo.com/inventory.html"
    status = current_url == expected_url

    assert status
    save_screenshot(driver,"standart_kullanici_girildiginde_inventoryhtml_donmesi.png")
#6 ürün listeleniyormu onu kontrol eder.
def test_6_urun_listesi(driver):
     logout(driver)
     username = driver.find_element(By.ID, "user-name")
     password = driver.find_element(By.ID, "password")
     login_button = driver.find_element(By.ID, "login-button")
     sleep(1)

     username.send_keys("standard_user")
     password.send_keys("secret_sauce")
     sleep(1)

     login_button.click()
     sleep(1)

     items = driver.find_elements(By.CLASS_NAME, "inventory_item")
     expected_item_count = 6
     status = len(items) == expected_item_count
     save_screenshot(driver,f"6_ürün_doğrulama.png")
#ürün fiyat doğrular
@pytest.mark.parametrize("item_name, item_price", [("Sauce Labs Backpack", 29.99),
                                                     ("Sauce Labs Bike Light", 9.99),
                                                     ("Sauce Labs Bolt T-Shirt", 15.99)])
def test_urun_fiyati_dogrulama(driver, item_name, item_price):
     driver.refresh()
     logout(driver)
     username = driver.find_element(By.ID, "user-name")
     password = driver.find_element(By.ID, "password")
     login_button = driver.find_element(By.ID, "login-button")
    

     username.send_keys("standard_user")
     password.send_keys("secret_sauce")
    

     login_button.click()
    

     item = driver.find_element(By.XPATH, f"//div[text()='{item_name}']/../../..//div[@class='pricebar']/div")
     price_text = item.text[1:]  # Remove the '$' sign from the beginning
     price = float(price_text)

     assert price == item_price
     save_screenshot(driver,f"{item_name}_fiyat_dogrulama.png")
     sleep (10)
#ürün sepete ekleme
def test_urun_sepete_ekleme(driver):
    driver.refresh()
    logout(driver)
    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username.send_keys("standard_user")
    password.send_keys("secret_sauce")
    login_button.click()

    item_name = "Sauce Labs Backpack"
    item = driver.find_element(By.XPATH, f"//div[@class='inventory_item_name'][text()='{item_name}']/ancestor::div[@class='inventory_item']//button")
    item.click()
    
    cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert cart_count.text == "1"

    save_screenshot(driver, "urun_sepete_ekleme.png")
#ürün sıralaması dorğumu onu kontrol eder
def test_urun_siralamasi(driver):
    driver.refresh()
    logout(driver)
    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username.send_keys("standard_user")
    password.send_keys("secret_sauce")
    login_button.click()

    sorting_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
    sorting_options = sorting_dropdown.find_elements(By.TAG_NAME, "option")

    for option in sorting_options:
        option_value = option.get_attribute("value")
        sorting_dropdown.send_keys(option_value)

        items = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        item_names = [item.text for item in items]
        sorted_item_names = sorted(item_names)

        assert item_names == sorted_item_names

    save_screenshot(driver, "urun_siralamasi.png")

#geri tuşuna tıklar ve ardından mevcut URL’in doğru olup olmadığını kontrol eder
def test_geri_tusu(driver):
    driver.refresh()
    logout(driver)
    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username.send_keys("standard_user")
    password.send_keys("secret_sauce")
    login_button.click()

    item_name = "Sauce Labs Bike Light"
    item = driver.find_element(By.XPATH, f"//div[text()='{item_name}']/../..//a")
    item.click()

    back_button = driver.find_element(By.CLASS_NAME, "inventory_details_back_button")
    back_button.click()

    current_url = driver.current_url
    expected_url = "https://www.saucedemo.com/inventory.html"
    status = current_url == expected_url

    assert status

    save_screenshot(driver, "geri_tusu.png")
#ürün filtrelemesi yapar
def test_urun_filtreleme(driver):
    driver.refresh()
    logout(driver)
    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username.send_keys("standard_user")
    password.send_keys("secret_sauce")
    login_button.click()

    filter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "product_sort_container")))
    sleep(2)
    filter_button.click()

    price_low_to_high = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[text()='Price (low to high)']")))
    sleep(2)
    price_low_to_high.click()

    items = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    expected_item_prices = sorted([float(item.text[1:]) for item in items])

    actual_item_prices = [float(item.text[1:]) for item in items]

    assert actual_item_prices == expected_item_prices

    save_screenshot(driver, "urun_filtreleme.png")

