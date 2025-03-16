import streamlit as st
import json
import os

# File to store the library data
data_file = 'library.txt'

# Function to load the library from a file
def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

# Function to save the library to a file
def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file)

# Function to add a new book to the library
def add_book(library):
    st.header('Add a New Book')
    title = st.text_input('Title')
    author = st.text_input('Author')
    year = st.text_input('Publication Year')
    genre = st.text_input('Genre')
    read = st.checkbox('Have you read the book?')

    if st.button('Add Book'):
        new_book = {'title': title, 'author': author, 'year': year, 'genre': genre, 'read': read}
        library.append(new_book)
        save_library(library)
        st.success(f'Book "{title}" added successfully!')



# Function to remove a book from the library
def remove_book(library):
    st.header('Remove a Book')
    title = st.text_input('Enter the title of the book to remove')
    if st.button('Remove Book'):
        initial_length = len(library)
        library = [book for book in library if book['title'].lower() != title.lower()]
        if len(library) < initial_length:
            save_library(library)
            st.success(f'Book "{title}" removed successfully!')
        else:
            st.warning(f'Book "{title}" not found in the library.')

# Function to search for books
def search_library(library):
    st.header('Search for a Book')
    search_by = st.radio('Search by', ('Title', 'Author'))
    search_term = st.text_input(f'Enter the {search_by.lower()}')

    if st.button('Search'):
        results = [book for book in library if search_term.lower() in book[search_by.lower()].lower()]
        if results:
            st.write('Matching Books:')
            for idx, book in enumerate(results, 1):
                status = "Read" if book['read'] else "Unread"
                st.write(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
        else:
            st.warning(f'No books found matching to author "{search_term}".')

# Function to display all books
def display_all_books(library):
    st.header('All Books in the Library')
    if library:
        for idx, book in enumerate(library, 1):
            status = "Read" if book['read'] else "Unread"
            st.write(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        st.info('The library is empty.')

# Function to display library statistics
def display_statistics(library):
    st.header('Library Statistics')
    total_books = len(library)
    read_books = len([book for book in library if book['read']])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0

    st.write(f'Total books: {total_books}')
    st.write(f'Percentage of reading: {percentage_read:.2f}%')

# Main function to handle navigation
def main():
    st.title('📚 Personal Book Library Manager')

    library = load_library()

    menu = ['Add Book', 'Remove Book', 'Search Book', 'Display All Books', 'Statistics']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Add Book':
        add_book(library)
    elif choice == 'Remove Book':
        remove_book(library)
    elif choice == 'Search Book':
        search_library(library)
    elif choice == 'Display All Books':
        display_all_books(library)
    elif choice == 'Statistics':
        display_statistics(library)

if __name__ == '__main__':
    main()