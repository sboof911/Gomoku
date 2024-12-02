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

export default function PlayerVsPlayer() {
  const navigate = useNavigate();
  const [player1Name, setPlayer1NameState] = useState('');
  const [player2Name, setPlayer2NameState] = useState('');
  const [board, setBoard] = useState<number[][]>(Array(19).fill(0).map(() => Array(19).fill(0)));
  const [currentPlayer, setCurrentPlayer] = useState<1 | 2>(1);
  const [turns, setTurns] = useState(1);
  const [player1Time, setPlayer1Time] = useState(0);
  const [player2Time, setPlayer2Time] = useState(0);
  const [captured1, setCaptured1] = useState(0);
  const [captured2, setCaptured2] = useState(0);
  const [showHints1, setShowHints1] = useState(false);
  const [showHints2, setShowHints2] = useState(false);
  const [bestMoveX, setBestMoveX] = useState<number | null>(null);
  const [bestMoveY, setBestMoveY] = useState<number | null>(null);
  const [winner, setWinner] = useState<string | null>(null);
  const [winningLine, setWinningLine] = useState<WinningLine>(null);
  const [lastMoveTime, setLastMoveTime] = useState<number>(Date.now());
  const [showWinnerModal, setShowWinnerModal] = useState(false);


  const initializeGame = async () => {
    try {
      const response = await axios.post(`${config.serverUrl}/api/game/init`,
                              { isAI: false },
                              { headers: config.headers_data });
      console.log('Game initialized:', response.data.message);
    } catch (error) {
      console.error('Error initializing game:', error);
    }

    await get_board();
    await set_CurrentPlayer();
    await set_Turns();
    await set_Peer_Captured();
    await get_Players_Name();
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
          setPlayer1Time(elapsed);
        } else {
          setPlayer2Time(elapsed);
        }
      }
    }, 100);

    return () => clearInterval(timer);
  }, [currentPlayer, winner, lastMoveTime]);


  useEffect(() => {
    if (!winner) {
      if ((currentPlayer === 1 && showHints1) || (currentPlayer === 2 && showHints2)) {
        findBestMove();
      }
    }
  }, [showHints1, showHints2, currentPlayer]);


  const findBestMove = async () => {
    if (winner) return null;
    if (bestMoveX === null || bestMoveY === null) {
        if ((currentPlayer === 1 && showHints1) || (currentPlayer === 2 && showHints2)) {
          try {
            const response = await axios.get(`${config.serverUrl}/api/game/best_move`, { headers: config.headers_data });
            setBestMoveX(response.data.x);
            setBestMoveY(response.data.y);
            console.log('Best move:', response.data.x, response.data.y);
          } catch (error) {
            console.error('Error fetching best move:', error);
          }
        }
      }
  }

  const getHintPosition = (): [number, number] | null => {
    if (bestMoveX !== null && bestMoveY !== null) {
      return [bestMoveY, bestMoveX];
    }
    return null;
  };

  const handleCellClick = (row: number, col: number) => {
    if (winner) return;
    axios.post(`${config.serverUrl}/api/game/move`, { x: col, y: row }, { headers: config.headers_data })
    .then(async response => {
      if (response.data.played) {
        get_board();
        set_Peer_Captured();
        set_Turns();
        setBestMoveX(null);
        setBestMoveY(null);
        if (await checkWinner() === false) {
          set_CurrentPlayer();
          setPlayer1Time(0);
          setPlayer2Time(0);
          setLastMoveTime(Date.now());
          }
      } else {
        toast.error('Invalid move');
      }
    })
    .catch(error => {
      toast.error('Error making move:', error.response.data.message);
    });
  };

  const checkWinner = async () => {
    try {
      const response = await axios.get(`${config.serverUrl}/api/game/winner`, {headers : config.headers_data});
      if (response.data.message !== null) {
        setWinner(response.data.message.winner_name);
        setWinningLine(response.data.message.winning_line);
        return true;
      }
    } catch (error) {
      console.error('Error fetching winner:', error);
    }
    return false;
  }

  const get_Players_Name = async () => {
    try {
      const response = await axios.get(`${config.serverUrl}/api/game/players_name`, {headers : config.headers_data});
      setPlayer1NameState(response.data.message[0]);
      setPlayer2NameState(response.data.message[1]);
    } catch (error) {
      console.error('Error fetching players name:', error);
    }
  }

  const set_Peer_Captured = async () => {
    try {
      const response = await axios.get(`${config.serverUrl}/api/game/captured`, {headers : config.headers_data});
      setCaptured1(response.data.message[0]);
      setCaptured2(response.data.message[1]);
    } catch (error) {
      console.error('Error fetching captured:', error);
    }
  }

  const set_Turns = async () => {
    try {
      const response = await axios.get(`${config.serverUrl}/api/game/turns`, {headers : config.headers_data});
      setTurns(response.data.message);
    } catch (error) {
      console.error('Error fetching turns:', error);
    }
  }

  const set_CurrentPlayer = async () => {
    try {
      const response = await axios.get(`${config.serverUrl}/api/game/currentPlayer`, {headers : config.headers_data});
      setCurrentPlayer(response.data.message + 1);
    } catch (error) {
      console.error('Error fetching current player:', error);
    }
  }

  const get_board = async () => {
    try {
      const response = await axios.get(`${config.serverUrl}/api/game/board`, {headers : config.headers_data});
      setBoard(response.data.message);
    } catch (error) {
      console.error('Error fetching board:', error);
    }
  }

  const handleNewGame = async () => {
      initializeGame()
      setPlayer1Time(0);
      setPlayer2Time(0);
      setWinner(null);
      setLastMoveTime(Date.now());
      setWinningLine(null);
      setShowWinnerModal(false);
  };

  const handleBackToMenu = async () => {
    try {
      await axios.post(`${config.serverUrl}/api/game/delete`, {}, { headers: config.headers_data });
      navigate('/');
    } catch (error) {
      console.error('Error deleting game:', error);
      toast.error('Error deleting game');
    }
  };

  return (
    <div className="min-h-screen p-8">
      <button
        onClick={() => handleBackToMenu()}
        className="absolute top-4 left-4 text-white hover:text-gray-300 flex items-center gap-2"
      >
        <ArrowLeft className="w-6 h-6" />
        Back to Menu
      </button>

      <div className={`flex items-center justify-center gap-8 max-w-7xl mx-auto ${showWinnerModal ? 'blur-sm' : ''}`}>
        <PlayerInfo
          name={player1Name}
          captured={captured1}
          time={player1Time}
          isCurrentTurn={currentPlayer === 1}
          showHints={showHints1}
          onToggleHints={() => setShowHints1(prev => !prev)}
        />

        <div className="flex flex-col items-center">
          <div className="mb-4 px-6 py-2 bg-white/10 backdrop-blur rounded-full">
            <span className="text-xl font-bold text-white">Turn {turns}</span>
          </div>
          <Board 
            board={board} 
            onCellClick={handleCellClick} 
            hintPosition={getHintPosition()}
            winningLine={winningLine}
          />
        </div>

        <PlayerInfo
          name={player2Name}
          captured={captured2}
          time={player2Time}
          isCurrentTurn={currentPlayer === 2}
          showHints={showHints2}
          onToggleHints={() => setShowHints2(prev => !prev)}
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