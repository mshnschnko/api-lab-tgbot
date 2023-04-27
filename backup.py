from dotenv import load_dotenv
import os
import platform
import yadisk
import asyncio
import aioschedule
import time

dotenv_path = '.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

YA_TOKEN = os.environ.get("YA_TOKEN")
y = yadisk.YaDisk(token=YA_TOKEN)

USERS_STORAGE_FOLDER = "tg_storage/users_files/"
REMOTE_BACKUP_FOLDER = "tg_storage/files_backup/"
LOCAL_STORAGE = "storage"
LOCAL_BACKUP_FOLDER = "storage/backup/"
LOCAL_TEMP_FOLDER = "storage/temp/"

def backup():
    try:
        if os.path.isdir(f'{LOCAL_BACKUP_FOLDER}'):
                os.system(f'rm -rf {LOCAL_BACKUP_FOLDER}*')
        # y.download("/tg_storage/", "./storage/backup/")
        for i in list(y.listdir(USERS_STORAGE_FOLDER)):
            dir_name = i['name']
            try:
                os.mkdir(f'{LOCAL_BACKUP_FOLDER}{dir_name}')
            except Exception as ex:
                print(ex)
            for j in list(y.listdir(f"{USERS_STORAGE_FOLDER}{dir_name}/")):
                file_name = j['name']
                y.download(f'{USERS_STORAGE_FOLDER}{dir_name}/{file_name}', f'{LOCAL_BACKUP_FOLDER}{dir_name}/{file_name}')
        print(platform.system())
        ext = str()
        if platform.system() == 'Windows':
            os.system(f'powershell Compress-Archive -Force "{os.path.join(LOCAL_STORAGE, "backup")}"\
                        {os.path.join(LOCAL_STORAGE, "temp", "backup.zip")}')
            print("сделал зип")
            # os.system(f'powershell Compress-Archive -Force "{os.path.join(LOCAL_STORAGE, "dump.sql")}"\
            #             -Update {os.path.join(LOCAL_STORAGE, "temp", "backup.zip")}')
            ext = 'zip'
        elif platform.system() == 'Linux':
            # os.system(f'zip -r {os.path.join(LOCAL_STORAGE, "temp", "backup.zip")} {os.path.join(LOCAL_STORAGE, "backup")}')
            os.system(f'tar -jcvf {os.path.join(LOCAL_STORAGE, "temp", "backup.tar")}\
                        {os.path.join(LOCAL_STORAGE, "backup")} {os.path.join(LOCAL_STORAGE, "dump.sql")}')
            # os.system(f'tar -jrvf {os.path.join(LOCAL_STORAGE, "temp", "backup.tar")} {os.path.join(LOCAL_STORAGE, "dump.sql")}')
            ext = 'tar'
        try:
            y.upload(f'{os.path.join(LOCAL_STORAGE, "temp", f"backup.{ext}")}', f'{REMOTE_BACKUP_FOLDER}backup.{ext}', overwrite=True)
        except:
             time.sleep(3)
        print("загрузил архив")
        print("перед удалением темпа")
        if os.path.isfile(os.path.join(LOCAL_STORAGE, "temp", f"backup.{ext}")):
                    print("temp removed")
                    os.remove(os.path.join(LOCAL_STORAGE, "temp", f"backup.{ext}"))
        print("перед удалением бэкапа")
        if os.path.isdir(f'{LOCAL_BACKUP_FOLDER}'):
                print("backup removed")
                os.system(f'rm -rf {LOCAL_BACKUP_FOLDER}*')
    except Exception as ex:
        print(ex)

async def async_backup():
    backup()


if __name__ == "__main__":
    backup()
    aioschedule.every(1).day.do(async_backup)
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(aioschedule.run_pending())
        time.sleep(1)