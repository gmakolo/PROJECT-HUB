print("WELCOME TO MY MYSTERY ISLAND")
print("Get ready for adventure!")
print("Find the lost lighthouse!")

player_name = input("What is your name, adventurer? ")

energy = 5
location = "Beach"
inventory = []

locations = [
    "Beach",
    "Forest",
    "River",
    "Cave",
    "Lighthouse"
]

print("\nWelcome,", player_name)
print("Your energy is:", energy)
print("You are starting at:", location)
print("Your inventory:", inventory)

print("\nPlaces you can explore:")

for number, place in enumerate(locations, start=1):
    print(f"{number}. {place}")

print("\nWhat would you like to do?")
print("1. Explore the island")
print("2. Check inventory")
print("3. Quit game")

choice = input("Enter your choice: ")

if choice == "1":
    print("\nWhere would you like to go?")

    for number, place in enumerate(locations, start=1):
        print(f"{number}. {place}")

    destination = input("Enter the location number: ")

    if destination.isdigit():
        destination = int(destination)

        if 1 <= destination <= len(locations):
            location = locations[destination - 1]
            energy = energy - 1

            print("You moved to:", location)
            print("Your energy is:", energy)
        else:
            print("Invalid location number.")
    else:
        print("Please enter a number.")

elif choice == "2":
    print("Your inventory:", inventory)

elif choice == "3":
    print("Thanks for playing!")

else:
    print("Invalid choice. Try again.")