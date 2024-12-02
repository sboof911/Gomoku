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

### Backend

The backend is located in the `backend` directory and includes:

- `api/`: Contains the API logic for the game.
- `srcs/ai/`: Contains the AI logic for the game, including heuristic evaluation and memoization.
- `srcs/game` : Contains the core game logic, including board representation, move validation, and game state management.
- `srcs/settings/`: Contains configuration settings for the game, including game rules and server settings.
- `server.py`: The main server file.

### Frontend

The frontend is located in the `render` directory and includes:

- `src/`: Contains the React components and main application logic.
- `index.html`: The main HTML file.
- `package.json`: The npm configuration file.

