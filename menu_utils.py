def print_menu(operations):
    print("\nSpotify Playlist Manager")
    sorted_operations = sorted(operations.items(), key=lambda x: int(x[0]))
    
    for option, operation in sorted_operations:
        print(f"{option}. {operation.__doc__.strip()}")
    print("0. Exit")

def get_user_choice(operations):
    while True:
        choice = input("Enter your choice: ")
        if choice == '0':
            return 'exit'
        if choice in operations:
            return choice
        print("Invalid choice. Please try again.")
