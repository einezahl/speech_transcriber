import tkinter as tk
import uuid


class Model:
	recordings = []

class Controller:
	def __init__(self, model, view) -> None:
		self.model = model
		self.view = view

	def start(self):
		self.view.setup(self)
		self.view.start_main_loop()

	def start_recording(self):
		self.model.recordings.append(uuid.uuid4())
		self.view.append_to_list(self.model.recordings[-1])
	
	def end_recording(self):
		self.view.clear_list()
		self.model.recordings = []

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
		self.end_recording_button = tk.Button(self.frame_buttons, text="End Recording", command=controller.end_recording)
		self.end_recording_button.pack()
		self.play_recording_button = tk.Button(self.frame_buttons, text="Play Recording", command=controller.end_recording)
		self.play_recording_button.pack()
		self.delete_recording_button = tk.Button(self.frame_buttons, text="Delete Recording", command=controller.end_recording)
		self.delete_recording_button.pack()

	def append_to_list(self, item):
		self.list.insert(tk.END, item)

	def clear_list(self):
		self.list.delete(0, tk.END)

	def start_main_loop(self):
		self.root.mainloop()


if __name__=="__main__":
	c = Controller(Model(), TkView())
	c.start()