from flask import request, jsonify
from flask_cors import cross_origin
from server import app, settings_module


@app.route('/api/settings/difficulty/<difficulty>', methods=['POST'])
@cross_origin()
def set_difficulty(difficulty):
    try:
        setattr(settings_module, difficulty, difficulty)
        return jsonify({"message": "success"})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/api/settings/<player>', methods=['POST'])
@cross_origin()
def set_player(player):
    players = ["player1", "player2", "AIName"]
    if player in players:
        data = request.get_json()
        try:
            setattr(settings_module, player, data[player])
            return jsonify({"message": "success"})
        except Exception as e:
            return jsonify({"message": str(e)}), 400
    else:
        return jsonify({"message": "Player not found"}), 404


@app.route('/api/settings/<setting>', methods=['GET'])
@cross_origin()
def get_setting(setting):
    settings = ["player1", "player2", "AIName", "difficulty", "rules"]
    if setting in settings:
        return jsonify({"message": getattr(settings_module, setting)})
    else:
        return jsonify({"message": "Player not found"}), 404