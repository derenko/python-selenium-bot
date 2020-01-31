from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from config import EMAIL, PASSWORD, executable_path

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("window-size=1900,1080")

driver = webdriver.Chrome(
    executable_path=executable_path,
    options=chrome_options
)

running = True
works_counter = 0
total_time = 0


def get_works():
    global works_counter
    global running
    global total_time

    start = time.time()
    driver.get("https://linkum.ru/user/crowd/")

    elements = driver.find_elements_by_css_selector(".dl.crowd_task")

    alert_message = ''

    for element in elements:
        element.click()
        time.sleep(1)

        try:
            driver.find_element_by_css_selector(".form_work input").click()
            time.sleep(1)
        except:
            time.sleep(1)
            driver.find_element_by_css_selector(".form_work input").click()

        try:
            alert = driver.switch_to_alert()
            alert_message = alert.text

            if(alert_message == 'У вас в работе уже больше 50 заказов. Пожалуйста, выполните сначала их.'):
                print(f'-----------------------------------------\n')
                print('КОЛИЧЕСТВО ДОПУСТИМЫХ ПРИНЯТЫХ РАБОТ ПРЕВЫШЕНО')
                running = False
                return

            alert.dismiss()
        except:
            print("Что то пошло не так...Перезапустите приложение")

        works_counter += 1
        print(f'{alert_message}\nОбщее количество принятых работ : {works_counter}')

    end = time.time()
    total_page_time = int(end - start)
    total_time += (total_page_time)


driver.get("https://linkum.ru/")
driver.find_element_by_css_selector(".login a").click()
time.sleep(1.5)
driver.find_element_by_id("login").send_keys(EMAIL)
driver.find_element_by_id("pass").send_keys(PASSWORD)
driver.find_element_by_id("loginsubmit").click()

while(running):
    try:
        get_works()
    except:
        running = False

driver.quit()
print(f'Завершено! Количество полученных работ {works_counter}.')
print(f'Прошло всего времени {total_time} сек.')
print(f'\n-----------------------------------------')
