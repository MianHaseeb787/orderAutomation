from selenium import webdriver
# import undetected_chromedriver as webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import re
import io
import time

with open("lastOrder.txt", "r") as file:
    order_number = file.readline().strip()
    print(order_number)

options = Options()
options.page_load_strategy = 'normal'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver = webdriver.Chrome(
    options=options,
)

driver.get("https://aestheticmedicine.ie/wp-admin/admin.php?page=wc-orders")
time.sleep(5)

email_input = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
email_input.send_keys("MianAdmin")

pass_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
pass_input.send_keys("jmZkYY%CMk4pttTeB1i(aVMX")

submit_btn = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]' )
submit_btn.click()
time.sleep(5)


order1 = driver.find_element(By.CSS_SELECTOR, "tbody#the-list tr:first-child")
orderId = driver.find_element(By.CSS_SELECTOR, "tbody#the-list tr:first-child").get_attribute('id')
print(orderId)

if orderId == order_number:
     driver.quit()

with open("lastOrder.txt", "w") as file:
    order_number = file.writelines(orderId)
    # print(order_number)

order1.click()
time.sleep(5)

second_edit_address = driver.find_element(By.CSS_SELECTOR, 'div.order_data_column_container > div.order_data_column:nth-of-type(3) > h3 > a.edit_address')
second_edit_address.click()
time.sleep(4)
firstName = driver.find_element(By.ID, "_shipping_first_name").get_attribute('value')
lastName = driver.find_element(By.ID, "_shipping_last_name").get_attribute('value')
shippingAddress1 = driver.find_element(By.ID, "_shipping_address_1").get_attribute('value')
shippingAddress2 = driver.find_element(By.ID, "_shipping_address_2").get_attribute('value')
shippingCity = driver.find_element(By.ID, "_shipping_city").get_attribute('value')
shippingPostalCode = driver.find_element(By.ID, "_shipping_postcode").get_attribute('value')

emaila = driver.find_element(By.ID, "_billing_email").get_attribute('value')
phoneNumber = driver.find_element(By.ID, "_billing_phone").get_attribute('value')


select_country = driver.find_element(By.ID, '_shipping_country')
select = Select(select_country)
country = select.first_selected_option


select_state = driver.find_element(By.ID, '_shipping_state')
select = Select(select_state)
state = select.first_selected_option


print(country.text)
print(state.text)
print(firstName)
print(lastName)
print(shippingAddress1)
print(shippingAddress2)
print(shippingCity)
print(shippingPostalCode)
print(emaila)
print(phoneNumber)


orderItems = driver.find_elements(By.CSS_SELECTOR, "tbody#order_line_items > tr")
print(len(orderItems))


orders = []

for item in orderItems:
    sku = item.find_element(By.CSS_SELECTOR, "div.wc-order-item-sku").text
    sku = sku.replace("SKU:", "").strip()
    quantity = item.find_element(By.CSS_SELECTOR, "td.quantity > div.view").text
    quantity = quantity.replace("×", "").strip()

    orders.append({"sku": sku, "quantity" : quantity})
    print(orders)

    # print(sku)
    # print(quantity)


driver.get("https://estetik.pl/")
driver.execute_script("document.body.style.zoom='30%'")
time.sleep(10)

goFurtherBtn = driver.find_element(By.CSS_SELECTOR, "div.medical-popup-bttns > a.btn-red")
goFurtherBtn.click()

acceptAllBtn = driver.find_element(By.CSS_SELECTOR, "button.js__accept-all-consents")
acceptAllBtn.click()

for order in orders:
    print(order.get("sku"))

    # try:
    #     cross = driver.find_element(By.CSS_SELECTOR, "div.search__input-area-item > span.icon-close")
    #     cross.click()
    # except:
    #     print("no cross")

    searchInput = driver.find_element(By.CSS_SELECTOR, "div.search__input-area-item.search__input-area-item_grow >  input")
    searchInput.send_keys(order.get("sku"))
    time.sleep(4)

    try:
        searchButton = driver.find_element(By.CSS_SELECTOR, "button.js__search-submit-btn")
        searchButton = driver.find_element(By.CSS_SELECTOR, "ul.search__list > li.search__list-item")
        searchButton.click()
        time.sleep(10)

    except:
        logo = driver.find_element(By.CSS_SELECTOR, "a.link-logo")
        logo.click()
        time.sleep(5)
        continue
        # driver.execute_script("document.body.style.zoom='30%'")

    try:
        driver.execute_script("document.body.style.zoom='50%'")
        time.sleep(1)
        quantity_input = driver.find_element(By.CSS_SELECTOR, 'input[name="quantity"]')
        quantity_input.clear()
        quantity_input.send_keys(order.get('quantity'))
        addToCartBtn = driver.find_element(By.CLASS_NAME, "addtobasket")
        addToCartBtn.click()
        time.sleep(10)


        continueShoppingBtn = driver.find_element(By.CSS_SELECTOR, "div.modal-close")
        continueShoppingBtn.click()
        time.sleep(2)
    
    except Exception as e:
        # alert = driver.find_element(By.CSS_SELECTOR, "div.alert-info.alert > p").text
        # if alert == "Nie znaleziono produktów spełniających podane kryteria.":
            print(f"item not found     {e}")
    
    logo = driver.find_element(By.CSS_SELECTOR, "a.link-logo")
    logo.click()
    time.sleep(5)

