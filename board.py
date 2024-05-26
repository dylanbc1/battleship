import random

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]
        self.ships = {
            'Aircraft Carrier': ('Aircraft Carrier', 5),
            'Battleship': ('Battleship', 4),
            'Cruiser': ('Cruiser', 3),
            'Submarine': ('Submarine', 3),
            'Destroyer': ('Destroyer', 2)
        }
        self.ship_health = {name: size for name, size in self.ships.values()}

    def print_board(self, hide_ships=False):
        for row in self.grid:
            if hide_ships:
                print(' '.join(['~' if cell not in ('X', 'O', '~') else cell for cell in row]))
            else:
                print(' '.join(cell[:1] if cell not in ('~', 'X', 'O') else cell for cell in row))
        print()

    def place_ship(self, ship_name, ship_size):
        placed = False
        while not placed:
            orientation = random.choice(['H', 'V'])
            if orientation == 'H':
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - ship_size)
                if all(self.grid[row][col + i] == '~' for i in range(ship_size)):
                    for i in range(ship_size):
                        self.grid[row][col + i] = ship_name
                    placed = True
            else:
                row = random.randint(0, self.size - ship_size)
                col = random.randint(0, self.size - 1)
                if all(self.grid[row + i][col] == '~' for i in range(ship_size)):
                    for i in range(ship_size):
                        self.grid[row + i][col] = ship_name
                    placed = True

    def place_all_ships(self):
        for ship, (name, size) in self.ships.items():
            self.place_ship(name, size)

    def place_ship_manual(self, ship_name, ship_size):
        while True:
            try:
                row = int(input(f"Enter starting row for {ship_name} (size {ship_size}): "))
                col = int(input(f"Enter starting column for {ship_name} (size {ship_size}): "))
                orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()

                if orientation == 'H':
                    if col + ship_size > self.size or any(self.grid[row][col + i] != '~' for i in range(ship_size)):
                        print("Invalid position. Try again.")
                        continue
                    for i in range(ship_size):
                        self.grid[row][col + i] = ship_name
                    break
                elif orientation == 'V':
                    if row + ship_size > self.size or any(self.grid[row + i][col] != '~' for i in range(ship_size)):
                        print("Invalid position. Try again.")
                        continue
                    for i in range(ship_size):
                        self.grid[row + i][col] = ship_name
                    break
                else:
                    print("Invalid orientation. Try again.")
            except ValueError:
                print("Invalid input. Please enter numbers for row and column.")

    def place_all_ships_manual(self):
        for ship, (name, size) in self.ships.items():
            self.print_board()
            self.place_ship_manual(name, size)

    def receive_missile(self, row, col):
        if self.grid[row][col] in self.ship_health:
            ship_name = self.grid[row][col]
            self.grid[row][col] = 'X'  # Hit
            self.ship_health[ship_name] -= 1
            if self.ship_health[ship_name] == 0:
                return True, ship_name, True
            return True, ship_name, False
        else:
            self.grid[row][col] = 'O'  # Miss
            return False, None, False

    def all_ships_sunk(self):
        return all(health == 0 for health in self.ship_health.values())
