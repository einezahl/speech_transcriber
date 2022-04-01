import requests
import os
import asyncio
import time
import hydra
from hydra.core.config_store import ConfigStore
from hydra.utils import get_original_cwd
from pydub import AudioSegment

from src.config import Config

cs = ConfigStore.instance()
cs.store(name="config", node=Config)

def read_file(filename):
   with open(filename, 'rb') as _file:
       while True:
           data = _file.read(5242880)
           if not data:
               break
           yield data

class AudioTranscriber:
  def __init__(self, conf: Config):
    self.auth_key = conf.trans_params.auth_key
    self.headers = {"authorization": self.auth_key, "content-type": "application/json"}
    self.conf = conf

  def prepare_data(self, filename):
      filepath = os.path.join(get_original_cwd(), self.conf.paths.recording_folder,  filename)
      sound = AudioSegment.from_file(f"{filepath}.wav", format="wav")
      sound.export(f"{filepath}.mp3", format="mp3")

  async def __get_audio_url(self, filename):
    filepath = os.path.join(get_original_cwd(), self.conf.paths.recording_folder,  f'{filename}.mp3')
    upload_response = requests.post('https://api.assemblyai.com/v2/upload', headers=self.headers, data=read_file(filepath))
    self.audio_url = upload_response.json()["upload_url"]

  async def __send_request(self):
    transcript_request = {'audio_url': self.audio_url}
    transcript_response = requests.post("https://api.assemblyai.com/v2/transcript", json=transcript_request, headers=self.headers)
    self.transcript_id = transcript_response.json()["id"]

  async def __get_transcript(self, filename):
    filepath = os.path.join(get_original_cwd(), self.conf.paths.transcript_folder,  f'{filename}.txt')
    processed = False
    max_loops = 30
    i = 0
    while not processed and i<max_loops:
      polling_response = requests.get("https://api.assemblyai.com/v2/transcript/" + self.transcript_id, headers=self.headers)
      if polling_response.json()["status"] == "completed":
        processed = True
      time.sleep(1)
      i+=1

    if processed:
      with open(filepath, 'w') as f:
        f.write(polling_response.json()['text'])
      print('Transcript saved to', filepath)

  def clean_up(self, filename):
    filepath = os.path.join(get_original_cwd(), self.conf.paths.recording_folder,  f'{filename}.mp3')
    os.remove(filepath)

  async def __run(self, filename):
    await self.__get_audio_url(filename)
    await self.__send_request()
    await self.__get_transcript(filename)

  def run(self, filename):
    self.prepare_data(filename)
    asyncio.run(self.__run(filename))
    self.clean_up(filename)

@hydra.main(config_path="../conf/", config_name="conf")
def run(conf: Config):
  transcriber = AudioTranscriber(conf)
  transcriber.run('1648766442')


if __name__ == "__main__":
  run()