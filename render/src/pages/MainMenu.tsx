import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, Bot, Settings as SettingsIcon } from 'lucide-react';

export default function MainMenu() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="bg-white/10 backdrop-blur-lg p-8 rounded-2xl shadow-2xl w-full max-w-md">
        <h1 className="text-4xl font-bold text-center mb-8 text-white">Gomoku</h1>
        <div className="space-y-4">
          <button
            onClick={() => navigate('/pvp')}
            className="w-full flex items-center justify-center gap-3 bg-indigo-600 hover:bg-indigo-700 text-white py-4 px-6 rounded-lg text-lg font-semibold transition-colors"
          >
            <Users className="w-6 h-6" />
            Player vs Player
          </button>
          <button
            onClick={() => navigate('/ai')}
            className="w-full flex items-center justify-center gap-3 bg-purple-600 hover:bg-purple-700 text-white py-4 px-6 rounded-lg text-lg font-semibold transition-colors"
          >
            <Bot className="w-6 h-6" />
            Player vs AI
          </button>
          <button
            onClick={() => navigate('/settings')}
            className="w-full flex items-center justify-center gap-3 bg-gray-600 hover:bg-gray-700 text-white py-4 px-6 rounded-lg text-lg font-semibold transition-colors"
          >
            <SettingsIcon className="w-6 h-6" />
            Settings
          </button>
        </div>
      </div>
    </div>
  );
}