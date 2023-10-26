import yaml

class Config:
    def __init__(self) -> None:
        self.read_config()
        self.validate()
        

    def read_config(self) -> None:
        # read config from config.yaml file
        with open("config.yaml.example", "r") as f:
            self.config = yaml.safe_load(f)

    def validate(self) -> bool:
        # check if config is valid
        if (False):
            raise ValueError("Please set all environment variables.")