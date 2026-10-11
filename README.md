# Terminal Checkers

A two-player checkers game written in Python. Two people take turns on the same computer, entering moves in a terminal. The program displays the board, validates moves, handles captures and kings, and prints game statistics when play ends.

## Features

- An 8 x 8 board with 12 pieces per player.
- Player names and alternating turns, with red moving first.
- Legal-move validation and compulsory captures.
- Multiple jumps using the same piece.
- King promotion and movement in both directions.
- Win detection when a player has no pieces or legal moves.
- A final summary with results, move counts, remaining pieces, and elapsed time.


## Run the game

Open a terminal in the folder containing `checkers.py` and run:

```shell
python checkers.py
```


Enter a name for each player. Leaving a name blank uses `Player 1` or `Player 2`.

## Controls

Enter the starting square and destination square, separated by a space:

```text
a3 b4
```

This moves a piece from `a3` to `b4`. Columns are labeled `a` through `h`, and rows are labeled `1` through `8`. Invalid input displays an error and lets the same player try again.

For a capture, enter the starting square and the landing square beyond the opponent's piece. If another capture is available, the program lists the next landing squares. Enter just the next destination to continue the jump sequence.

Type `finish` at the initial move prompt to stop the game and display the summary. A capture sequence must be completed once started, so `finish` is not accepted at the continuation prompt. Pressing `Ctrl+C` during play interrupts the game and prints the summary.

### Board symbols

| Symbol | Meaning |
| --- | --- |
| `r` | Red piece |
| `b` | Black piece |
| `R` | Red king |
| `B` | Black king |
| `.` | Empty playable square |
| Blank | Light square |

## Game rules

The game uses English/American checkers movement rules:

- Ordinary pieces move one square diagonally forward into an empty square.
- Ordinary pieces capture forward by jumping over an adjacent opponent into an empty square.
- A capture is compulsory if any piece belonging to the current player can capture.
- When several captures are available, the player can choose any legal option.
- After a capture, the same piece must keep jumping while another capture is available.
- A piece reaching the opposite edge becomes a king, ending that turn.
- Kings move one square diagonally in either direction and capture by jumping in either direction.
- A player loses when they have no legal moves, including when all their pieces have been captured.

A multiple-jump sequence counts as one completed move. Stopping manually records the game as unfinished.

## Code structure

The game is contained in `checkers.py` and organized into four classes:

| Class | Responsibility |
| --- | --- |
| `Player` | Stores a player's name, color, moves, result, and accumulated turn time. |
| `Checker` | Stores a piece's position and king status; provides movement directions, promotion, and display symbols. |
| `Board` | Stores the grid, creates the starting position, displays pieces, finds legal moves, applies moves, and counts remaining pieces. |
| `Game` | Creates the players and board, converts coordinates, processes input, manages turns, measures time, and prints the summary. |

The board is a nested list accessed as `checkers[row][column]`. Each square contains either a `Checker` object or `None`. Internal indices range from `0` to `7`; the game translates these to the printed board coordinates.

`Board.legal_moves()` returns captures whenever any are available, enforcing compulsory capture. `Game.take_turn()` checks input against those moves before calling `Board.move()`. The move method assumes its arguments have already been validated.

`Game.play()` alternates players and checks for a winner before each turn. Its `finally` block records the duration and prints the summary when play ends. The main guard starts the interactive game only when the file is run directly, so the classes can also be imported without prompting for input.

## Game statistics

The final summary includes:

- Why the game ended.
- Total completed moves and overall game duration.
- Each player's result, completed moves, remaining pieces, and turn time.

Game duration starts after player names are entered. Player time includes thinking time, invalid input retries, and capture continuations during that player's turns. An interrupted, incomplete turn is not counted, although any jumps already applied remain on the board.

## Rules reference

[World Checkers/Draughts Federation: Rules of Checkers](https://wcdf.net/rules/rules_of_checkers_english.pdf)
