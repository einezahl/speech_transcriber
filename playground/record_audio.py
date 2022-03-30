import asyncio
import hydra
from hydra.core.config_store import ConfigStore
from hydra.utils import get_original_cwd
import os
import pyaudio
import wave

from src.config import RecordingConfig

cs = ConfigStore.instance()
cs.store(name="recording_config", node=RecordingConfig)

class RecordAudio:
    def __init__(self, conf: RecordingConfig):
        self.audio = pyaudio.PyAudio()
        self.sample_format = conf.rec_params.sample_format
        self.channel = conf.rec_params.channels
        self.rate = conf.rec_params.fs
        self.chunk = conf.rec_params.chunk
        self.seconds = conf.rec_params.seconds

    async def start_recording(self):
        self.stream = self.audio.open(
            format=self.sample_format,
            channels=self.channel,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        print("* recording")
        self.frames = []
        self.rec = True

        for _ in range(0, int(self.rate / self.chunk * self.seconds)):
            data = self.stream.read(self.chunk)
            self.frames.append(data)

        while self.rec:
            print("Sleeping for another second")
            await asyncio.sleep(1)
    
    def stop_recording(self):
        self.rec = False
    
    
    def save_recording(self, conf: RecordingConfig):
        filename = "output.wav"
        filepath = os.path.join(get_original_cwd(), conf.paths.recording_folder, filename)
        print("* done recording")
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        waveFile = wave.open(filepath, 'wb')
        waveFile.setnchannels(conf.rec_params.channels)
        waveFile.setsampwidth(self.audio.get_sample_size(conf.rec_params.sample_format))
        waveFile.setframerate(conf.rec_params.fs)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()

async def main(conf: RecordingConfig):
    record = RecordAudio(conf)
    loop = asyncio.get_event_loop()
    loop.create_task(record.start_recording())
    await asyncio.sleep(2)
    record.stop_recording()
    record.save_recording(conf)

@hydra.main(config_path="../src/conf/", config_name="conf")
def run(conf: RecordingConfig):
    asyncio.run(main(conf))

if __name__ == "__main__":
    run()