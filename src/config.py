from dataclasses import dataclass

@dataclass
class RecParams:
	chunk: int
	sample_format: int
	channels: int
	fs: int
	seconds: int

@dataclass
class Paths:
	recording_folder: str

@dataclass
class RecordingConfig:
	paths: Paths
	rec_params: RecParams