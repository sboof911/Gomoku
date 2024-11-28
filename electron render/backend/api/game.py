from flask import request, jsonify
from flask_cors import cross_origin
from server import app, game_manager_module, game_manager, settings_module

@app.route('/api/game/init', methods=['POST'])
@cross_origin()
def initilize_game():
    global game_manager_module
    try:
        data = request.get_json()
        game_manager_module = game_manager(settings_module, data["isAI"])
        return jsonify({"message": "success"})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/api/game/delete', methods=['POST'])
@cross_origin()
def delete_game():
    global game_manager_module
    try:
        game_manager_module = None
        return jsonify({"message": "success"})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/api/game/move', methods=['POST'])
@cross_origin()
def move():
    global game_manager_module
    try:
        data = request.get_json()
        played = game_manager_module.play_turn(data["x"], data["y"])
        return jsonify({"played": played})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/api/game/board', methods=['GET'])
@cross_origin()
def get_board():
    global game_manager_module
    try:
        return jsonify({"message": game_manager_module.board.tolist()})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/api/game/turns', methods=['GET'])
@cross_origin()
def get_turn():
    global game_manager_module
    try:
        return jsonify({"message": game_manager_module.turn})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/api/game/currentPlayer', methods=['GET'])
@cross_origin()
def get_current_player():
    global game_manager_module
    try:
        return jsonify({"message": game_manager_module.current_player_index})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/api/game/captured', methods=['GET'])
@cross_origin()
def get_peercaptured():
    global game_manager_module
    try:
        player1_captured = game_manager_module.player1_captured
        player2_captured = game_manager_module.player2_captured
        return jsonify({"message": [player1_captured, player2_captured]})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/api/game/players_name', methods=['GET'])
@cross_origin()
def get_names():
    global game_manager_module
    try:
        return jsonify({"message": [game_manager_module.player1_name, game_manager_module.player2_name]})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/api/game/best_move', methods=['GET'])
@cross_origin()
def get_best_moves():
    global game_manager_module

    try:
        best_move = game_manager_module.best_move()
        return jsonify({"x": best_move[0], "y": best_move[1]})
    except Exception as e:
        return jsonify({"message": str(e)}), 400