from flask import Flask, request, jsonify, g
from backend.game.game_manager import game_manager
from backend.settings.settings import settings


app = Flask(__name__)

@app.route('/api/settings/<player>', methods=['GET'])
def get_data(player):
    players = ["player1", "player2", "AIName"]
    if player in players:
        return jsonify({"message": player})
        return jsonify({"message": getattr(g.settings_module, player)})
    else:
        return jsonify({"message": "Player not found"}), 404

@app.route('/api/settings/<player>', methods=['POST'])
def set_data(player):
    players = ["player1", "player2", "AIName"]
    if player in players:
        data = request.get_json()
        try:
            # setattr(g.settings_module, player, data[player])
            return jsonify({"message": "success"})
        except Exception as e:
            return jsonify({"message": str(e)}), 400
    else:
        return jsonify({"message": "Player not found"}), 404

def main():
    with app.app_context():
        g.settings_module = settings()
    app.run(port=5000)

if __name__ == '__main__':
    main()