import tkinter as tk

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
		self.start_stop_recording_button = tk.Button(self.frame_buttons, text="Start Recording", command=controller.start_recording)
		self.start_stop_recording_button.pack()
		self.delete_recording_button = tk.Button(self.frame_buttons, text="Delete Recording", command=controller.delete_recording)
		self.delete_recording_button.pack()
		self.play_recording_button = tk.Button(self.frame_buttons, text="Play Recording", command=controller.play_recording)
		self.play_recording_button.pack()

	def append_to_list(self, item):
		self.list.insert(tk.END, item)

	def clear_list(self):
		self.list.delete(0, tk.END)

	def start_main_loop(self):
		self.root.mainloop()