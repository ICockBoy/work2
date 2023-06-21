import asyncio

from pyrogram import Client
from pyrogram.types import ChatPrivileges

token = "5611863889:AAE-UpQbZBhmt7aosaLMydP1H7tm5RtKZ5k"
client_str = "BQAAAAAAjC-6N_3BV_JQ6Rr-NUC_MLKAjwoDRUgizo5bp1wjNeYSpUc5UoYMWCwedItuyDVLQ1UiDIaBC3CetUyp2sl1E8bL9ow31nKIHS4RGfwV_MI1ukOJaskCIy0IwzLHITxo_xx_mAaLc5vpqk9OVCrxRqM_CC70i3XXGvU8NR9s4ptx6pH2be1a0JYXvVzzyuKb8aoS2auZ8-aRl8-YHdlvca2p--UqbfyoVIGbi61_6eDdMRbjGvdwH2q67XIE7Th60uJ7Oq7yll3D1BH1v7OrOuUstPfKszYIBkg_n0eia-t89Ljg_r6fYjnwajyQXm_raCmx0b1HnqP2_COBkaNMOgAAAAAAACcPAA"
api_id = 6
api_hash = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
client = Client("_", api_id=api_id, api_hash=api_hash, session_string=client_str, in_memory=True)
client_bot = Client("_", api_id=api_id, api_hash=api_hash, bot_token=token, in_memory=True)


async def change_link(chat_id):
    chat = await client_bot.get_chat(chat_id)
    chat.

async def run():
    await client_bot.start()
    await client.start()

if __name__ == "__main__":
    asyncio.run(run())
