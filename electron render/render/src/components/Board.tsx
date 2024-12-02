import React from 'react';
import type { WinningLine } from '../types/game';

interface BoardProps {
  board: number[][];
  onCellClick: (row: number, col: number) => void;
  hintPosition: [number, number] | null;
  winningLine: WinningLine;
}

export default function Board({ board, onCellClick, hintPosition, winningLine }: BoardProps) {
  const CELL_SIZE = 24;
  const GRID_SIZE = 19;
  const DISPLAY_SIZE = 20;
  const BOARD_SIZE = CELL_SIZE * (DISPLAY_SIZE - 1);

  const renderWinningLine = () => {
    if (!winningLine) return null;

    const { start, end } = winningLine;
    const startX = start[1] * CELL_SIZE;
    const startY = start[0] * CELL_SIZE;
    const endX = end[1] * CELL_SIZE;
    const endY = end[0] * CELL_SIZE;

    // Calculate line length and angle
    const dx = endX - startX;
    const dy = endY - startY;
    const length = Math.sqrt(dx * dx + dy * dy);
    const angle = Math.atan2(dy, dx) * (180 / Math.PI);

    return (
      <div
        className="absolute bg-green-500 rounded-full transform -translate-x-1/2 -translate-y-1/2 z-20"
        style={{
          width: `${length}px`,
          height: '4px',
          left: startX,
          top: startY,
          transformOrigin: 'left',
          transform: `rotate(${angle}deg)`,
        }}
      />
    );
  };

  return (
    <div className="relative bg-amber-100 p-8 rounded-lg shadow-xl">
      <div 
        className="relative"
        style={{ 
          width: BOARD_SIZE,
          height: BOARD_SIZE,
        }}
      >
        {/* Grid lines */}
        {Array.from({ length: DISPLAY_SIZE }, (_, i) => (
          <React.Fragment key={i}>
            {/* Vertical lines */}
            <div
              className="absolute bg-[#855E42] w-[1px]"
              style={{
                left: `${CELL_SIZE * i}px`,
                top: '0px',
                height: `${BOARD_SIZE}px`,
              }}
            />
            {/* Horizontal lines */}
            <div
              className="absolute bg-[#855E42] h-[1px]"
              style={{
                top: `${CELL_SIZE * i}px`,
                left: '0px',
                width: `${BOARD_SIZE}px`,
              }}
            />
          </React.Fragment>
        ))}

        {renderWinningLine()}

        {/* Intersection points for gameplay (19x19) */}
        <div className="absolute inset-0 grid"
          style={{ 
            gridTemplateColumns: `repeat(${GRID_SIZE}, ${CELL_SIZE}px)`,
            gridTemplateRows: `repeat(${GRID_SIZE}, ${CELL_SIZE}px)`,
            transform: `translate(${-CELL_SIZE/2}px, ${-CELL_SIZE/2}px)`,
          }}
        >
          {board.map((row, i) =>
            row.map((cell, j) => (
              <button
                key={`${i}-${j}`}
                className="w-6 h-6 relative z-10"
                onClick={() => onCellClick(i, j)}
              >
                {cell !== 0 && (
                  <div 
                    className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-5 h-5 rounded-full
                      ${cell === 1 ? 'bg-black' : 'bg-white border-2 border-black'}`}
                  />
                )}
                {hintPosition && hintPosition[0] === i && hintPosition[1] === j && cell === 0 && (
                  <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-5 h-5 rounded-full border-2 border-indigo-500 animate-pulse" />
                )}
              </button>
            ))
          )}
        </div>
      </div>
    </div>
  );
}