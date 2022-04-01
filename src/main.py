import tkinter as tk
import hydra
from hydra.core.config_store import ConfigStore
from hydra.utils import get_original_cwd
import os

from src.api.audio_transcriber import AudioTranscriber
from src.audio.audio_recorder import AudioRecorder
from src.audio.audio_player import AudioPlayer
from src.config import Config
from src.gui.model import Model
from src.gui.controller import Controller
from src.gui.tkview import TkView

cs = ConfigStore.instance()
cs.store(name="config", node=Config)

@hydra.main(config_path="./conf/", config_name="conf")
def main(conf: Config):
	if not os.path.exists(os.path.join(get_original_cwd(), conf.paths.recording_folder)):
		os.makedirs(os.path.join(get_original_cwd(), conf.paths.recording_folder))
	if not os.path.exists(os.path.join(get_original_cwd(), conf.paths.transcript_folder)):
		os.makedirs(os.path.join(get_original_cwd(), conf.paths.transcript_folder))

	model = Model()
	view = TkView()
	audio_recorder = AudioRecorder(conf)
	audio_player = AudioPlayer(conf)
	audio_transcriber = AudioTranscriber(conf)
	
	controller = Controller(audio_recorder, audio_player, audio_transcriber, model, view, conf)
	controller.start()
	audio_recorder.terminate()
	audio_player.terminate()

if __name__=="__main__":
	main()