import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Board from '../components/Board';
import PlayerInfo from '../components/PlayerInfo';
import { useGame } from '../context/GameContext';
import { ArrowLeft } from 'lucide-react';

export default function PlayerVsAI() {
  const navigate = useNavigate();
  const { player1Name, aiName, difficulty } = useGame();
  const [board, setBoard] = useState<number[][]>(Array(19).fill(0).map(() => Array(19).fill(0)));
  const [currentPlayer, setCurrentPlayer] = useState<1 | 2>(1);
  const [turns, setTurns] = useState(1);
  const [playerTime, setPlayerTime] = useState(0);
  const [aiTime, setAiTime] = useState(0);
  const [playerCaptured, setPlayerCaptured] = useState(0);
  const [aiCaptured, setAiCaptured] = useState(0);

  useEffect(() => {
    let startTime = Date.now();
    const timer = setInterval(() => {
      const elapsed = (Date.now() - startTime) / 1000;
      if (currentPlayer === 1) {
        setPlayerTime(prev => prev + elapsed);
      } else {
        setAiTime(prev => prev + elapsed);
      }
      startTime = Date.now();
    }, 100);

    return () => clearInterval(timer);
  }, [currentPlayer]);

  const makeAiMove = () => {
    const emptyCells = [];
    for (let i = 0; i < 19; i++) {
      for (let j = 0; j < 19; j++) {
        if (board[i][j] === 0) {
          emptyCells.push([i, j]);
        }
      }
    }

    if (emptyCells.length > 0) {
      const [row, col] = emptyCells[Math.floor(Math.random() * emptyCells.length)];
      const newBoard = board.map(r => [...r]);
      newBoard[row][col] = 2;
      setBoard(newBoard);
      setCurrentPlayer(1);
      setTurns(t => t + 1);
    }
  };

  useEffect(() => {
    if (currentPlayer === 2) {
      const timeout = setTimeout(makeAiMove, 1000);
      return () => clearTimeout(timeout);
    }
  }, [currentPlayer, board]);

  const handleCellClick = (row: number, col: number) => {
    if (currentPlayer !== 1 || board[row][col] !== 0) return;

    const newBoard = board.map(r => [...r]);
    newBoard[row][col] = 1;
    setBoard(newBoard);
    setCurrentPlayer(2);
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
          captured={playerCaptured}
          time={playerTime}
          isCurrentTurn={currentPlayer === 1}
        />

        <div className="flex flex-col items-center">
          <div className="mb-4 px-6 py-2 bg-white/10 backdrop-blur rounded-full">
            <span className="text-xl font-bold text-white">Turn {turns}</span>
          </div>
          <Board board={board} onCellClick={handleCellClick} />
        </div>

        <PlayerInfo
          name={aiName}
          captured={aiCaptured}
          time={aiTime}
          isCurrentTurn={currentPlayer === 2}
        />
      </div>
    </div>
  );
}