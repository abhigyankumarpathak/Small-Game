from library import clear_screen, print_header, show_help
from player import Player
from world import describe_room, handle_command


def main():
    player = Player()
    room_name = "forest"

    clear_screen()
    print_header("Treasure Trail")
    print("You wake up in a quiet forest.")
    print("Your goal is to reach the treasure room.")
    show_help()
    print()

    while True:
        clear_screen()
        print_header("Treasure Trail")
        print(describe_room(room_name))
        print("\nInventory:", player.show_inventory())

        command = input("\nWhat do you do? ").strip().lower()

        try:
            room_name, message = handle_command(room_name, command, player)
        except SystemExit:
            print("Thanks for playing!")
            break

        print("\n" + message)

        if room_name == "treasure":
            print("\nYou win!")
            break


if __name__ == "__main__":
    main()
