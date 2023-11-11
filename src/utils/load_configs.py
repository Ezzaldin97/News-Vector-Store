import yaml
from dotenv import dotenv_values

class Config:
    def __init__(self):
        with open("config.yml") as yml:
            self.conf = yaml.safe_load(yml)
        self.env = dotenv_values(".env")