# Multiplayer Server Tic Tac Toe (Command Line)

## Overview
This project implements a **multiplayer Tic Tac Toe game** using Python with multi-threading. Players can join the server, send play requests to other players, and engage in multiple simultaneous games. The game runs entirely on the command line.

---

## Features
- Multi-threaded server to handle multiple players and games simultaneously.
- Dynamic player list refresh.
- Games start automatically upon acceptance of a play request.
- Command-line-based interaction for both server and players.

---

## Requirements
- **Python 3.8 or higher**

---

## Setup Instructions

### 1. Clone the Repository
```bash
$ git clone <repository_url>
$ cd <repository_folder>
```

### 2. Run the Server
1. Open a terminal.
2. Navigate to the project folder.
3. Run the server script:
   ```bash
   $ python server.py
   ```

### 3. Run Players
1. Open additional terminal windows for each player.
2. Navigate to the project folder.
3. Run the player script for each player:
   ```bash
   $ python client.py
   ```

---

## How to Play

### 1. Connect to the Server
Each player connects to the server upon running the `client.py` script. A unique ID is assigned to each player.

### 2. Refresh the Player List
To see the updated list of active players:
```bash
> refresh
```

### 3. Send a Play Request
Send a play request to another player by their ID:
```bash
> play <player_id>
```


### 4. Play the Game
- Once the game starts, players take turns entering their moves (row and column indices).
- The server validates moves and notifies players of the game's progress.

### 5. End of Game
- The game ends when a player wins, or the board is filled (draw).

---

## Notes
- The server can handle multiple games concurrently.
- Ensure all players are connected to the server before sending play requests.

---
