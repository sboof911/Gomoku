from flask import request, jsonify, Blueprint
from srcs.settings.settings import settings

settings_module = settings()
settings_blueprint = Blueprint('settings', __name__)

@settings_blueprint.route('/api/settings/difficulty/<difficulty>', methods=['POST'])
def set_difficulty(difficulty):
    try:
        global settings_module
        if settings_module is None:
            return jsonify({"message": "Settings not initialized"}), 400
        setattr(settings_module, "difficulty_level", difficulty)
        return jsonify({"message": "success"})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@settings_blueprint.route('/api/settings/<player>', methods=['POST'])
def set_player(player):
    global settings_module
    players = ["player1", "player2", "AIName"]
    if player in players:
        data = request.get_json()
        try:
            setattr(settings_module, player, data[player])
            return jsonify({"message": "success"})
        except Exception as e:
            return jsonify({"message": str(e)}), 400
    else:
        return jsonify({"message": "Player not found"}), 400


@settings_blueprint.route('/api/settings/<setting>', methods=['GET'])
def get_setting(setting):
    print(setting)
    global settings_module
    settings = ["player1", "player2", "AIName", "difficulty", "rules"]
    if setting in settings:
        return jsonify({"message": getattr(settings_module, setting)})
    else:
        return jsonify({"message": "Player not found"}), 400
