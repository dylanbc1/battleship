import random

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]
        self.ships = {
            'Aircraft Carrier': ('A', 5),
            'Battleship': ('B', 4),
            'Cruiser': ('C', 3),
            'Submarine': ('S', 3),
            'Destroyer': ('D', 2)
        }
        self.ship_symbols = {v[0]: (k, v[1]) for k, v in self.ships.items()}
        self.ship_health = {symbol: size for symbol, (_, size) in self.ship_symbols.items()}

    def print_board(self, hide_ships=False):
        for row in self.grid:
            if hide_ships:
                print(' '.join(['~' if cell not in ('X', 'O', '~') else cell for cell in row]))
            else:
                print(' '.join(row))
        print()

    def place_ship(self, ship_symbol, ship_size):
        placed = False
        while not placed:
            orientation = random.choice(['H', 'V'])
            if orientation == 'H':
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - ship_size)
                if all(self.grid[row][col + i] == '~' for i in range(ship_size)):
                    for i in range(ship_size):
                        self.grid[row][col + i] = ship_symbol
                    placed = True
            else:
                row = random.randint(0, self.size - ship_size)
                col = random.randint(0, self.size - 1)
                if all(self.grid[row + i][col] == '~' for i in range(ship_size)):
                    for i in range(ship_size):
                        self.grid[row + i][col] = ship_symbol
                    placed = True

    def place_all_ships(self):
        for ship, (symbol, size) in self.ships.items():
            self.place_ship(symbol, size)

    def receive_missile(self, row, col):
        if self.grid[row][col] in self.ship_symbols:
            ship_symbol = self.grid[row][col]
            self.grid[row][col] = 'X'  # Hit
            self.ship_health[ship_symbol] -= 1
            if self.ship_health[ship_symbol] == 0:
                return True, self.ship_symbols[ship_symbol][0], True
            return True, self.ship_symbols[ship_symbol][0], False
        else:
            self.grid[row][col] = 'O'  # Miss
            return False, None, False

    def all_ships_sunk(self):
        return all(health == 0 for health in self.ship_health.values())
