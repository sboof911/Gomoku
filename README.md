# Gomoku

This is a Gomoku game project developed as part of the 42 projects. The project includes both a backend and a frontend, with the backend written in Python and the frontend in TypeScript using React.


## Getting Started

### Prerequisites

- Python
- Node.js
- npm

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/sboof911/Gomoku
    cd Gomoku
    ```

### Building the Project

To build both the frontend and backend, run:
```sh
make build
```

This will:

- Create a virtual environment for the backend and install the dependencies.
- Build the frontend using npm.
- Package the backend using PyInstalle

### Running the Project

To start the project, run:
```sh
make start
```

This will build the project and start the Gomoku executable.

### Cleaning the Project
To clean the build artifacts, run:
```sh
make clean
```

To perform a full clean, run:
```sh
make fclean
```

## Project Details

### AI Details

The AI for the Gomoku game is implemented using the Minimax algorithm with alpha-beta pruning. The AI logic is located in the [`ai`](backend/srcs/ai) directory and includes the following key components:

#### Key Components

- **Minimax Algorithm**: The core of the AI is the Minimax algorithm, which is implemented in the [`minimax`](backend/srcs/ai/Minimax.py) function. This function recursively evaluates possible moves to determine the best move for the AI player.

- **Alpha-Beta Pruning**: To optimize the Minimax algorithm, alpha-beta pruning is used to eliminate branches in the search tree that do not need to be explored. This helps in reducing the computation time.

- **Heuristic Evaluation**: The AI uses a heuristic evaluation function to score the board positions. This function is implemented in the [`heuristic_evaluation`](backend/srcs/ai/heuristic_evaluation.py) function and considers factors such as the number of stones in a row, potential captures, and free spaces.

- **AI Manager**: The [`AI_manager`](backend/srcs/ai/ai_manager.py) class manages the AI's decision-making process. It handles the initialization of the AI and determining the best move based on the Minimax algorithm.

- **Memoization**: To further optimize the AI, memoization is used to store previously computed board states and their evaluations. This helps in avoiding redundant calculations and speeds up the decision-making process.


### Backend

The backend is located in the [`backend`](backend) directory and includes:

- [`api`](backend/api): Contains the API logic for the game.
- [`ai`](backend/srcs/ai): Contains the AI logic for the game, including heuristic evaluation and memoization.
- [`game`](backend/srcs/game) : Contains the core game logic, including board representation, move validation, and game state management.
- [`settings`](backend/srcs/settings): Contains configuration settings for the game, including game rules and server settings.
- [`server`](backend/server.py): The main server file.

### Frontend

The frontend is located in the [`render`](render)  directory and includes:

- [`src`](render/src): Contains the React components and main application logic.
- [`index`](render/index.html): The main HTML file.
- [`package`](render/package.json): The npm configuration file.
