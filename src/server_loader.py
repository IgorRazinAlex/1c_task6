import json


class ServerLoader:
    def __init__(self, path):
        self.host, self.port = None, None
        self.load_server(path)

    def load_server(self, path):
        with open(path, "r") as file:
            server_data = json.load(file)

        self.host, self.port = server_data["host"], server_data["port"]
