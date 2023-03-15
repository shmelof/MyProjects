# import time
#
# from settings import TOKEN
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.common.exceptions import NoSuchElementException
# from telegram import Update
# from telegram.ext import ApplicationBuilder, MessageHandler, filters
# # Драйвер для Chrome
# # import chromedriver_binary
#
# # токен из settings.py
# # TOKEN = "my token"
#
#
# def selenium_paraser(job_title):
#     # Конфигурация браузера
#     options = Options()
#     options.add_argument("--headless")
#
#     # Создаем браузер
#     browser = webdriver.Chrome("/chromedriver", options=options)
#     browser.maximize_window()
#
#     # Делаем запрос к сайту
#     browser.get("https://hh.ru")
#
#     # Ищем форму поиска
#     search_input = browser.find_element(By.ID, "a11y-search-input")
#     search_input.send_keys(job_title)
#
#     # # Отправить форму
#     # search_input.submit()
#
#     # Ищем кнопку и нажимаем
#     search_button = browser.find_element(By.CSS_SELECTOR, 'button[data-qa="search-button"]')
#     search_button.click()
#
#     # Ищем данные со страницы(количество вакансий)
#     vacancies_count = browser.find_element(By.CSS_SELECTOR, '[data-qa="vacancies-search-header"]')
#     v_c = vacancies_count.text
#     time.sleep(3)
#     browser.close()
#     return v_c
#
#
# async def hello(update: Update, _):
#     # Ищу сообщение отправителя
#     user_text = update.message.text
#     # Ищу имя отправителя
#     user_name = update.effective_user.first_name
#     print(f"Пользователь {user_name} отправил сообщение '{user_text}'")
#     # Отвечаю пользователю
#     await update.message.reply_text(f"Пользователь {user_name} отправил сообщение '{user_text}'")
#     await update.message.reply_text("Ищу информацию..")
#     try:
#         # Применяю функцию с парсером
#         offers = selenium_paraser(user_text)
#         print(f"По запросу {user_text} результат: {offers}")
#         # Отдаю ответ
#         await update.message.reply_text(f"По запросу {user_text} результат: {offers}")
#     except NoSuchElementException as exc:
#         # Обрабатываю некорректный запрос
#         print(f"По запросу {user_text} ничего не найдено")
#         await update.message.reply_text(f"По запросу {user_text} ничего не найдено")
#
#
# def main():
#     # Создаю приложение
#     app = ApplicationBuilder().token(TOKEN).build()
#     # Добавляю обработчик сообщений
#     app.add_handler(MessageHandler(filters.TEXT, hello))
#     # Запускаю бота
#     app.run_polling()
#
#
# if __name__ == "__main__":
#     main()
