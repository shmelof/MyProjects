import time
from settings import TOKEN
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from telegram import Update
from telegram.ext import MessageHandler, filters, ApplicationBuilder


def selenium_parser(price):
    options = Options()
    # options.add_argument("--headless")

    # Создаю браузер
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.maximize_window()
    # Ссылка на сайт и 1 секунда ожидания для полной загрузки(В коде после каждого запроса ставлю задержку. Далее
    # комментарием помечена она не будет)
    browser.get("https://www.dns-shop.ru/")
    time.sleep(3)

    # Код для выбора города поиска
    # select_town = browser.find_element(By.CSS_SELECTOR, 'span.city-select__icon')
    # select_town.click()
    # time.sleep(1)
    # input_town = browser.find_element(By.XPATH, "//input[@placeholder='Найти город']")
    # time.sleep(1)
    # input_town.send_keys("Екатеринбург")
    # time.sleep(1)
    # find_town = browser.find_element(By.XPATH, "//span[@class='base-ui-input-search__icon_oRx base-ui-input-search__icon_search_N2w base-ui-input-search__icon-location_left_ikg']")
    # find_town.click()
    # time.sleep(1)

    # Тут код на случай, если на сайте выходит окно по типу "Ваш город точно Екатеринбург?"
    # town = browser.find_element(By.CSS_SELECTOR, "span.base-ui-button-v2__text")
    # town.click()
    # time.sleep(3)

    # Ищу поисковую строку по сайту
    search_input = browser.find_element(By.XPATH, "//input[@placeholder='Поиск по сайту']")
    # Ввожу сообщение пользователя
    search_input.send_keys(price)
    # Ищу кнопку поиска
    search_button = browser.find_element(By.CSS_SELECTOR, "span.presearch__icon-search")
    # Нажимаю на кнопку поиска
    search_button.click()
    time.sleep(1)
    # Ищу кнопку сортировки полученного рез-та
    sort = browser.find_element(By.CSS_SELECTOR, "span.top-filter__icon")
    # Нажимаю на нее
    sort.click()
    # Ищу нужный мне тип сортировки. В моем случае использовал тип сортировки "Сначала недорогие"
    sort_by_low_price = browser.find_element(By.XPATH, "//span[text()='Сначала недорогие']")
    # Нажимаю на нее
    sort_by_low_price.click()
    time.sleep(3)
    # Ищу первый элемент на странице(Так как он самый дешевый), забираю у него часть с ценой и перевожу в текст
    low_price = browser.find_element(By.XPATH,
                                     "//div[@class='product-buy__price-wrap product-buy__price-wrap_interactive']").text

    time.sleep(3)
    # Закрываю браузер
    browser.close()
    # Возвращаю рез-тат своей функции
    return low_price

# Телеграмм бот --------------------------------------------------------------------------------------------------------


async def hello(update: Update, _):
    # Ищу сообщение отправителя
    user_text = update.message.text
    # Ищу имя отправителя
    user_name = update.effective_user.first_name
    print(f"Пользователь {user_name} отправил сообщение '{user_text}'")
    # Отвечаю пользователю
    await update.message.reply_text("Ищу информацию..")
    try:
        # Применяю функцию с парсером
        offers = selenium_parser(user_text)
        print(f"По запросу {user_text} результат: {offers}")
        # Отдаю ответ
        await update.message.reply_text(f"По запросу {user_text} результат: {offers}")
    except NoSuchElementException as exc:
        # Обрабатываю некорректный запрос
        print(f"По запросу {user_text} ничего не найдено")
        await update.message.reply_text(f"По запросу {user_text} ничего не найдено")

# Функция приложения и запуск скрипта ----------------------------------------------------------------------------------


def main():
    # Создаю приложение и подключаю бота
    app = ApplicationBuilder().token(TOKEN).build()
    # Добавляю обработчик сообщений
    app.add_handler(MessageHandler(filters.TEXT, hello))
    # Запускаю бота
    app.run_polling()


if __name__ == '__main__':
    main()
