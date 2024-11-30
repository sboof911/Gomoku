from flask import Flask, send_from_directory
from flask_cors import CORS
import logging, os


app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = True

# Configure logging
logging.basicConfig(level=logging.DEBUG)

from api.settings import settings_blueprint
from api.game import game_blueprint

app.register_blueprint(settings_blueprint)
app.register_blueprint(game_blueprint)
dist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'render_dist')

# Route to serve the `index.html`
@app.route('/')
def serve_index():
    return send_from_directory(dist_dir, 'index.html')

# Route to serve other static files (CSS, JS, etc.)
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(dist_dir, path)

def main():
    app.run(port=5000)

if __name__ == '__main__':
    main()