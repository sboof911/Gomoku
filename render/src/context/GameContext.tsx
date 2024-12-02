import React, { createContext, useContext, useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import axios from 'axios';
import config from '../Config';

interface GameContextType {
  player1Name: string;
  player2Name: string;
  aiName: string;
  difficulty: 'easy' | 'medium' | 'hard';
  setPlayer1Name: (name: string) => void;
  setPlayer2Name: (name: string) => void;
  setAiName: (name: string) => void;
  setDifficulty: (difficulty: 'easy' | 'medium' | 'hard') => void;
  getPlayer1Name: () => Promise<void>;
  getPlayer2Name: () => Promise<void>;
  getAiName: () => Promise<void>;
  getDifficulty: () => Promise<void>;
}

const GameContext = createContext<GameContextType | undefined>(undefined);

const validatePlayerName = async (name: string, setting: string): Promise<string | null> => {
  try {
    await axios.post(`${config.serverUrl}/api/settings/${setting}`, { [setting]: name }, {headers : config.headers_data});
    return null;
  } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        return err.response.data.message;
      }
      return 'An unknown error occurred';
  }
};


export function GameProvider({ children }: { children: React.ReactNode }) {
  const [player1Name, setPlayer1NameState] = useState('');
  const [player2Name, setPlayer2NameState] = useState('');
  const [aiName, setAiNameState] = useState('');
  const [difficulty, setDifficultyState] = useState<'easy' | 'medium' | 'hard'>('medium');

  useEffect(() => {
    const fetchInitialSettings = async () => {
      try {
        const player1Response = await axios.get(`${config.serverUrl}/api/settings/player1`, {headers : config.headers_data});
        setPlayer1NameState(player1Response.data.message);

        const player2Response = await axios.get(`${config.serverUrl}/api/settings/player2`, {headers : config.headers_data});
        setPlayer2NameState(player2Response.data.message);

        const aiNameResponse = await axios.get(`${config.serverUrl}/api/settings/AIName`, {headers : config.headers_data});
        setAiNameState(aiNameResponse.data.message);

        const difficultyResponse = await axios.get(`${config.serverUrl}/api/settings/difficulty`, {headers : config.headers_data});
        setDifficultyState(difficultyResponse.data.message);
      } catch (error) {
        console.error('Error fetching initial settings:', error);
      }
    };

    fetchInitialSettings();
  }, []);

  const setPlayer1Name = async (name: string) => {
    const error = await validatePlayerName(name, "player1");
    if (error) {
      console.log(error)
      toast.error(`Player1 ${error}`);
      return;
    }
    setPlayer1NameState(name);
    toast.success('Player 1 name updated');
  };

  const setPlayer2Name = async (name: string) => {
    const error = await validatePlayerName(name, "player2");
    if (error) {
      toast.error(`Player2 ${error}`);
      return;
    }
    setPlayer2NameState(name);
    toast.success('Player 2 name updated');
  };

  const setAiName = async (name: string) => {
    const error = await validatePlayerName(name, "AIName");
    if (error) {
      toast.error(`AIName ${error}`);
      return;
    }
    setAiNameState(name);
    toast.success('AI name updated');
  };

  const setDifficulty = (difficulty: 'easy' | 'medium' | 'hard') => {
    var error = null;
    axios.post(`${config.serverUrl}/api/settings/difficulty/${difficulty}`, { difficulty }, {headers : config.headers_data})
        .then(_ => error = null)
        .catch(error => error = error.response.data.message);

    if (error) {
      toast.error(error);
      return;
    }
    setDifficultyState(difficulty);
    toast.success('Difficulty updated');
  };

  const getPlayer1Name = async () => {
    try {
      const response = await axios.get(`${config.serverUrl}/api/settings/player1`, {headers : config.headers_data});
      setPlayer1NameState(response.data.message);
    } catch (error) {
      console.error('Error fetching player1Name:', error);
    }
  };

  const getPlayer2Name = async () => {
    try {
      const response = await axios.get(`${config.serverUrl}/api/settings/player2`, {headers : config.headers_data});
      setPlayer2NameState(response.data.message);
    } catch (error) {
      console.error('Error fetching player2Name:', error);
    }
  };

  const getAiName = async () => {
    try {
      const response = await axios.get(`${config.serverUrl}/api/settings/AIName`, {headers : config.headers_data});
      setAiNameState(response.data.message);
    } catch (error) {
      console.error('Error fetching aiName:', error);
    }
  };

  const getDifficulty = async () => {
    try {
      const response = await axios.get(`${config.serverUrl}/api/settings/difficulty`, {headers : config.headers_data});
      setDifficultyState(response.data.message);
    } catch (error) {
      console.error('Error fetching difficulty:', error);
    }
  };

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
        getPlayer1Name,
        getPlayer2Name,
        getAiName,
        getDifficulty,
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