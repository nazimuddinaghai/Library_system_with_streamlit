
class Book:
    def __init__(self, title, author, book_id, copies):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.total_copies = copies
        self.available_copies = copies
    def show(self):
        return {
            "Book ID": self.book_id,
            "Title": self.title,
            "Author": self.author,
            "Available Copies": f"{self.available_copies} / {self.total_copies}",
        }
class Library:
    def __init__(self):
        self.books = {}
        self.borrowed_books = {}
    def add_book(self, book):
        if book.book_id in self.books:
            old_book = self.books[book.book_id]
            old_book.total_copies += book.total_copies
            old_book.available_copies += book.total_copies
        else:
            self.books[book.book_id] = book
    def search_by_title(self, text):
        result = []
        for book in self.books.values():
            if text.lower() in book.title.lower():
                result.append(book)
        return result
    def search_by_author(self, text):
        result = []
        for book in self.books.values():
            if text.lower() in book.author.lower():
                result.append(book)
        return result
    def borrow_book(self, user, book_id):
        if book_id not in self.books:
            return False
        book = self.books[book_id]
        if book.available_copies <= 0:
            return False
        book.available_copies -= 1
        if user not in self.borrowed_books:
            self.borrowed_books[user] = []
        self.borrowed_books[user].append(book_id)
        return True
    def return_book(self, user, book_id):
        if user not in self.borrowed_books:
            return False
        if book_id not in self.borrowed_books[user]:
            return False
        self.borrowed_books[user].remove(book_id)
        self.books[book_id].available_copies += 1
        return True
st.set_page_config(page_title="Digital Library")
st.title(" Digital Library System")
if "library" not in st.session_state:
    st.session_state.library = Library()
library = st.session_state.library
menu = st.sidebar.selectbox(
    "Choose an option",
    (
        "Add Book",
        "Search by Title",
        "Search by Author",
        "Borrow Book",
        "Return Book",
        "View All Books",
    ),)
if menu == "Add Book":
    st.subheader("Add New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author Name")
    book_id = st.text_input("Book ID")
    copies = st.number_input("Total Copies", min_value=1, step=1)
    if st.button("Add Book"):
        if title == "" or author == "" or book_id == "":
            st.error("Please fill all fields")
        else:
            book = Book(title, author, book_id, copies)
            library.add_book(book)
            st.success("Book added successfully")
elif menu == "Search by Title":
    st.subheader("Search Book by Title")
    text = st.text_input("Enter title keyword")
    if st.button("Search"):
        result = library.search_by_title(text)
        if result:
            st.table([b.show() for b in result])
        else:
            st.warning("No book found")
elif menu == "Search by Author":
    st.subheader("Search Book by Author")
    text = st.text_input("Enter author name")
    if st.button("Search"):
        result = library.search_by_author(text)
        if result:
            st.table([b.show() for b in result])
        else:
            st.warning("No book found")
elif menu == "Borrow Book":
    st.subheader(" Borrow Book")
    user = st.text_input("Your Name")
    book_id = st.text_input("Book ID")
    if st.button("Borrow"):
        success = library.borrow_book(user, book_id)
        if success:
            st.success("Book borrowed successfully")
        else:
            st.error("Book not available or wrong ID")
    st.subheader("Return Book")
    user = st.text_input("Your Name")
    book_id = st.text_input("Book ID")
    if st.button("Return"):
        success = library.return_book(user, book_id)
        if success:
            st.success("Book returned successfully")
        else:
            st.error("Invalid return")
elif menu == "View All Books":
    st.subheader(" All Available Books")
    if library.books:
        st.table([b.show() for b in library.books.values()])
    else:
        st.info("No books available in library")
