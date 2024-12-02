import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Board from '../components/Board';
import PlayerInfo from '../components/PlayerInfo';
import { useGame } from '../context/GameContext';
import { ArrowLeft } from 'lucide-react';

export default function PlayerVsPlayer() {
  const navigate = useNavigate();
  const { player1Name, player2Name } = useGame();
  const [board, setBoard] = useState<number[][]>(Array(19).fill(0).map(() => Array(19).fill(0)));
  const [currentPlayer, setCurrentPlayer] = useState<1 | 2>(1);
  const [turns, setTurns] = useState(1);
  const [player1Time, setPlayer1Time] = useState(0);
  const [player2Time, setPlayer2Time] = useState(0);
  const [captured1, setCaptured1] = useState(0);
  const [captured2, setCaptured2] = useState(0);

  useEffect(() => {
    let startTime = Date.now();
    const timer = setInterval(() => {
      const elapsed = (Date.now() - startTime) / 1000;
      if (currentPlayer === 1) {
        setPlayer1Time(prev => prev + elapsed);
      } else {
        setPlayer2Time(prev => prev + elapsed);
      }
      startTime = Date.now();
    }, 100);

    return () => clearInterval(timer);
  }, [currentPlayer]);

  const handleCellClick = (row: number, col: number) => {
    if (board[row][col] !== 0) return;

    const newBoard = board.map(r => [...r]);
    newBoard[row][col] = currentPlayer;
    setBoard(newBoard);
    setCurrentPlayer(currentPlayer === 1 ? 2 : 1);
    setTurns(t => t + 1);
  };

  return (
    <div className="min-h-screen p-8">
      <button
        onClick={() => navigate('/')}
        className="absolute top-4 left-4 text-white hover:text-gray-300 flex items-center gap-2"
      >
        <ArrowLeft className="w-6 h-6" />
        Back to Menu
      </button>

      <div className="flex items-center justify-center gap-8 max-w-7xl mx-auto">
        <PlayerInfo
          name={player1Name}
          captured={captured1}
          time={player1Time}
          isCurrentTurn={currentPlayer === 1}
        />

        <div className="flex flex-col items-center">
          <div className="mb-4 px-6 py-2 bg-white/10 backdrop-blur rounded-full">
            <span className="text-xl font-bold text-white">Turn {turns}</span>
          </div>
          <Board board={board} onCellClick={handleCellClick} />
        </div>

        <PlayerInfo
          name={player2Name}
          captured={captured2}
          time={player2Time}
          isCurrentTurn={currentPlayer === 2}
        />
      </div>
    </div>
  );
}