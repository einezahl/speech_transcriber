import tkinter as tk
import uuid
import hydra
from hydra.core.config_store import ConfigStore

from src.audio.record_audio import RecordAudio
from src.config import RecordingConfig

cs = ConfigStore.instance()
cs.store(name="recording_config", node=RecordingConfig)

class Model:
	recordings = []

class Controller:
	def __init__(self, recorder, model, view) -> None:
		self.recorder = recorder
		self.model = model
		self.view = view

	def start(self):
		self.view.setup(self)
		self.view.start_main_loop()

	def start_recording(self):
		self.recorder.start_recording()
	
	def stop_recording(self):
		self.recorder.stop_recording()
	
	def save_recording(self):
		self.recorder.save_recording()

class TkView:
	def setup(self, controller):
		self.root = tk.Tk()
		self.root.geometry("400x400")
		self.root.title("Voice Message Transcriber")

		self.frame = tk.Frame(self.root)
		self.frame.pack(fill=tk.BOTH, expand=1)
		self.label = tk.Label(self.frame, text="Recording")
		self.label.pack()
		self.list = tk.Listbox(self.frame)
		self.list.pack(fill=tk.BOTH, expand=1)
		self.frame_buttons = tk.Frame(self.frame)
		self.frame_buttons.pack(fill=tk.BOTH, expand=1)
		self.start_recording_button = tk.Button(self.frame_buttons, text="Start Recording", command=controller.start_recording)
		self.start_recording_button.pack()
		self.stop_recording_button = tk.Button(self.frame_buttons, text="Stop Recording", command=controller.stop_recording)
		self.stop_recording_button.pack()
		self.save_recording_button = tk.Button(self.frame_buttons, text="Save Recording", command=controller.save_recording)
		self.save_recording_button.pack()
		# self.play_recording_button = tk.Button(self.frame_buttons, text="Save Recording", command=controller.end_recording)
		# self.play_recording_button.pack()
		# self.delete_recording_button = tk.Button(self.frame_buttons, text="Delete Recording", command=controller.end_recording)
		# self.delete_recording_button.pack()

	def append_to_list(self, item):
		self.list.insert(tk.END, item)

	def clear_list(self):
		self.list.delete(0, tk.END)

	def start_main_loop(self):
		self.root.mainloop()

@hydra.main(config_path="../conf/", config_name="conf")
def main(conf: RecordingConfig):
	model = Model()
	view = TkView()
	controller = Controller(RecordAudio(conf), model, view)
	controller.start()

if __name__=="__main__":
	main()