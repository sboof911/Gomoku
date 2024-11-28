import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Board from '../components/Board';
import PlayerInfo from '../components/PlayerInfo';
import WinnerModal from '../components/WinnerModal';
import type { WinningLine } from '../types/game';
import { ArrowLeft } from 'lucide-react';
import axios from 'axios';
import config from '../Config';
import toast from 'react-hot-toast';

export default function PlayerVsAI() {
  const navigate = useNavigate();
  const [playerName, setPlayerNameState] = useState('');
  const [playerAIName, setPlayerAINameState] = useState('');
  const [board, setBoard] = useState<number[][]>(
    Array(19)
      .fill(0)
      .map(() => Array(19).fill(0))
  );
  const [currentPlayer, setCurrentPlayer] = useState<1 | 2>(1);
  const [AIPlayerIndex, setAIPlayerIndex] = useState(0);
  const [turns, setTurns] = useState(1);
  const [playerTime, setPlayerTime] = useState(0);
  const [aiTime, setAiTime] = useState(0);
  const [playerCaptured, setPlayerCaptured] = useState(0);
  const [aiCaptured, setAiCaptured] = useState(0);
  const [winner, setWinner] = useState<string | null>(null);
  const [winningLine, setWinningLine] = useState<WinningLine>(null);
  const [showWinnerModal, setShowWinnerModal] = useState(false);
  const [lastMoveTime, setLastMoveTime] = useState<number>(Date.now());

  const get_Players_Name = async () => {
    try {
      const response = await axios.get(
        `${config.serverUrl}/api/game/players_name`,
        { headers: config.headers_data }
      );
      setPlayerNameState(response.data.message[0]);
      setPlayerAINameState(response.data.message[1]);
    } catch (error) {
      console.error('Error fetching players name:', error);
    }
  };

  const get_AiPlayer_index = async () => {
    try {
      const response = await axios.get(
        `${config.serverUrl}/api/game/ai_player`,
        { headers: config.headers_data }
      );
      setAIPlayerIndex(response.data.message+1)
    } catch (error) {
      console.error('Error fetching ai index:', error);
    }
  }

  const set_Captured = async () => {
    try {
      const response = await axios.get(
        `${config.serverUrl}/api/game/captured`,
        { headers: config.headers_data }
      );
      setPlayerCaptured(response.data.message[0]);
      setAiCaptured(response.data.message[1]);
    } catch (error) {
      console.error('Error fetching captured:', error);
    }
  };

  const set_Turns = async () => {
    try {
      const response = await axios.get(`${config.serverUrl}/api/game/turns`, {
        headers: config.headers_data,
      });
      setTurns(response.data.message);
    } catch (error) {
      console.error('Error fetching turns:', error);
    }
  };

  const set_CurrentPlayer = async () => {
    try {
      const response = await axios.get(
        `${config.serverUrl}/api/game/currentPlayer`,
        { headers: config.headers_data }
      );
      setCurrentPlayer(response.data.message + 1);
    } catch (error) {
      console.error('Error fetching current player:', error);
    }
  };

  const get_board = async () => {
    try {
      const response = await axios.get(`${config.serverUrl}/api/game/board`, {
        headers: config.headers_data,
      });
      setBoard(response.data.message);
    } catch (error) {
      console.error('Error fetching board:', error);
    }
  };

  const checkWinner = async () => {
    try {
      const response = await axios.get(
        `${config.serverUrl}/api/game/winner`,
        { headers: config.headers_data }
      );
      if (response.data.message !== null) {
        setWinner(response.data.message.winner_name);
        setWinningLine(response.data.message.winning_line);
        return true;
      }
    } catch (error) {
      console.error('Error fetching winner:', error);
    }
    return false;
  };

  const initializeGame = async () => {
    try {
      const response = await axios.post(
        `${config.serverUrl}/api/game/init`,
        { isAI: true },
        { headers: config.headers_data }
      );
      console.log('Game initialized:', response.data.message);
    } catch (error) {
      console.error('Error initializing game:', error);
    }

    await get_board();
    await set_CurrentPlayer();
    await set_Turns();
    await set_Captured();
    await get_Players_Name();
    await get_AiPlayer_index()
  };

  useEffect(() => {
    initializeGame();
  }, []);

  useEffect(() => {
    if (winner) {
      setShowWinnerModal(true);
    }
  }, [winner]);

  useEffect(() => {
    const timer = setInterval(() => {
      if (!winner) {
        const now = Date.now();
        const elapsed = (now - lastMoveTime) / 1000;
        if (currentPlayer === 1) {
          setPlayerTime(elapsed);
        } else {
          setAiTime(elapsed);
        }
      }
    }, 100);

    return () => clearInterval(timer);
  }, [currentPlayer, winner, lastMoveTime]);

  const findBestMove = async () => {
    if (winner) return null;
    try {
      const response = await axios.get(
        `${config.serverUrl}/api/game/best_move`,
        { headers: config.headers_data }
      );
      console.log('Best move:', response.data.x, response.data.y);
      return [response.data.x, response.data.y];
    } catch (error) {
      console.error('Error fetching best move:', error);
      return null;
    }
  };

  const makeAiMove = async () => {
    if (winner) return;

    const bestMove = await findBestMove();
    if (!bestMove) return;
    const [x, y] = bestMove;

    try {
      const response = await axios.post(
        `${config.serverUrl}/api/game/move`,
        { x: x, y: y },
        { headers: config.headers_data }
      );
      if (response.data.played) {
        await get_board();
        await set_Captured();
        await set_Turns();
        if ((await checkWinner()) === false) {
          await set_CurrentPlayer();
          setPlayerTime(0);
          setAiTime(0);
          setLastMoveTime(Date.now());
        }
      } else {
        toast.error('Invalid move');
      }
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        toast.error(`Error making move: ${error.response.data.message}`);
      } else {
        toast.error('Error making move');
      }
    }
  };

  useEffect(() => {
    if (currentPlayer === AIPlayerIndex && !winner) {
      const timeout = setTimeout(makeAiMove, 1000);
      return () => clearTimeout(timeout);
    }
  }, [currentPlayer, winner, AIPlayerIndex]);

  const handleCellClick = (row: number, col: number) => {
    if (currentPlayer === AIPlayerIndex || winner) return;

    axios
      .post(
        `${config.serverUrl}/api/game/move`,
        { x: col, y: row },
        { headers: config.headers_data }
      )
      .then(async (response) => {
        if (response.data.played) {
          await get_board();
          await set_Captured();
          await set_Turns();
          if ((await checkWinner()) === false) {
            await set_CurrentPlayer();
            setPlayerTime(0);
            setAiTime(0);
            setLastMoveTime(Date.now());
          }
        } else {
          toast.error('Invalid move');
        }
      })
      .catch((error) => {
        if (axios.isAxiosError(error) && error.response) {
          toast.error(`Error making move: ${error.response.data.message}`);
        } else {
          toast.error('Error making move');
        }
      });
  };

  const handleNewGame = async () => {
    await initializeGame();
    setPlayerTime(0);
    setAiTime(0);
    setWinner(null);
    setLastMoveTime(Date.now());
    setWinningLine(null);
    setShowWinnerModal(false);
  };

  const handleBackToMenu = async () => {
    try {
      await axios.post(
        `${config.serverUrl}/api/game/delete`,
        {},
        { headers: config.headers_data }
      );
      navigate('/');
    } catch (error) {
      console.error('Error deleting game:', error);
      toast.error('Error deleting game');
    }
  };

  return (
    <div className="min-h-screen p-8">
      <button
        onClick={handleBackToMenu}
        className="absolute top-4 left-4 text-white hover:text-gray-300 flex items-center gap-2"
      >
        <ArrowLeft className="w-6 h-6" />
        Back to Menu
      </button>

      <div
        className={`flex items-center justify-center gap-8 max-w-7xl mx-auto ${
          showWinnerModal ? 'blur-sm' : ''
        }`}
      >
        <PlayerInfo
          name={playerName}
          captured={playerCaptured}
          time={playerTime}
          isCurrentTurn={currentPlayer === 1}
          showHints={false}
          onToggleHints={() => {}}
          hideHints={true}
        />

        <div className="flex flex-col items-center">
          <div className="mb-4 px-6 py-2 bg-white/10 backdrop-blur rounded-full">
            <span className="text-xl font-bold text-white">
              Turn {turns}
            </span>
          </div>
          <Board
            board={board}
            onCellClick={handleCellClick}
            hintPosition={null}
            winningLine={winningLine}
          />
        </div>

        <PlayerInfo
          name={playerAIName}
          captured={aiCaptured}
          time={aiTime}
          isCurrentTurn={currentPlayer === 2}
          showHints={false}
          onToggleHints={() => {}}
          hideHints={true}
        />
      </div>

      {showWinnerModal && winner && (
        <WinnerModal
          winner={winner}
          onNewGame={handleNewGame}
          onMainMenu={() => navigate('/')}
          onClose={() => setShowWinnerModal(false)}
        />
      )}
    </div>
  );
}