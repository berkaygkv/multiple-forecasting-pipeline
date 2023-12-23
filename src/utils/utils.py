from .constants import ProjectConstants
from pathlib import Path
import yaml

class Utils:

    @staticmethod
    def list_providers():
        """ Reads model config YAML file and extracts all the providers given.
        """
        root_path = Path(ProjectConstants.ROOT_DIR)
        config_path = root_path.joinpath("config", "model_config.yaml")
        with open(config_path, "r") as rd:
            conf = yaml.safe_load(rd)
        return list(conf.keys())
            

if __name__ == "__main__":
    Utils.list_providers()