import hydra
from hydra.core.config_store import ConfigStore
from hydra.utils import get_original_cwd
import os
import pyaudio
import wave

from src.config import Config

cs = ConfigStore.instance()
cs.store(name="config", node=Config)

class PlayAudio:
	def __init__(self, conf: Config):
		self.conf = conf
		self.audio = pyaudio.PyAudio()
		self.sample_format = conf.rec_params.sample_format
		self.channel = conf.rec_params.channels
		self.rate = conf.rec_params.fs
		self.chunk = conf.rec_params.chunk

	def start_playing(self, filename: str):
		wf = wave.open(filename, 'rb')
		self.stream = self.audio.open(
			format=self.audio.get_format_from_width(wf.getsampwidth()),
			channels=wf.getnchannels(),
			rate=wf.getframerate(),
			output=True
		)
		print("* playing")
		data = wf.readframes(self.chunk)
		self.play = True
		while data != b'' and self.play:
			self.stream.write(data)
			data = wf.readframes(self.chunk)

	def stop_playing(self):
		self.play = False

	def terminate(self):
		self.audio.terminate()


@hydra.main(config_path="../src/conf/", config_name="conf")
def main(conf: Config):
	record = PlayAudio(conf)
	record.start_playing(os.path.join(get_original_cwd(), './recordings/1648754506.wav'))
	record.terminate()


if __name__ == "__main__":
    main()