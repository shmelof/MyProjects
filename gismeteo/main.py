import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from telegram import Update
from telegram.ext import MessageHandler, filters, ApplicationBuilder, CommandHandler, Updater


def gismeteo(town_user):
    options = Options()
    options.add_argument("--headless")

    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.set_window_size(1920, 1080)
    browser.get("https://www.gismeteo.ru/")
    time.sleep(1)

    select_town = browser.find_element(By.XPATH, "//input[@placeholder='поиск — через пробел можно уточнить страну или регион']")
    select_town.send_keys(town_user)
    time.sleep(1)
    town = browser.find_element(By.XPATH, "//a[@class='search-item list-item icon-menu icon-menu-gray']")
    town.click()
    mounth = browser.find_element(By.LINK_TEXT, 'Месяц')
    mounth.click()
    time.sleep(1)
    browser.execute_script("window.scrollTo(0, 300)")
    time.sleep(1)
    result = browser.find_element(By.XPATH, "//div[@class='widget widget-month']")
    result.screenshot('test.png')
    allres = result

    time.sleep(1)
    browser.close()
    return allres


async def start(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Введите город')


async def hello(update: Update, _):
    user_town = update.message.text
    await update.message.reply_text('Ожидайте..')
    try:
        res = gismeteo(user_town)
        await update.message.reply_photo('test.png')
        os.remove('test.png')
    except NoSuchElementException as exc:
        await update.message.reply_text(f"Город {user_town} не найден")


def main():
    start_handler = CommandHandler('start', start)
    app = ApplicationBuilder().token('5906092069:AAFelf6R-_YCub1jQwKgH8X5oFZfcs0BqZM').build()
    app.add_handler(start_handler)
    app.add_handler(MessageHandler(filters.TEXT, hello))
    app.run_polling()


if __name__ == '__main__':
    main()