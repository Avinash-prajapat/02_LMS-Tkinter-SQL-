import tkinter as tk  # Import the tkinter library for creating GUI applications
from tkinter import messagebox  # Import messagebox for displaying pop-up messages
import mysql.connector  # Import mysql.connector for connecting to MySQL

# Connect to the MySQL database
connection = mysql.connector.connect(
    host="localhost",  # Hostname of the MySQL server
    user="root",  # MySQL username (replace with your own)
    password="Avinash@9199",  # MySQL password (replace with your own)
    database="library_db"  # The database to connect to
)
cursor = connection.cursor()  # Create a cursor object to execute SQL queries

# Create a class for the Library Management GUI
class LibraryGUI:
    def __init__(self, root):
        root.title("Library Management System")  # Set the window title

        # Frame for Adding Books
        self.add_frame = tk.Frame(root)  # Create a frame for adding books
        self.add_frame.pack(pady=10)  # Pack the frame with padding

        # Labels and Entry fields for book details
        tk.Label(self.add_frame, text="Book ID").grid(row=0, column=0)  # Book ID label
        self.book_id_entry = tk.Entry(self.add_frame)  # Entry field for Book ID
        self.book_id_entry.grid(row=0, column=1)  # Position the Book ID entry

        tk.Label(self.add_frame, text="Title").grid(row=1, column=0)  # Title label
        self.title_entry = tk.Entry(self.add_frame)  # Entry field for Title
        self.title_entry.grid(row=1, column=1)  # Position the Title entry

        tk.Label(self.add_frame, text="Author").grid(row=2, column=0)  # Author label
        self.author_entry = tk.Entry(self.add_frame)  # Entry field for Author
        self.author_entry.grid(row=2, column=1)  # Position the Author entry

        tk.Label(self.add_frame, text="Category").grid(row=3, column=0)  # Category label
        self.category_entry = tk.Entry(self.add_frame)  # Entry field for Category
        self.category_entry.grid(row=3, column=1)  # Position the Category entry

        # Button to Add Book
        self.add_button = tk.Button(self.add_frame, text="Add Book", command=self.add_book)  # Button for adding a book
        self.add_button.grid(row=4, columnspan=2, pady=5)  # Position the button

        # Frame for Issuing Books
        self.issue_frame = tk.Frame(root)  # Create a frame for issuing books
        self.issue_frame.pack(pady=10)  # Pack the frame with padding

        tk.Label(self.issue_frame, text="Book ID to Issue").grid(row=0, column=0)  # Label for issuing book
        self.issue_id_entry = tk.Entry(self.issue_frame)  # Entry field for Book ID to issue
        self.issue_id_entry.grid(row=0, column=1)  # Position the entry field

        # Button to Issue Book
        self.issue_button = tk.Button(self.issue_frame, text="Issue Book", command=self.issue_book)  # Button for issuing a book
        self.issue_button.grid(row=1, columnspan=2, pady=5)  # Position the button

        # Frame for Returning Books
        self.return_frame = tk.Frame(root)  # Create a frame for returning books
        self.return_frame.pack(pady=10)  # Pack the frame with padding

        tk.Label(self.return_frame, text="Book ID to Return").grid(row=0, column=0)  # Label for returning book
        self.return_id_entry = tk.Entry(self.return_frame)  # Entry field for Book ID to return
        self.return_id_entry.grid(row=0, column=1)  # Position the entry field

        # Button to Return Book
        self.return_button = tk.Button(self.return_frame, text="Return Book", command=self.return_book)  # Button for returning a book
        self.return_button.grid(row=1, columnspan=2, pady=5)  # Position the button

        # Frame for Displaying Books
        self.display_frame = tk.Frame(root)  # Create a frame for displaying books
        self.display_frame.pack(pady=10)  # Pack the frame with padding

        # Button to Display Books
        self.display_button = tk.Button(self.display_frame, text="Display Books", command=self.display_books)  # Button to display all books
        self.display_button.pack()  # Position the button

        # Text area to show book details
        self.display_area = tk.Text(self.display_frame, height=10, width=50)  # Text area for displaying book information
        self.display_area.pack(pady=5)  # Pack the text area

    # Method to add a book to the database
    def add_book(self):
        # Get data from entry fields
        book_id = self.book_id_entry.get()  # Retrieve Book ID from entry
        title = self.title_entry.get()  # Retrieve Title from entry
        author = self.author_entry.get()  # Retrieve Author from entry
        category = self.category_entry.get()  # Retrieve Category from entry

        # SQL query to insert book into the database
        query = "INSERT INTO books (book_id, title, author, category) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(query, (book_id, title, author, category))  # Execute the insert query
            connection.commit()  # Commit the transaction to save changes
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")  # Show success message
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")  # Show error message

        # Clear entry fields after adding
        self.clear_entries()

    # Method to issue a book to a user
    def issue_book(self):
        book_id = self.issue_id_entry.get()  # Retrieve Book ID to issue
        # SQL query to update book availability
        query = "UPDATE books SET is_available = FALSE WHERE book_id = %s AND is_available = TRUE"
        cursor.execute(query, (book_id,))  # Execute the update query
        if cursor.rowcount > 0:  # Check if any rows were updated
            connection.commit()  # Commit the transaction
            messagebox.showinfo("Success", f"Book with ID {book_id} issued successfully!")  # Show success message
        else:
            messagebox.showwarning("Warning", "Book not available or invalid ID.")  # Show warning message

    # Method to return a book to the library
    def return_book(self):
        book_id = self.return_id_entry.get()  # Retrieve Book ID to return
        # SQL query to update book availability
        query = "UPDATE books SET is_available = TRUE WHERE book_id = %s AND is_available = FALSE"
        cursor.execute(query, (book_id,))  # Execute the update query
        if cursor.rowcount > 0:  # Check if any rows were updated
            connection.commit()  # Commit the transaction
            messagebox.showinfo("Success", f"Book with ID {book_id} returned successfully!")  # Show success message
        else:
            messagebox.showwarning("Warning", "Invalid book ID or the book was not issued.")  # Show warning message

    # Method to display all books in the library
    def display_books(self):
        # SQL query to select all available books
        query = "SELECT * FROM books WHERE is_available = TRUE"
        cursor.execute(query)  # Execute the select query
        books = cursor.fetchall()  # Fetch all results from the executed query
        self.display_area.delete(1.0, tk.END)  # Clear the display area before showing new results
        if not books:  # Check if there are no books
            self.display_area.insert(tk.END, "No books available in the library.")  # Display message if no books
        else:
            for book in books:  # Iterate through each book
                self.display_area.insert(tk.END, f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Category: {book[3]}\n")  # Display book details

    # Method to clear entry fields after adding or issuing
    def clear_entries(self):
        self.book_id_entry.delete(0, tk.END)  # Clear the Book ID entry field
        self.title_entry.delete(0, tk.END)  # Clear the Title entry field
        self.author_entry.delete(0, tk.END)  # Clear the Author entry field
        self.category_entry.delete(0, tk.END)  # Clear the Category entry field
        self.issue_id_entry.delete(0, tk.END)  # Clear the Book ID to issue entry field
        self.return_id_entry.delete(0, tk.END)  # Clear the Book ID to return entry field

# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()  # Initialize the Tkinter window
    app = LibraryGUI(root)  # Create an instance of the LibraryGUI class
    root.mainloop()  # Start the GUI event loop
    cursor.close()  # Close the cursor
    connection.close()  # Close the database connection
