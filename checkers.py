"""Two-player checkers for the terminal. Run with: python checkers.py"""

from time import perf_counter


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.moves = 0
        self.result = "In progress"
        self.time = 0.0  # Seconds spent taking turns.


class Checker:
    def __init__(self, color, row, column):
        self.color = color
        self.row = row
        self.column = column
        self.king = False

    def directions(self):
        if self.king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        forward = -1 if self.color == "red" else 1
        return [(forward, -1), (forward, 1)]

    def move_to(self, row, column):
        self.row = row
        self.column = column
        crowned = not self.king and (
            (self.color == "red" and row == 0)
            or (self.color == "black" and row == 7)
        )
        if crowned:
            self.king = True
        return crowned

    def symbol(self):
        letter = "r" if self.color == "red" else "b"
        return letter.upper() if self.king else letter


class Board:
    def __init__(self):
        self.checkers = [[None for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for column in range(8):
                if (row + column) % 2 == 1:
                    if row < 3:
                        self.checkers[row][column] = Checker("black", row, column)
                    elif row > 4:
                        self.checkers[row][column] = Checker("red", row, column)

    def display(self):
        print("\n    a b c d e f g h")
        for row in range(8):
            symbols = []
            for column in range(8):
                piece = self.checkers[row][column]
                symbols.append(piece.symbol() if piece else (
                    "." if (row + column) % 2 else " "
                ))
            print(f" {8 - row}  {' '.join(symbols)}  {8 - row}")
        print("    a b c d e f g h")
        print("r = red, b = black, uppercase = king\n")

    @staticmethod
    def inside(row, column):
        return 0 <= row < 8 and 0 <= column < 8

    def options(self, piece, captures=False):
        destinations = []
        for dr, dc in piece.directions():
            row, column = piece.row + dr, piece.column + dc
            if not self.inside(row, column):
                continue
            neighbour = self.checkers[row][column]
            if captures:
                landing_row, landing_column = row + dr, column + dc
                if (neighbour and neighbour.color != piece.color
                        and self.inside(landing_row, landing_column)
                        and self.checkers[landing_row][landing_column] is None):
                    destinations.append((landing_row, landing_column))
            elif neighbour is None:
                destinations.append((row, column))
        return destinations

    def legal_moves(self, color):
        steps, jumps = [], []
        for row in self.checkers:
            for piece in row:
                if piece and piece.color == color:
                    start = (piece.row, piece.column)
                    jumps.extend((start, end) for end in self.options(piece, True))
                    steps.extend((start, end) for end in self.options(piece))
        # If any capture is possible, an ordinary move is not allowed.
        return jumps if jumps else steps

    def move(self, start, end):
        piece = self.checkers[start[0]][start[1]]
        captured = abs(end[0] - start[0]) == 2
        self.checkers[start[0]][start[1]] = None
        if captured:
            self.checkers[(start[0] + end[0]) // 2][(start[1] + end[1]) // 2] = None
        crowned = piece.move_to(*end)
        self.checkers[end[0]][end[1]] = piece
        return captured, crowned

    def count(self, color):
        return sum(piece is not None and piece.color == color
                   for row in self.checkers for piece in row)


class Game:
    def __init__(self, red_name, black_name):
        self.players = [Player(red_name, "red"), Player(black_name, "black")]
        self.board = Board()
        self.moves = 0
        self.time = 0.0
        self.reason = ""

    @staticmethod
    def square(text):
        text = text.lower().strip()
        if len(text) != 2 or text[0] not in "abcdefgh" or text[1] not in "12345678":
            raise ValueError("Use a square like a3 or b4.")
        return 8 - int(text[1]), ord(text[0]) - ord("a")

    @staticmethod
    def label(position):
        row, column = position
        return f"{chr(ord('a') + column)}{8 - row}"

    def take_turn(self, player):
        legal = self.board.legal_moves(player.color)
        while True:
            command = input("Enter a move (a3 b4), or finish: ").strip().lower()
            if command == "finish":
                return False
            try:
                parts = command.split()
                if len(parts) != 2:
                    raise ValueError("Enter two squares, for example a3 b4.")
                start, end = map(self.square, parts)
                if (start, end) not in legal:
                    raise ValueError("Illegal move. Captures are compulsory when available.")
            except ValueError as error:
                print(error)
                continue
            break

        captured, crowned = self.board.move(start, end)
        print(f"{player.name} ({player.color}): {self.label(start)} -> {self.label(end)}")
        self.board.display()
        # A jump sequence belongs to one turn. Crowning ends that turn.
        while captured and not crowned:
            piece = self.board.checkers[end[0]][end[1]]
            options = self.board.options(piece, captures=True)
            if not options:
                break
            print("Continue capturing with the same piece:",
                  ", ".join(self.label(position) for position in options))
            while True:
                try:
                    next_square = self.square(input("Next landing square: "))
                    if next_square not in options:
                        raise ValueError("Choose one of the listed squares.")
                    break
                except ValueError as error:
                    print(error)
            captured, crowned = self.board.move(end, next_square)
            print(f"{player.name}: {self.label(end)} -> {self.label(next_square)}")
            end = next_square
            self.board.display()
        player.moves += 1
        self.moves += 1
        return True

    def play(self):
        started = perf_counter()
        turn = 0
        print("\nRed moves first. Move diagonally; jump to capture.")
        print("Reach the opposite edge to become a king. Type finish to stop.")
        try:
            while True:
                player = self.players[turn]
                opponent = self.players[1 - turn]
                self.board.display()
                if not self.board.legal_moves(player.color):
                    player.result = "Lost"
                    opponent.result = "Won"
                    self.reason = f"{player.name} has no legal moves or no pieces."
                    break
                print(f"Turn {self.moves + 1}: {player.name} ({player.color})")
                turn_started = perf_counter()
                try:
                    completed = self.take_turn(player)
                finally:
                    player.time += perf_counter() - turn_started
                if not completed:
                    self.reason = f"{player.name} chose to finish the game."
                    break
                turn = 1 - turn
        except (KeyboardInterrupt, EOFError):
            self.reason = "The game was interrupted."
        finally:
            self.time = perf_counter() - started
            for player in self.players:
                if player.result == "In progress":
                    player.result = "Stopped (unfinished)"
            self.summary()

    def summary(self):
        print("\n--- Game summary ---")
        print(self.reason)
        print(f"Total moves: {self.moves}")
        print(f"Game duration: {self.time:.1f} seconds")
        for player in self.players:
            print(f"{player.name} ({player.color}): {player.result}")
            print(f"  Moves: {player.moves}, pieces left: {self.board.count(player.color)}, "
                  f"turn time: {player.time:.1f} seconds")


if __name__ == "__main__":
    print("Two-player checkers")
    red_name = input("Red player's name: ").strip() or "Player 1"
    black_name = input("Black player's name: ").strip() or "Player 2"
    Game(red_name, black_name).play()
