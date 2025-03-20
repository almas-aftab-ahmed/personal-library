import json
import os

BOOKS_FILE = "books.json"

def load_books():
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, "r") as file:
        return json.load(file)

def save_books(books):
    with open(BOOKS_FILE, "w") as file:
        json.dump(books, file, indent=4)

def show_books():
    books = load_books()
    if not books:
        print("📖 No books found!")
        return
    for index, book in enumerate(books):
        status = "✅ Read" if book["read"] else "❌ Unread"
        print(f"{index + 1}. {book['title']} by {book['author']} - {status}")

def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    books = load_books()
    books.append({"title": title, "author": author, "read": False})
    save_books(books)
    print(f"📚 '{title}' added to library!")

def mark_read():
    show_books()
    index = int(input("Enter book number to mark read/unread: ")) - 1
    books = load_books()
    if 0 <= index < len(books):
        books[index]["read"] = not books[index]["read"]
        save_books(books)
        print("✔ Status updated!")
    else:
        print("❌ Invalid choice!")

def remove_book():
    show_books()
    index = int(input("Enter book number to remove: ")) - 1
    books = load_books()
    if 0 <= index < len(books):
        removed = books.pop(index)
        save_books(books)
        print(f"🗑 '{removed['title']}' removed from library!")
    else:
        print("❌ Invalid choice!")

def main():
    while True:
        print("\n📚 Personal Library CLI")
        print("1️⃣ Show Books")
        print("2️⃣ Add Book")
        print("3️⃣ Mark Read/Unread")
        print("4️⃣ Remove Book")
        print("5️⃣ Exit")
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            show_books()
        elif choice == "2":
            add_book()
        elif choice == "3":
            mark_read()
        elif choice == "4":
            remove_book()
        elif choice == "5":
            print("👋 Exiting Library CLI!")
            break
        else:
            print("❌ Invalid choice! Try again.")

if __name__ == "__main__":
    main()
