import requests
import os
import asyncio
import time
import hydra
from hydra.core.config_store import ConfigStore
from hydra.utils import get_original_cwd

from src.config import RecordingConfig

cs = ConfigStore.instance()
cs.store(name="recording_config", node=RecordingConfig)

def read_file(filename):
   with open(filename, 'rb') as _file:
       while True:
           data = _file.read(5242880)
           if not data:
               break
           yield data

auth_key = '9c4204d8e38f4e698ec518edaa7e5018'
headers = {"authorization": auth_key, "content-type": "application/json"}

async def get_audio_url(filepath):
  global headers
  upload_response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=read_file(filepath))
  audio_url = upload_response.json()["upload_url"]

  print(audio_url)
  return audio_url

async def send_request(audio_url):
  global headers
  transcript_request = {'audio_url': audio_url}
  transcript_response = requests.post("https://api.assemblyai.com/v2/transcript", json=transcript_request, headers=headers)
  id = transcript_response.json()["id"]
  print(id)
  return id

async def get_transcript(transcript_id, filepath_trans):
  processed = False
  max_loops = 30
  i = 0
  while not processed and i<max_loops:
    polling_response = requests.get("https://api.assemblyai.com/v2/transcript/" + transcript_id, headers=headers)
    if polling_response.json()["status"] == "completed":
      processed = True
    time.sleep(1)
    print(processed)
    i+=1

  if processed:
    with open(filepath_trans, 'w') as f:
      f.write(polling_response.json()['text'])
    print('Transcript saved to', transcript_id, '.txt')

async def main(conf: RecordingConfig):
  filepath = os.path.join(get_original_cwd(), conf.paths.recording_folder,  'output.mp3')
  filepath_trans = os.path.join(get_original_cwd(), conf.paths.transcript_folder,  'output.txt')
  audio_url = await get_audio_url(filepath)
  id = await send_request(audio_url)
  await get_transcript(id, filepath_trans)

@hydra.main(config_path="../conf/", config_name="conf")
def run(conf: RecordingConfig):
  asyncio.run(main(conf))


if __name__ == "__main__":
  run()