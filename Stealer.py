import instabot
import shutil
from instabot import Bot
from downloader import c
import downloader
import os


Name = (c[18:])
Dir = (".\\memes\\" + (Name))
dir_path = '.\\memes\\'

print(Dir)

bot = Bot()
bot.login(username="eyeslearnscode", password="Gobwio01")

bot.upload_photo((Dir), caption="a")

print("Removing Meme")
shutil.rmtree(dir_path)
print("Meme Removed")
