import json
import os

LIBRARY_FILE = 'library.txt'

def load_data():
    """Load the users' library data from file if exists; otherwise return an empty dict."""
    if os.path.exists(LIBRARY_FILE) and os.path.getsize(LIBRARY_FILE) > 0:
        try:
            with open(LIBRARY_FILE, 'r') as file:
                data = json.load(file)
                return data
        except Exception as e:
            print("Error loading data:", e)
    return {}

def save_data(data):
    """Save the complete users' library data to file."""
    try:
        with open(LIBRARY_FILE, 'w') as file:
            json.dump(data, file, indent=4)
        print("Data saved to file. Goodbye!")
    except Exception as e:
        print("Error saving data:", e)

def register_user(data):
    """Register a new user by asking username and password."""
    while True:
        username = input("Enter new username: ").strip()
        if username in data:
            print("Username already exists. Please choose a different name.")
        else:
            break
    password = input("Enter new password: ").strip()
    # Initialize empty library for the new user
    data[username] = {"password": password, "books": []}
    print("Registration successful!")
    return username

def login_user(data):
    """Login an existing user by verifying username and password."""
    for _ in range(3):
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        if username in data and data[username]["password"] == password:
            print("Login successful!")
            return username
        else:
            print("Invalid username or password. Try again.")
    print("Too many failed attempts. Exiting.")
    exit()

def add_book(library):
    """Prompt the user to add a book and append it to the user's library."""
    print("\nAdd a Book:")
    title = input("Enter the book title: ").strip()
    author = input("Enter the author: ").strip()
    try:
        year = int(input("Enter the publication year: ").strip())
    except ValueError:
        print("Invalid year. Please enter an integer.")
        return
    genre = input("Enter the genre: ").strip()
    read_input = input("Have you read this book? (yes/no): ").strip().lower()
    read_status = True if read_input == 'yes' else False

    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read_status
    }
    library.append(book)
    print("Book added successfully!")

def remove_book(library):
    """Remove a book by title from the library."""
    print("\nRemove a Book:")
    title = input("Enter the title of the book to remove: ").strip()
    removed = False
    for book in library:
        if book["title"].lower() == title.lower():
            library.remove(book)
            removed = True
            print("Book removed successfully!")
            break
    if not removed:
        print("Book not found.")

def search_book(library):
    """Search for books by title or author."""
    print("\nSearch for a Book:")
    print("Search by:")
    print("1. Title")
    print("2. Author")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        search_term = input("Enter the title: ").strip().lower()
        # List comprehension
        results = [book for book in library if search_term in book["title"].lower()]
    elif choice == '2':
        search_term = input("Enter the author: ").strip().lower()
        results = [book for book in library if search_term in book["author"].lower()]
    else:
        print("Invalid choice.")
        return

    if results:
        print("\nMatching Books:")
        # enumerate built in function , that return index also iterate value.
        for idx, book in enumerate(results, start=1):
            # ternary operator
            status = "Read" if book["read"] else "Unread"
            print(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        print("No matching books found.")

def display_all_books(library):
    """Display all books in the library."""
    print("\nYour Library:")
    if not library:
        print("No books in your library.")
    else:
        for idx, book in enumerate(library, start=1):
            status = "Read" if book["read"] else "Unread"
            print(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

def display_statistics(library):
    """Display statistics such as total books and percentage read."""
    total = len(library)
    if total == 0:
        print("\nNo books in your library.")
        return
    #   generator expression
    read_books = sum(1 for book in library if book["read"])
    percentage = (read_books / total) * 100
    print(f"\nTotal books: {total}")
    print(f"Percentage read: {percentage:.1f}%")

def user_menu(library):
    """Display the menu and process user choices for managing the library."""
    while True:
        print("\nMenu:")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_book(library)
        elif choice == '2':
            remove_book(library)
        elif choice == '3':
            search_book(library)
        elif choice == '4':
            display_all_books(library)
        elif choice == '5':
            display_statistics(library)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    # Load overall data from file
    data = load_data()

    # User authentication/registration
    if data:
        user_type = input("Are you a new user? (yes/no): ").strip().lower()
    else:
        print("No user data found. Let's register you as a new user.")
        user_type = "yes"

    if user_type == "yes":
        current_user = register_user(data)
    else:
        current_user = login_user(data)

    # Load current user's library (books)
    current_library = data[current_user]["books"]

    # Run the menu for the current user
    user_menu(current_library)

    # Update the user's library data
    data[current_user]["books"] = current_library
    save_data(data)


main()
