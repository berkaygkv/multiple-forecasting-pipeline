from dataclasses import dataclass
import os

@dataclass
class ProjectConstants:
    ROOT_DIR: str = os.path.dirname(__file__).split("/src")[0]