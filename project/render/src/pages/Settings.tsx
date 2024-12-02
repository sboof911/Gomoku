import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useGame } from '../context/GameContext';
import { ArrowLeft, User, Bot, Zap } from 'lucide-react';

export default function Settings() {
  const navigate = useNavigate();
  const {
    player1Name,
    player2Name,
    aiName,
    difficulty,
    setPlayer1Name,
    setPlayer2Name,
    setAiName,
    setDifficulty,
  } = useGame();

  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <button
        onClick={() => navigate('/')}
        className="absolute top-4 left-4 text-white hover:text-gray-300 flex items-center gap-2"
      >
        <ArrowLeft className="w-6 h-6" />
        Back to Menu
      </button>

      <div className="bg-white/10 backdrop-blur-lg p-8 rounded-2xl shadow-2xl w-full max-w-md">
        <h2 className="text-3xl font-bold text-center mb-8 text-white">Settings</h2>

        <div className="space-y-6">
          <div className="space-y-4">
            <div className="relative">
              <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-indigo-300 w-5 h-5" />
              <input
                type="text"
                value={player1Name}
                onChange={(e) => setPlayer1Name(e.target.value)}
                placeholder="Player 1 Name"
                className="w-full bg-white/5 border border-indigo-300/20 rounded-lg py-3 pl-12 pr-4 text-white placeholder-indigo-300"
              />
            </div>

            <div className="relative">
              <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-purple-300 w-5 h-5" />
              <input
                type="text"
                value={player2Name}
                onChange={(e) => setPlayer2Name(e.target.value)}
                placeholder="Player 2 Name"
                className="w-full bg-white/5 border border-purple-300/20 rounded-lg py-3 pl-12 pr-4 text-white placeholder-purple-300"
              />
            </div>

            <div className="relative">
              <Bot className="absolute left-3 top-1/2 transform -translate-y-1/2 text-green-300 w-5 h-5" />
              <input
                type="text"
                value={aiName}
                onChange={(e) => setAiName(e.target.value)}
                placeholder="AI Player Name"
                className="w-full bg-white/5 border border-green-300/20 rounded-lg py-3 pl-12 pr-4 text-white placeholder-green-300"
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="flex items-center gap-2 text-white">
              <Zap className="w-5 h-5" />
              AI Difficulty
            </label>
            <div className="grid grid-cols-3 gap-2">
              {(['easy', 'medium', 'hard'] as const).map((level) => (
                <button
                  key={level}
                  onClick={() => setDifficulty(level)}
                  className={`py-2 px-4 rounded-lg font-medium transition-colors ${
                    difficulty === level
                      ? 'bg-indigo-600 text-white'
                      : 'bg-white/5 text-white/80 hover:bg-white/10'
                  }`}
                >
                  {level.charAt(0).toUpperCase() + level.slice(1)}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}