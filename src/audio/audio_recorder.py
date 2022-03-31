import hydra
from hydra.core.config_store import ConfigStore
from hydra.utils import get_original_cwd
import os
import pyaudio
import time
import wave

from src.config import RecordingConfig

cs = ConfigStore.instance()
cs.store(name="recording_config", node=RecordingConfig)

class AudioRecorder:
    def __init__(self, conf: RecordingConfig):
        self.conf = conf
        self.audio = pyaudio.PyAudio()
        self.sample_format = conf.rec_params.sample_format
        self.channel = conf.rec_params.channels
        self.rate = conf.rec_params.fs
        self.chunk = conf.rec_params.chunk
        self.duration = conf.rec_params.duration

    def start_recording(self):
        self.stream = self.audio.open(
            format=self.sample_format,
            channels=self.channel,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self.callback
        )
        print("* recording")
        self.frames = []
        self.stream.start_stream()

    def callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        print("* done recording")
    
    def save_recording(self, filename):
        filename = f"{filename}.wav"
        filepath = os.path.join(get_original_cwd(), self.conf.paths.recording_folder, filename)

        waveFile = wave.open(filepath, 'wb')
        waveFile.setnchannels(self.conf.rec_params.channels)
        waveFile.setsampwidth(self.audio.get_sample_size(self.conf.rec_params.sample_format))
        waveFile.setframerate(self.conf.rec_params.fs)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()

    def terminate(self):
        self.audio.terminate()


@hydra.main(config_path="../src/conf/", config_name="conf")
def main(conf: RecordingConfig):
    record = AudioRecorder(conf)
    record.start_recording()

    time.sleep(record.duration)

    record.stop_recording()
    record.save_recording(conf)

if __name__ == "__main__":
    main()