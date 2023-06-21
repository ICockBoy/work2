import asyncio

from TGConvertor.manager.manager import SessionManager
from pathlib import Path


api_id = 6
api_hash = "eb06d4abfb49dc3eeb1aeb98ae0f581e"


def load_form_tdata_folder(folder_path: str):
    return SessionManager.from_tdata_folder(Path(folder_path)).to_pyrogram_string()


if __name__ == '__main__':
    print(load_form_tdata_folder(input("folder:")))