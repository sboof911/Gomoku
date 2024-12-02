import React from 'react';
import { Trophy, RotateCcw, Home, X } from 'lucide-react';

interface WinnerModalProps {
  winner: string;
  onNewGame: () => void;
  onMainMenu: () => void;
  onClose: () => void;
}

export default function WinnerModal({ winner, onNewGame, onMainMenu, onClose }: WinnerModalProps) {
  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-8 shadow-2xl max-w-md w-full mx-4 animate-fade-in relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-500 hover:text-gray-700 transition-colors"
          aria-label="Close modal"
        >
          <X className="w-6 h-6" />
        </button>
        
        <div className="flex flex-col items-center text-center">
          <Trophy className="w-16 h-16 text-yellow-500 mb-4" />
          <h2 className="text-3xl font-bold text-gray-800 mb-2">Congratulations!</h2>
          <p className="text-xl text-gray-600 mb-8">{winner} wins!</p>
          
          <div className="grid grid-cols-2 gap-4 w-full">
            <button
              onClick={onNewGame}
              className="flex items-center justify-center gap-2 bg-indigo-600 text-white py-3 px-6 rounded-lg hover:bg-indigo-700 transition-colors"
            >
              <RotateCcw className="w-5 h-5" />
              New Game
            </button>
            <button
              onClick={onMainMenu}
              className="flex items-center justify-center gap-2 bg-gray-600 text-white py-3 px-6 rounded-lg hover:bg-gray-700 transition-colors"
            >
              <Home className="w-5 h-5" />
              Main Menu
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}