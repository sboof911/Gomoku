import React, { createContext, useContext, useState } from 'react';

interface GameContextType {
  player1Name: string;
  player2Name: string;
  aiName: string;
  difficulty: 'easy' | 'medium' | 'hard';
  setPlayer1Name: (name: string) => void;
  setPlayer2Name: (name: string) => void;
  setAiName: (name: string) => void;
  setDifficulty: (difficulty: 'easy' | 'medium' | 'hard') => void;
}

const GameContext = createContext<GameContextType | undefined>(undefined);

export function GameProvider({ children }: { children: React.ReactNode }) {
  const [player1Name, setPlayer1Name] = useState('Player 1');
  const [player2Name, setPlayer2Name] = useState('Player 2');
  const [aiName, setAiName] = useState('AI Player');
  const [difficulty, setDifficulty] = useState<'easy' | 'medium' | 'hard'>('medium');

  return (
    <GameContext.Provider
      value={{
        player1Name,
        player2Name,
        aiName,
        difficulty,
        setPlayer1Name,
        setPlayer2Name,
        setAiName,
        setDifficulty,
      }}
    >
      {children}
    </GameContext.Provider>
  );
}

export function useGame() {
  const context = useContext(GameContext);
  if (context === undefined) {
    throw new Error('useGame must be used within a GameProvider');
  }
  return context;
}