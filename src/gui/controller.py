import imp
from hydra.utils import get_original_cwd
import os
import time


class Controller:
	def __init__(self, recorder, player, model, view, conf) -> None:
		self.recorder = recorder
		self.player = player
		self.model = model
		self.view = view
		self.conf = conf
		self.recordings_folder = os.path.join(get_original_cwd(), conf.paths.recording_folder)

	def start(self):
		self.view.setup(self)
		recordings = [recording.split(".")[0] for recording in os.listdir(self.recordings_folder)]
		for recording in recordings:
			self.view.append_to_list(recording)
			self.model.recordings.append(recording)
		self.view.start_main_loop()

	def start_recording(self):
		self.recorder.start_recording()
		self.view.start_stop_recording_button.config(text="Stop Recording")
		self.view.start_stop_recording_button.config(command=self.stop_recording)
	
	def stop_recording(self):
		self.recorder.stop_recording()
		filename = str(int(time.time()))
		self.recorder.save_recording(filename)
		self.model.recordings.append(filename)
		self.view.append_to_list(filename)
		self.view.start_stop_recording_button.config(text="Start Recording")
		self.view.start_stop_recording_button.config(command=self.start_recording)

	def delete_recording(self):
		selected_recordings = self.view.list.curselection()
		if len(selected_recordings) > 0:
			for recording in selected_recordings:
				filename = self.model.recordings[recording]
				self.model.recordings.remove(self.model.recordings[recording])
				self.view.list.delete(recording)
				filepath = os.path.join(self.recordings_folder, filename) 
				filepath = filepath + ".wav"
				if os.path.exists(filepath):
					os.remove(filepath)

	def play_recording(self):
		selected_recordings = self.view.list.curselection()
		if len(selected_recordings) > 0:
			for recording in selected_recordings:
				filename = self.model.recordings[recording]
				filepath = os.path.join(self.recordings_folder, filename)
				filepath = filepath + ".wav"
				self.player.start_playing(filepath)