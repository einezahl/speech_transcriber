import time
import hydra
from hydra.core.config_store import ConfigStore
from hydra.utils import get_original_cwd
import os
import pyaudio
import wave

from src.config import Config

cs = ConfigStore.instance()
cs.store(name="config", node=Config)


class AudioPlayer:
    def __init__(self, conf: Config):
        self.audio = pyaudio.PyAudio()
        self.chunk = conf.rec_params.chunk

    def start_playing(self, filename: str):
        self.wf = wave.open(filename, 'rb')
        self.stream = self.audio.open(
            format=self.audio.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.wf.getframerate(),
            output=True,
            stream_callback=self.callback
        )
        print("* playing")
        data = self.wf.readframes(self.chunk)
        self.stream.start_stream()

    def stop_playing(self):
        print("* done playing")
        self.stream.stop_stream()

    def callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(self.chunk)
        return (data, pyaudio.paContinue)

    def terminate(self):
        while self.stream.is_active():
            time.sleep(0.1)
        self.audio.terminate()


@hydra.main(config_path="../conf/", config_name="conf")
def main(conf: Config):
    record = AudioPlayer(conf)
    record.start_playing(os.path.join(
        get_original_cwd(), './recordings/1648754506.wav'))
    record.terminate()


if __name__ == "__main__":
    main()
