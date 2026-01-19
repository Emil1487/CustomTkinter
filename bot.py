import os
import asyncio
from pyrogram import Client, filters
import yt_dlp
from pyrogram.types import Message

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.text & ~filters.private & ~filters.command("start"))
async def download_video(client: Client, message: Message):
    url = message.text.strip()
    if not ("youtube.com" in url or "youtu.be" in url):
        await message.reply("Отправьте ссылку на YouTube!")
        return
    
    await message.reply("🔄 Скачиваю видео...")
    
    ydl_opts = {
        'format': 'best[height<=720]/best[ext=mp4]',
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            await message.reply(f"📥 Скачиваю: {title[:50]}...")
            ydl.download([url])
        
        files = [f for f in os.listdir('.') if f.endswith(('.mp4', '.mkv', '.webm'))]
        if files:
            video_file = files[0]
            file_size = os.path.getsize(video_file) / (1024**2)
            if file_size > 2000:  # >2GB
                await message.reply("❌ Файл слишком большой (>2GB).")
                os.remove(video_file)
                return
            await client.send_video(message.chat.id, video_file, caption=title)
            os.remove(video_file)
            await message.delete()  # Удаляем сообщение с ссылкой
        else:
            await message.reply("❌ Не удалось скачать.")
    except Exception as e:
        await message.reply(f"❌ Ошибка: {str(e)}")

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply("Отправьте ссылку на YouTube для скачивания!")

if __name__ == "__main__":
    app.run()