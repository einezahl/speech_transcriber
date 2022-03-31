import hydra
from hydra.core.config_store import ConfigStore

from src.config import RecordingConfig

cs = ConfigStore.instance()
cs.store(name="recording_config", node=RecordingConfig)


class HydraClassTest:
	def __init__(self, conf: RecordingConfig):
		print(conf)


@hydra.main(config_path="../src/conf/", config_name="conf")
def main(conf: RecordingConfig):
	HydraClassTest(conf)

if __name__ == "__main__":
	main()