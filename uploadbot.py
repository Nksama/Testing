from pyrogram import Client , filters , enums
from pyrogram.types import Message
import os
import requests

bot = Client(
    "bbot",
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
    bot_token=os.environ['BTOKEN']
)

CHANNEL_ID = -1001797893141
BOT_USERNAME = "dynastyanimeuploaderbot" #WITOUT @

@bot.on_message(filters.document & filters.user([2114972069, 5704299476, 6713194639]))
def main(_,m : Message):
    x = bot.send_document(CHANNEL_ID,m.document.file_id)
    msg_id = x.id
    m.reply(f"https://t.me/{BOT_USERNAME}?start={msg_id}")

@bot.on_message(filters.command("start"))
def start(_,m : Message):
    if len(m.text.split(" ")) == 2:
        msg_id = m.text.split(" ")[1]
        msg_id = int(msg_id)
        doc = bot.get_messages(CHANNEL_ID , msg_id)
        doc.copy(m.chat.id)
    else:
        m.reply("Hello there, only admins can use me")


def progress(current, total):
    print(f"{current * 100 / total:.1f}%")
    rply.edit(f"{current * 100 / total:.1f}%")
    



def download_file_with_progress(url, filename):
  """Downloads a file with progress tracked in MB and returned as a dictionary.

  Args:
      url (str): URL of the file to download.
      filename (str): Name of the file to save to.

  Returns:
      dict: {'downloaded_mb': float, 'total_size_mb': float} or None on error.
  """

  downloaded = 0
  try:
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise exception for non-200 status codes

    if response.status_code == 200:
      total_size_bytes = int(response.headers.get('Content-Length', 0))  # Handle missing header
      total_size_mb = total_size_bytes / (1024**2)  # Convert to MB

      progress = {'downloaded_mb': 0.0, 'total_size_mb': total_size_mb}

      with open(filename, 'wb') as f:
        for data in response.iter_content(chunk_size=1024):
          downloaded += len(data)
          downloaded_mb = downloaded / (1024**2)  # Convert downloaded bytes to MB

          progress['downloaded_mb'] = downloaded_mb

          # Print progress every 1 MB or on the last chunk
          if downloaded_mb % 1 == 0 or downloaded == total_size_bytes:
            print(f"Downloaded: {downloaded_mb:.1f} MB ({downloaded_mb:.1f}/{total_size_mb:.1f} MB)")

          f.write(data)

      if downloaded != total_size_bytes:
        raise Exception(f"Downloaded size ({downloaded_bytes} bytes) doesn't match total size ({total_size_bytes} bytes)")

      return progress
    else:
      raise Exception(f"Download failed: {response.status_code}")

  except requests.exceptions.RequestException as e:
    raise Exception(f"Download error: {e}")





@bot.on_message(filters.command("upload") & filters.user([5704299476 , 6713194639]))
def upload(_, m):
    link = m.text.split(" ")[1]
    filename = m.text.split(" ")[2]
    dl = m.reply("DOWNLOADING...") 
    # x = requests.get(link).content
    # with open(filename , "wb") as f:
    #     f.write(x)

    x = download_file_with_progress(link , filename)
    dl.edit(f"Downloaded: {progress['downloaded_percent']:.1f}%")

    global rply
    rply = m.reply("UPLOADING...")
    bot.send_chat_action(m.from_user.id , enums.ChatAction.UPLOAD_VIDEO)
    m.reply_document(filename , progress=progress)
    os.remove(filename)


bot.run()
