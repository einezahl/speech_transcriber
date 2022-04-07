import os
from hydra.utils import get_original_cwd
from src.gui.main_window import MainWindow


class UiController:
    def __init__(self, recorder, player, transcriber, model, window: MainWindow, conf) -> None:
        self.recorder = recorder
        self.player = player
        self.transcriber = transcriber
        self.model = model
        self.window = window
        self.conf = conf
        self.recordings_folder = os.path.join(
            get_original_cwd(), conf.paths.recording_folder)
        self.transcript_folder = os.path.join(
            get_original_cwd(), conf.paths.transcript_folder)

    def start(self):
        self.window.initializeUI()
        recordings = [recording.split(
            ".")[0] for recording in os.listdir(self.recordings_folder)]
        for recording in recordings:
            self.window.append_to_list(recording)
            self.model.recordings.append(recording)
        self.window.show()
