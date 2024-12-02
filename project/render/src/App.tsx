import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainMenu from './pages/MainMenu';
import PlayerVsPlayer from './pages/PlayerVsPlayer';
import PlayerVsAI from './pages/PlayerVsAI';
import Settings from './pages/Settings';
import { GameProvider } from './context/GameContext';

function App() {
  return (
    <GameProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
          <Routes>
            <Route path="/" element={<MainMenu />} />
            <Route path="/pvp" element={<PlayerVsPlayer />} />
            <Route path="/ai" element={<PlayerVsAI />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </div>
      </BrowserRouter>
    </GameProvider>
  );
}

export default App;