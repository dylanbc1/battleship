from board import Board
import random

def get_board_size():
    while True:
        try:
            size = int(input("Enter board size (5-15): "))
            if 5 <= size <= 15:
                return size
            else:
                print("Please enter a number between 5 and 15.")
        except ValueError:
            print("Invalid input. Please enter a number between 5 and 15.")

def get_shot():
    while True:
        try:
            row = int(input("Enter row (0-indexed): "))
            col = int(input("Enter column (0-indexed): "))
            return row, col
        except ValueError:
            print("Invalid input. Please enter numbers for row and column.")

def main():
    print("Welcome to Battleship!")
    size = get_board_size()

    player_board = Board(size)
    machine_board = Board(size)

    print("\nPlacing player's ships...")
    player_board.place_all_ships()
    print("Player's board:")
    player_board.print_board()

    print("\nPlacing machine's ships...")
    machine_board.place_all_ships()
    print("Machine's board (hidden):")
    machine_board.print_board(hide_ships=True)

    player_turn = True

    while True:
        if player_turn:
            print("\nPlayer's turn:")
            row, col = get_shot()
            hit, ship_type = machine_board.receive_missile(row, col)
            if hit:
                print(f"Hit! You hit the {ship_type}.")
            else:
                print("Miss!")
            machine_board.print_board(hide_ships=True)
        else:
            print("\nMachine's turn:")
            row, col = random.randint(0, size-1), random.randint(0, size-1)
            hit, ship_type = player_board.receive_missile(row, col)
            if hit:
                print(f"Machine hit your {ship_type}!")
            else:
                print("Machine missed!")
            player_board.print_board()

        player_turn = not player_turn

if __name__ == "__main__":
    main()