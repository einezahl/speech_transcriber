from dataclasses import dataclass

@dataclass
class RecParams:
	chunk: int
	sample_format: int
	channels: int
	fs: int
	duration: int

@dataclass
class Paths:
	recording_folder: str
	transcript_folder: str

@dataclass
class TranscriptConfig:
	auth_key: str

@dataclass
class RecordingConfig:
	paths: Paths
	rec_params: RecParams
	trans_params: TranscriptConfig
