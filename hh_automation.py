from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import csv

caps = DesiredCapabilities().CHROME
caps['pageLoadStrategy'] = 'eager'
options = Options()
options.add_experimental_option('detach', True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ["enable-automation"])
#options.add_argument('--headless')
options.add_argument('--disable-gpu')

letter = """Уважаемые рекрутеры

Я рад представить Вам свою кандидатуру на вакансию разработчика Python в Вашей компании. Я считаю, что мой опыт работы в области программирования, особенно в языке Python, и мои навыки смогут принести большую пользу Вашей компании.

В моих предыдущих проектах, я использовал Python для разработки программного обеспечения, которое успешно решало задачи, связанные с обработкой больших объемов данных, автоматизацией рутинных задач и созданием веб-приложений. Я также имею опыт работы с популярными фреймворками Python, такими как Django и Flask. Свободно владею английским языком. 

Я всегда стремлюсь к саморазвитию и усовершенствованию своих навыков. Я люблю изучать новые технологии и применять их в своей работе. Вместе с тем, я умею работать в команде и с готовностью принимаю на себя ответственность за результаты своей работы.

Я уверен, что мой опыт, знания и умения могут быть полезны для Вашей компании и я хотел бы получить возможность показать свои способности в работе с Вашей командой. Я готов ответить на любые дополнительные вопросы и надеюсь на возможность пройти собеседование.

С уважением,
Полуяхтов Евгений Евгеньевич"""
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options, desired_capabilities=caps)

print("OPENING MAIN PAGE...")
driver.get("https://www.hh.ru")

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            """

})
counter = 0
driver.maximize_window()
time.sleep(30)

with open("C:\\Users\\я\\Desktop\\myProjects\\scrapper\\data\\vacancies_list_all.csv",  'r', encoding='utf16') as vacancies:
    print("OPENED VACANCIES LIST!")
    
    links = csv.DictReader(vacancies)

    for link in links:
        driver.get(link['Ссылка'])

        if counter >= 200:
            exit()

        try:
            try:
                next_click = driver.find_element('xpath', "//a[@class='bloko-button bloko-button_kind-success bloko-button_scale-large bloko-button_stretched']")
            
            except NoSuchElementException:
                print("ANOTHER DESIGN OF PAGE, JUST SKIPPING")
                continue
            
            if next_click.text == 'Откликнуться':
                next_click.click()
                time.sleep(3)
            
            else:
                continue
            
            try:
                confirmation = driver.find_element('xpath', "//span[text()='Все равно откликнуться']")
                confirmation.click()
                time.sleep(3)
            
            except Exception:
                print("Нет опции подтвердить!")
                continue
            
            try:
                send_letter = driver.find_element('xpath', "//span[text()='Написать сопроводительное']")
                send_letter.click()
                time.sleep(3)
            
            except Exception:
                print("Нету кнопки Для сопроводительного")
                continue
            
            letter_input = driver.find_elements('xpath', "//textarea[@class = 'bloko-textarea bloko-textarea_sized-rows']")
            letter_input[0].click()
            letter_input[0].send_keys(letter)
            time.sleep(1)

            confirm = driver.find_element('xpath', "//span[text()='Отправить']")
            confirm.click()
            time.sleep(2)
            counter += 1
            print("RESUMES ACCEPTED - " + str(counter))
        except IndexError:
            print("Seems that this vacancy in archive!")
        
        time.sleep(1)
    

print("DONE!")
























#options.add_argument('--profile-directory=Default')
#options.add_argument('--headless')
#options.add_argument('--user-data-dir=C:\\Users\\я\\AppData\\Local\\Google\\Chrome\\User Data\\')