# cartBtn = driver.find_element(By.CSS_SELECTOR, "div.icons-panel__icon-wrapper > a > img")
# cartBtn.click()
# time.sleep(5)

driver.get("https://estetik.pl/pl/basket")
time.sleep(10)

driver.execute_script("document.body.style.zoom='50%'")
time.sleep(1)

# paymentOption = driver.find_element(By.CSS_SELECTOR, "div.payment-css-15 > span.name > span")
# driver.execute_script("arguments[0].click();", paymentOption)

orderBtn = driver.find_element(By.CSS_SELECTOR, "button.order.btn")
driver.execute_script("arguments[0].click();", orderBtn)
time.sleep(5)

orderBtn = driver.find_element(By.CSS_SELECTOR, "button.order.btn")
driver.execute_script("arguments[0].click();", orderBtn)
time.sleep(5)


email = driver.find_element(By.CSS_SELECTOR, "table.maindata > tbody > tr.mail > td.input > div > input")
name = driver.find_element(By.CSS_SELECTOR, "table.maindata > tbody > tr.name > td.input > div > input")
surname = driver.find_element(By.CSS_SELECTOR, "table.maindata > tbody > tr.surname > td.input > div > input")
phone = driver.find_element(By.CSS_SELECTOR, "table.maindata > tbody > tr.phone > td.input > div > input")
address = driver.find_element(By.CSS_SELECTOR, "table.address > tbody > tr.other_address > td.input > div > input")
zipcode = driver.find_element(By.CSS_SELECTOR, "table.address > tbody > tr.zip > td.input > div > input")
city = driver.find_element(By.CSS_SELECTOR, "table.address > tbody > tr.city > td.input > div > input")


email.send_keys('mianhaseeb.ce@gmail.com')
# aestheticmedicineireland@gmail.com
driver.execute_script("document.body.style.zoom='50%'")

time.sleep(1)
driver.execute_script("document.body.style.zoom='30%'")
time.sleep(1.5)

name.send_keys("Aesthetic")
surname.send_keys("Medicine")
phone.send_keys("852565715")
address.send_keys("132 The Sycamores")
# zipcode.send_keys("R45P935")
zipcode.click()
time.sleep(1)
zipcode.send_keys("25000")
city.send_keys("Edenderry")


differentAddressCheckbox = driver.find_element(By.CSS_SELECTOR, "tr.different_address > td.input > span.checkbox-wrap")
differentAddressCheckbox.click()
time.sleep(5)

# differentEmail = driver.find_element(By.CSS_SELECTOR, "table.address-different> tbody > tr.mail2 > td.input > div > input")
differentName = driver.find_element(By.CSS_SELECTOR, "table.address-different> tbody > tr.name2 > td.input > div > input")
differentSurname = driver.find_element(By.CSS_SELECTOR, "table.address-different> tbody > tr.surname2 > td.input > div > input")
differentPhone = driver.find_element(By.CSS_SELECTOR, "table.address-different> tbody > tr.phone2 > td.input > div > input")

differentAddress = driver.find_element(By.CSS_SELECTOR, "table.address-different > tbody > tr.other_address2 > td.input > div >input")
differentZipcode = driver.find_element(By.CSS_SELECTOR, "table.address-different > tbody > tr.zip2 > td.input > div > input")
differentCity = driver.find_element(By.CSS_SELECTOR, "table.address-different> tbody > tr.city2 > td.input > div > input")

# differentEmail.send_keys(emaila)
differentName.send_keys(firstName)
differentSurname.send_keys(lastName)
differentPhone.send_keys(phoneNumber)
differentAddress.send_keys(shippingAddress1)
differentZipcode.click()
time.sleep(1)
differentZipcode.send_keys(shippingPostalCode)

# differentZipcode.send_keys(shippingPostalCode)
differentCity.send_keys(shippingCity)

checkbox = driver.find_element(By.CSS_SELECTOR, 'input[name="additional_2"]')
driver.execute_script("arguments[0].click();", checkbox)


SummaryButton = driver.find_element(By.CSS_SELECTOR, 'button[name="button2"]')
SummaryButton.click()




time.sleep(1000)
