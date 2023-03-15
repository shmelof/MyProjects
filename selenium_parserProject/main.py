import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters


def selenium_paraser(job_title):
    options = Options()
    # options.add_argument("--headless")

    browser = webdriver.Chrome("/chromedriver", options=options)
    browser.maximize_window()

    browser.get("https://hh.ru")

    search_input = browser.find_element(By.ID, "a11y-search-input")
    search_input.send_keys(job_title)

    # search_input.submit()

    search_button = browser.find_element(By.CSS_SELECTOR, 'button[data-qa="search-button"]')
    search_button.click()

    vacancies_count = browser.find_element(By.CSS_SELECTOR, '[data-qa="vacancies-search-header"]')
    v_c = vacancies_count.text
    time.sleep(3)
    browser.close()
    return v_c


async def hello(update: Update, _):
    user_text = update.message.text
    user_name = update.effective_user.first_name
    print(f"Пользователь {user_name} отправил сообщение '{user_text}'")
    await update.message.reply_text("Ищу информацию...")
    try:
        offers = selenium_paraser(user_text)
        print(f"По запросу {user_text} результат: {offers}")
        await update.message.reply_text(f"По запросу {user_text} результат: {offers}")
    except NoSuchElementException as exc:
        print(f"По запросу {user_text} ничего не найдено")
        await update.message.reply_text(f"По запросу {user_text} ничего не найдено")


def main():
    app = ApplicationBuilder().token('5925428563:AAH0989LOxqVfa7aYlPZ6KnxoECv9-hVW2U').build()
    app.add_handler(MessageHandler(filters.TEXT, hello))
    app.run_polling()


if __name__ == '__main__':
    main()