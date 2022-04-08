import hydra
from hydra.core.config_store import ConfigStore

from src.config import Config

cs = ConfigStore.instance()
cs.store(name="config", node=Config)


class HydraClassTest:
    def __init__(self, conf: Config):
        print(conf)


def merge_and_sort_lists(list1, list2):
    return sorted(list(set(list1 + list2)))


@hydra.main(config_path="../src/conf/", config_name="conf")
def main(conf: Config):
    HydraClassTest(conf)


if __name__ == "__main__":
    main()
