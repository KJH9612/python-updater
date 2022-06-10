import subprocess
import time

import requests
import os
import shutil
import boto3
import sys
from zipfile import ZipFile
from pathlib import Path
def main():
    VERSION = '1.0.0'
    APP_NAME = '셀파크롤러'
    PATH = os.path.dirname(__file__)
    BUCKET_FILE_PATH = 'files/latest'
    FRONT_URL = "https://cimg.sellpazg.co.kr/"
    REAL_PATH = os.getcwd()
    # 버전 체크
    s3_file_version = requests.get(f"{FRONT_URL}{BUCKET_FILE_PATH}/version.txt").text

    INSTALL_PATH = Path(__file__).resolve().parent.parent.parent
    DIR_FULL_PATH = Path(__file__).resolve().parent.parent

    print(REAL_PATH)
    print(REAL_PATH + f"\\{APP_NAME}-old.exe")

    # 이전 버전 삭제
    if os.path.exists(REAL_PATH + f"\\{APP_NAME}-old.exe"):
        os.unlink(REAL_PATH + f"\\{APP_NAME}-old.exe")

    try:
        if s3_file_version != VERSION:
            # 디렉토리 생성
            if not os.path.exists(PATH + "/latest"):
                os.makedirs(PATH + "/latest")

            # 파일 다운로드
            r = requests.get(f"{FRONT_URL}{BUCKET_FILE_PATH}/{APP_NAME}_{s3_file_version}.zip", stream=True)

            with open(PATH + f"/latest/{APP_NAME}_{s3_file_version}.zip", "wb") as fd:
                for chunk in r.iter_content(chunk_size=512):
                    fd.write(chunk)

            # ZIP 해제
            # shutil.unpack_archive(PATH + f"/latest/{APP_NAME}_{s3_file_version}.zip", PATH + "./latest")
            with ZipFile(PATH + f"/latest/{APP_NAME}_{s3_file_version}.zip", 'r') as zipObj:
                zipInfo = zipObj.infolist()
                for m in zipInfo:
                    m.filename = m.filename.encode('cp437').decode('euc-kr')
                    zipObj.extract(m, PATH + "/latest/")

            # 현재 파일이 존재하면
            if os.path.exists(REAL_PATH + f"/{APP_NAME}.exe"):
                os.rename(REAL_PATH + f"/{APP_NAME}.exe", REAL_PATH + f"/{APP_NAME}-old.exe")
            # print(__file__)
            # 최신버전 현재 디렉토리로 이동
            shutil.move(PATH + f"/latest/{APP_NAME}.exe", REAL_PATH + f"/{APP_NAME}.exe")
            shutil.rmtree(PATH + f"/latest")

            # 재시작
            # sys.stdout.flush()
            # os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
            # os.execv(f"{APP_NAME}.exe", [f"{APP_NAME}.exe"])
            # os.execl(sys.executable, sys.executable, *sys.argv)
            subprocess.call([sys.executable, REAL_PATH + f"{APP_NAME}.exe"] + sys.argv[1:])
        else:
            print(VERSION)
            os.system('pause')


    except Exception as e:
        print(e)
    os.system('pause')

main()
