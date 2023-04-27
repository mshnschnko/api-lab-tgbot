import os
from typing import Union
from dotenv import load_dotenv
import yadisk
import platform
from aiogram import types


dotenv_path = '.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

YA_TOKEN = os.environ.get("YA_TOKEN")
y = yadisk.YaDisk(token=YA_TOKEN)

BOT_OWNER_ID = os.environ.get("BOT_OWNER_ID")

USERS_STORAGE_FOLDER = "tg_storage/users_files/"
REMOTE_BACKUP_FOLDER = "tg_storage/files_backup/"
LOCAL_STORAGE = "storage"
LOCAL_BACKUP_FOLDER = "storage/backup/"
LOCAL_TEMP_FOLDER = "storage/temp/"

async def upload(message: types.Message) -> None:
    filename = ''
    file = None
    if not message.document is None:
        file = message.document
        # filename = message.document.file_name + message.document.file_id
        filename = message.document.file_name
    elif not message.photo is None:
        file = message.photo[0]
        file_type = 'photo'
        filename = message.photo[0].file_id + ".png"
    elif not message.video is None:
        file = message.video
        file_type = 'video'
        # filename = message.video.file_name + message.video.file_id
        filename = message.video.file_name
    elif not message.audio is None:
        file = message.audio
        file_type = 'audio'
        # filename = message.audio.file_name + message.audio.file_id
        filename = message.audio.file_name
    # elif not message.voice is None:
    #     file = message.voice
    #     file_type = 'voice'
    #     filename = message.voice.file_id
    else:
        await message.answer("Файл данного типа нельзя сохранить.")
        file = None
        return


    await file.download(destination_file=LOCAL_TEMP_FOLDER+filename)
    # await message.document.download(destination=LOCAL_TEMP_FOLDER+message.document.file_name)
    # filename = message.document.file_name
    print("Token is actual" if y.check_token() else "Please, update token")
    try:
        y.mkdir(f"{USERS_STORAGE_FOLDER}{message.from_id}")
    except:
        pass
    try:
        y.upload(f"{LOCAL_TEMP_FOLDER}{filename}", f"{USERS_STORAGE_FOLDER}{message.from_id}/{filename}", overwrite=True)
        if os.path.isfile(os.path.join(LOCAL_TEMP_FOLDER, filename)):
                os.remove(os.path.join(LOCAL_TEMP_FOLDER, filename))
        # await message.answer("Файл успешно загружен.")
    except Exception as ex:
        return ex
        # await message.answer("Возникла ошибка.")