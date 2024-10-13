import os
from src.server_loader import ServerLoader
from src.app import App

if __name__ == '__main__':
    server = ServerLoader(os.path.join("static", "json", "server_data.json"))
    app = App(__name__).get_app()
    app.run(server.host, server.port)
