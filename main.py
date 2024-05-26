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


def coin_toss():
    while True:
        choice = input("Choose heads or tails (H/T): ").upper()
        if choice in ['H', 'T']:
            break
        else:
            print("Invalid choice. Please choose H for heads or T for tails.")

    result = random.choice(['H', 'T'])
    print(f"Coin toss result: {'heads' if result == 'H' else 'tails'}")

    return choice == result


def choose_placement_method():
    while True:
        method = input("Do you want to place ships manually or automatically? (M/A): ").upper()
        if method in ['M', 'A']:
            return method
        else:
            print("Invalid choice. Please choose M for manual or A for automatic.")


def main():
    print("Welcome to Battleship!")
    size = get_board_size()

    player_board = Board(size)
    machine_board = Board(size)

    placement_method = choose_placement_method()
    if placement_method == 'M':
        print("\nPlacing player's ships manually...")
        player_board.place_all_ships_manual()
    else:
        print("\nPlacing player's ships automatically...")
        player_board.place_all_ships()

    print("Player's board:")
    player_board.print_board()

    print("\nPlacing machine's ships...")
    machine_board.place_all_ships()
    print("Machine's board (hidden):")
    machine_board.print_board(hide_ships=True)

    print("\nLet's do a coin toss to see who goes first.")
    player_turn = coin_toss()
    if player_turn:
        print("You won the coin toss! You will go first.")
    else:
        print("You lost the coin toss! The machine will go first.")

    turns = 0

    while True:
        if player_turn:
            print("\nPlayer's turn:")
            row, col = get_shot()
            hit, ship_name, destroyed = machine_board.receive_missile(row, col)
            if hit:
                if destroyed:
                    print(f"Hit! You destroyed the {ship_name}!")
                else:
                    print(f"Hit! You hit the {ship_name}.")
            else:
                print("Miss!")
            machine_board.print_board(hide_ships=True)
        else:
            print("\nMachine's turn:")
            row, col = random.randint(0, size - 1), random.randint(0, size - 1)
            hit, ship_name, destroyed = player_board.receive_missile(row, col)
            if hit:
                if destroyed:
                    print(f"Machine hit and destroyed your {ship_name}!")
                else:
                    print(f"Machine hit your {ship_name}!")
            else:
                print("Machine missed!")
            player_board.print_board()

        if player_board.all_ships_sunk():
            print("Game Over! Machine wins!")
            print(f"Total turns: {turns}")
            break
        elif machine_board.all_ships_sunk():
            print("Game Over! Player wins!")
            print(f"Total turns: {turns}")
            break

        player_turn = not player_turn
        if not player_turn:
            turns += 1  # Increment turns after each complete cycle


if __name__ == "__main__":
    main()
