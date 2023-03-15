import moviepy.editor
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters


def mp4tomp3(path):
    video_file = path
    video = moviepy.editor.VideoFileClip(f'{video_file}')
    audio = video.audio
    audio.write_audiofile(f'{video_file.stem}.mp3')


async def hello(update: Update):
    user_video = update.message.video
    user_name = update.effective_user.first_name
    print(f"Пользователь {user_name} отправил сообщение '{user_video}'")
    await update.message.reply_text("Processing...")
    result = mp4tomp3(user_video)
    await update.message.reply_text(f"По запросу {user_video} результат: {result}")
