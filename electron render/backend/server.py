import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from srcs.settings.settings import settings
from srcs.game.game_manager import game_manager
import logging


settings_module = settings()
game_manager_module : game_manager = None

app = Flask(__name__)

app.config['DEBUG'] = True

# Configure logging
logging.basicConfig(level=logging.DEBUG)

from api.settings import *
from api.game import *

def main():
    app.run(port=5000)

if __name__ == '__main__':
    main()