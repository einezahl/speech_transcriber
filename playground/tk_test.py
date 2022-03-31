import tkinter as tk

class TkView:
	def setup(self, controller):
		self.root = tk.Tk()
		self.root.geometry("1200x400")
		self.root.title("Voice Message Transcriber")

		self.root.columnconfigure(0, weight=3)
		self.root.columnconfigure(1, weight=1)
		self.root.columnconfigure(2, weight=3)

		self.frame_left = tk.Frame(self.root)
		self.frame_left.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
		self.list = tk.Listbox(self.frame_left, height=380, width=380)
		self.list.grid(column=0, row=0)
		self.frame_left = tk.Frame(self.root)
		self.frame_left.grid(column=1, row=0)
		self.list = tk.Listbox(self.frame_left)
		self.list.pack(fill=tk.BOTH, expand=1)
		self.frame_left = tk.Frame(self.root)
		self.frame_left.grid(column=2, row=0)
		self.list = tk.Listbox(self.frame_left)
		self.list.pack(fill=tk.BOTH, expand=1)

	def append_to_list(self, item):
		self.list.insert(tk.END, item)

	def clear_list(self):
		self.list.delete(0, tk.END)

	def start_main_loop(self):
		self.root.mainloop()

class DummyController:
	def start_recording(self):
		print("Start Recording")

	def delete_recording(self):
		print("Delete Recording")

	def play_recording(self):
		print("Play Recording")

	def transcribe_recording(self):
		print("Transcribe Recording")

if __name__=="__main__":
	view = TkView()
	view.setup(DummyController())
	view.start_main_loop()