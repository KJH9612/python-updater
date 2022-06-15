import requests
import os
import shutil
import sys
from zipfile import ZipFile

VERSION = '1.0.0'
APP_NAME = 'APP_NAME'
PATH = os.path.dirname(__file__)
BUCKET_FILE_PATH = ''
FRONT_URL = ""
REAL_PATH = os.getcwd()

filepath = sys.argv[0]
filename = filepath[filepath.rfind("\\") + 1:filepath.rfind(".exe")]


def removePrevVersion():
    # 이전 버전 삭제
    if os.path.exists(REAL_PATH + f"\\{filename}-old.exe"):
        print("FILE EXISTS")
        os.unlink(REAL_PATH + f"\\{filename}-old.exe")


def getNewVersion():
    return requests.get(f"{FRONT_URL}{BUCKET_FILE_PATH}/version.txt").text


def createDirectory():
    # 디렉토리 생성
    if not os.path.exists(PATH + "/latest"):
        os.makedirs(PATH + "/latest")


def fileDownload(version):
    # 파일 다운로드
    r = requests.get(f"{FRONT_URL}{BUCKET_FILE_PATH}/{APP_NAME}_{version}.zip", stream=True)

    with open(PATH + f"/latest/{APP_NAME}_{version}.zip", "wb") as fd:
        for chunk in r.iter_content(chunk_size=512):
            fd.write(chunk)


def main():
    # 버전 체크
    new_version = getNewVersion()

    try:
        if new_version != VERSION:
            createDirectory()
            fileDownload(new_version)

            # ZIP 해제
            with ZipFile(PATH + f"/latest/{APP_NAME}_{new_version}.zip", 'r') as zipObj:
                zipInfo = zipObj.infolist()
                for m in zipInfo:
                    m.filename = m.filename.encode('cp437').decode('euc-kr')
                    zipObj.extract(m, PATH + "/latest/")

            # 현재 파일이 존재하면
            if os.path.exists(REAL_PATH + f"/{filename}.exe"):
                os.rename(REAL_PATH + f"/{filename}.exe", REAL_PATH + f"/{filename}-old.exe")

            # 최신버전 현재 디렉토리로 이동
            shutil.move(PATH + f"/latest/{APP_NAME}.exe", REAL_PATH + f"/{filename}.exe")
            shutil.rmtree(PATH + f"/latest")

            # 재시작
            os.startfile(fr"{REAL_PATH}/{filename}.exe")

            sys.exit()
    except Exception as e:
        print(e)

# 1
main()

os.system('pause')