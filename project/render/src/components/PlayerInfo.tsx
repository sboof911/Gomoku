import React from 'react';
import { Timer, User } from 'lucide-react';

interface PlayerInfoProps {
  name: string;
  captured: number;
  time: number;
  isCurrentTurn: boolean;
}

export default function PlayerInfo({ name, captured, time, isCurrentTurn }: PlayerInfoProps) {
  const seconds = Math.floor(time);
  const milliseconds = Math.floor((time % 1) * 100);

  return (
    <div className={`p-6 rounded-lg ${isCurrentTurn ? 'bg-indigo-100' : 'bg-gray-100'} shadow-lg transition-colors`}>
      <div className="flex items-center gap-3 mb-4">
        <User className="w-6 h-6 text-indigo-600" />
        <h3 className="text-xl font-bold text-gray-800">{name}</h3>
      </div>
      <div className="space-y-2">
        <div className="flex items-center gap-2">
          <Timer className="w-5 h-5 text-indigo-600" />
          <span className="text-lg font-mono">
            {String(seconds).padStart(2, '0')}<span className="text-sm">.{String(milliseconds).padStart(2, '0')}</span>
          </span>
        </div>
        <div className="text-sm text-gray-600">
          Captured: <span className="font-bold text-indigo-600">{captured}</span>
        </div>
      </div>
    </div>
  );
}