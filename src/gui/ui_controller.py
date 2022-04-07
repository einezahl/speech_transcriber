import os
import time
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
        recordings = [recording.split(
            ".")[0] for recording in os.listdir(self.recordings_folder)]
        for recording in recordings:
            self.window.append_to_list(recording)
            self.model.recordings.append(recording)
        self.connect_to_window()
        self.window.show()

    def connect_to_window(self):
        # this is a hack to connect the Controller to the main window
        # okay, so this is a hack, but it works
        # TODO: find a better way to do this
        # this is the comment line I wrote on my own ... function (all parts!!) as well as comments were suggested by copilot ...
        self.window.start_stop_recording_button.clicked.connect(
            self.start_recording)
        self.window.delete_recording_button.clicked.connect(
            self.delete_recording)
        self.window.play_recording_button.clicked.connect(
            self.play_recording)
        self.window.listWidget.itemClicked.connect(self.set_recording)
        self.window.transcribe_recording_button.clicked.connect(
            self.transcribe_recording)

    def start_recording(self):
        self.recorder.start_recording()
        self.window.start_stop_recording_button.setText("Stop Recording")
        self.window.start_stop_recording_button.clicked.disconnect(
            self.start_recording)
        self.window.start_stop_recording_button.clicked.connect(
            self.stop_recording)

    def stop_recording(self):
        self.recorder.stop_recording()
        filename = str(int(time.time()))
        self.recorder.save_recording(filename)
        self.model.recordings.append(filename)
        self.window.append_to_list(filename)
        self.window.start_stop_recording_button.setText("Start Recording")
        self.window.start_stop_recording_button.clicked.disconnect(
            self.stop_recording)
        self.window.start_stop_recording_button.clicked.connect(
            self.start_recording)

    def play_recording(self):
        if self.selected_recording:
            self.player.play_recording(self.filepath)

    def set_recording(self, recording):
        if recording:
            self.selected_recording = recording
            self.filepath = os.path.join(
                self.recordings_folder, f'{self.selected_recording.text()}.wav')
            # thanks to copilot for the hint to enable and disable buttons
            # thank you also for suggesting to thank you
            self.window.play_recording_button.setEnabled(True)
            self.transcript_path = os.path.join(
                self.transcript_folder, f'{self.selected_recording.text()}.txt')
            self.update_textBrowser()

    def update_textBrowser(self):
        try:
            with open(self.transcript_path, 'r') as f:
                self.transcribt_text = f.read()
        except OSError:
            self.transcribt_text = 'No transcript available...'
        finally:
            self.window.textBrowser.setText(self.transcribt_text)

    def transcribe_recording(self):
        if self.selected_recording:
            self.transcriber.run(self.selected_recording.text())
            self.update_textBrowser()

    # BUG: recording can not be deleted if it was played before (windows10) -> "file used by another process"
    # tried to terminate audio and stopped stream, but still can't delete file
    def delete_recording(self):
        if self.selected_recording:
            self.model.recordings.remove(self.selected_recording.text())
            self.window.remove_from_list(self.selected_recording)
            if os.path.exists(self.filepath):
                os.remove(self.filepath)
                pass
