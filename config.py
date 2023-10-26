import yaml


class Config:
    def __init__(self) -> None:
        self.read_config()
        self.validate()

    def read_config(self) -> None:
        # read config from config.yaml file
        with open("config.yaml", "r") as f:
            self.config = yaml.safe_load(f)

    def validate(self) -> bool:
        # check if config is valid
        photprism_config = (
            self.config["photoprism"]
            and self.config["photoprism"]["base_url"]
            and self.config["photoprism"]["username"]
            and self.config["photoprism"]["password"]
        )
        immich_config = (
            self.config["immich"]
            and self.config["immich"]["base_url"]
            and self.config["immich"]["api_key"]
        )
        if not (photprism_config and immich_config):
            raise ValueError("Please set all config parameters.")
