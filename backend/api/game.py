from flask import request, jsonify, Blueprint
from srcs.game.game_manager import game_manager
import api.settings as settings

game_manager_module = None
settings_module = settings.settings_module
game_blueprint = Blueprint('game', __name__)

@game_blueprint.route('/api/game/init', methods=['POST'])
def initilize_game():
    global game_manager_module
    try:
        data = request.get_json()
        game_manager_module = game_manager(settings_module, data["isAI"])
        return jsonify({"message": "success"})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@game_blueprint.route('/api/game/delete', methods=['POST'])
def delete_game():
    global game_manager_module
    try:
        game_manager_module = None
        return jsonify({"message": "success"})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@game_blueprint.route('/api/game/move', methods=['POST'])
def move():
    global game_manager_module
    try:
        data = request.get_json()
        played = game_manager_module.play_turn(data["x"], data["y"])
        return jsonify({"played": played})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@game_blueprint.route('/api/game/board', methods=['GET'])
def get_board():
    global game_manager_module
    try:
        return jsonify({"message": game_manager_module.board.tolist()})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@game_blueprint.route('/api/game/turns', methods=['GET'])
def get_turn():
    global game_manager_module
    try:
        return jsonify({"message": game_manager_module.turn})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@game_blueprint.route('/api/game/currentPlayer', methods=['GET'])
def get_current_player():
    global game_manager_module
    try:
        return jsonify({"message": game_manager_module.current_player_index})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@game_blueprint.route('/api/game/captured', methods=['GET'])
def get_peercaptured():
    global game_manager_module
    try:
        player1_captured = game_manager_module.player1_captured
        player2_captured = game_manager_module.player2_captured
        return jsonify({"message": [player1_captured, player2_captured]})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@game_blueprint.route('/api/game/players_name', methods=['GET'])
def get_names():
    global game_manager_module
    try:
        return jsonify({"message": [game_manager_module.player1_name, game_manager_module.player2_name]})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@game_blueprint.route('/api/game/best_move', methods=['GET'])
def get_best_moves():
    global game_manager_module

    try:
        best_move = game_manager_module.best_move()
        return jsonify({"x": best_move[0], "y": best_move[1]})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@game_blueprint.route('/api/game/winner', methods=['GET'])
def get_winner_color():
    global game_manager_module
    try:
        if game_manager_module.is_game_over:
            kwargs = {
                "winning_line": {"start":[game_manager_module.line_pos_win["y0"], game_manager_module.line_pos_win["x0"]],
                                 "end":[game_manager_module.line_pos_win["y1"], game_manager_module.line_pos_win["x1"]]
                                 },
                "winner_name": game_manager_module.winner_name
            }
            return jsonify({"message": kwargs})
        else:
            return jsonify({"message": None})
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
@game_blueprint.route('/api/game/ai_player', methods=['GET'])
def get_ai_index_player():
    global game_manager_module
    try:
        return jsonify({"message": game_manager_module.AI_Player})
    except Exception as e:
        return jsonify({"message": str(e)}), 400
