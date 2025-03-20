import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = "static/pdfs"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 📚 Default Famous Books (with PDFs)
books = [
    {"title": "The Alchemist", "author": "Paulo Coelho", "cover": "https://m.media-amazon.com/images/I/51Z0nLAfLmL.jpg", "pdf": "the-alchemist.pdf", "read": False},
    {"title": "Atomic Habits", "author": "James Clear", "cover": "https://m.media-amazon.com/images/I/91bYsX41DVL.jpg", "pdf": "atomic-habits.pdf", "read": True},
    {"title": "1984", "author": "George Orwell", "cover": "https://m.media-amazon.com/images/I/71kxa1-0mfL.jpg", "pdf": "1984.pdf", "read": False},
    {"title": "Harry Potter", "author": "J.K. Rowling", "cover": "https://m.media-amazon.com/images/I/81YOuOGFCJL.jpg", "pdf": "harry-potter.pdf", "read": True},
    {"title": "Rich Dad Poor Dad", "author": "Robert Kiyosaki", "cover": "https://m.media-amazon.com/images/I/81bsw6fnUiL.jpg", "pdf": "rich-dad-poor-dad.pdf", "read": False},
    {"title": "The Power of Habit", "author": "Charles Duhigg", "cover": "https://m.media-amazon.com/images/I/81mO3rxvmtL.jpg", "pdf": "power-of-habit.pdf", "read": False},
    {"title": "Deep Work", "author": "Cal Newport", "cover": "https://m.media-amazon.com/images/I/61sOmzAaN7L.jpg", "pdf": "deep-work.pdf", "read": True},
    {"title": "The Subtle Art of Not Giving a F*ck", "author": "Mark Manson", "cover": "https://m.media-amazon.com/images/I/71QKQ9mwV7L.jpg", "pdf": "subtle-art.pdf", "read": False}
]

# 📂 Default Cover Image
DEFAULT_COVER = "https://via.placeholder.com/100x150.png?text=No+Cover"

# 🏠 Home Page
@app.route("/")
def home():
    total_books = len(books)
    read_books_count = sum(1 for book in books if book["read"])
    unread_books_count = total_books - read_books_count
    return render_template("index.html", books=books, total_books=total_books, read_books=read_books_count, unread_books=unread_books_count)

# 📖 Read a Book (Open PDF)
@app.route("/book/<int:book_index>")
def read_book(book_index):
    if 0 <= book_index < len(books):
        book = books[book_index]
        return redirect(url_for("serve_pdf", filename=book["pdf"]))
    return redirect("/")

# 📂 Serve PDF Files
@app.route("/pdfs/<filename>")
def serve_pdf(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# ➕ Add a New Book (with PDF upload)
@app.route("/add", methods=["POST"])
def add_book():
    try:
        title = request.form["title"]
        author = request.form["author"]
        cover = request.form.get("cover", DEFAULT_COVER)  # 🔥 Default cover if not provided
        pdf_file = request.files["pdf"]

        if pdf_file and pdf_file.filename.endswith(".pdf"):
            pdf_filename = pdf_file.filename
            pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)
            pdf_file.save(pdf_path)

            books.append({"title": title, "author": author, "cover": cover, "pdf": pdf_filename, "read": False})

        return redirect("/")
    
    except Exception as e:
        return f"Error adding book: {str(e)}"

# 🔄 Toggle Read/Unread
@app.route("/toggle_read/<int:book_index>")
def toggle_read(book_index):
    if 0 <= book_index < len(books):
        books[book_index]["read"] = not books[book_index]["read"]
    return redirect(url_for("home"))

# ❌ Delete a Book
@app.route("/delete/<int:book_index>")
def delete_book(book_index):
    if 0 <= book_index < len(books):
        del books[book_index]
    return redirect(url_for("home"))

# 📖 Show Read Books Only
@app.route("/read_books")
def show_read_books():
    read_books = [book for book in books if book["read"]]
    return render_template("index.html", books=read_books, total_books=len(read_books), read_books=len(read_books), unread_books=0)

# ❌ Show Unread Books Only
@app.route("/unread_books")
def show_unread_books():
    unread_books = [book for book in books if not book["read"]]
    return render_template("index.html", books=unread_books, total_books=len(unread_books), read_books=0, unread_books=len(unread_books))

# 🚀 Run the Server
if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload folder exists
    app.run(debug=True)
