from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3

import google.generativeai as genai

# Load all the environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the Google Gemini model and provide SQL query as a response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve data with a query generated from SQL db
def read_sql_query(sqlcmd, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    print("Executing SQL Command:", sqlcmd)

    cur.execute(sqlcmd)
    rows = cur.fetchall()
    conn.commit()
 
    conn.close()
    for row in rows:
        print(row)    
    return rows


# Function to check existing tables
def check_tables_exist(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    conn.close()
    return tables


# Prompt for the model
prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The SQL database has the name LIBRARY and has the following tables and columns:

    1. Publishers: publisher_id, Publisher_Name, Publisher_Address, Publisher_Phonenumber
    2. Books: Book_id, Book_Title, Book_Publisher_Name
    3. library_branch: library_branch_Branch_id, library_branch_BranchName, library_branch_BranchAddress
    4. Borrower: borrower_Card_Number, Borrower_Name, Borrower_Address, Borrower_Phone_number
    5. Book_loans: Book_Loans_id, Book_loans_Book_id, Book_loans_Branch_id, Book_loans_Card_No, Book_loans_Date_Out, Book_loans_Due_Date
    6. Book_Authors: Book_Author_id, Book_Authors_Book_id, Book_Author_Name

    Examples:
    Example 1 - How many publishers are in the database?
    The SQL command will be: SELECT COUNT(*) FROM Publishers;

    Example 2 - List all books published by Penguin Random House India.
    The SQL command will be: SELECT * FROM Books WHERE Book_Publisher_Name = "Penguin Random House India";

    Example 3 - Get the names of all borrowers.
    The SQL command will be: SELECT Borrower_Name FROM Borrower;

    Example 4 - Find all books written by J.K. Rowling.
    The SQL command will be: SELECT Books.Book_Title FROM Books
    JOIN Book_Authors ON Books.Book_id = Book_Authors.Book_Authors_Book_id
    WHERE Book_Author_Name = "J.K. Rowling";

    Example 5 - How many books are loaned out?
    The SQL command will be: SELECT COUNT(*) FROM Book_loans;

    Example 6 - Show the loan details for the book titled "The Hobbit".
    The SQL command will be: SELECT * FROM Book_loans
    WHERE Book_loans_Book_id = (SELECT Book_id FROM Books WHERE Book_Title = "The Hobbit");

    Example 7 - Which library branch has the address '100 Main Street, New Delhi, Delhi'?
    The SQL command will be: SELECT * FROM library_branch
    WHERE library_branch_BranchAddress = "100 Main Street, New Delhi, Delhi";

    Example 8 - Find the due date for the book loan with ID 1.
    The SQL command will be: SELECT Book_loans_Due_Date FROM Book_loans WHERE Book_Loans_id = 1;

    Example 9 - List all branches in the library.
    The SQL command will be: SELECT * FROM library_branch;

    Example 10 - Get all books loaned to the borrower named 'Amit Sharma'.
    The SQL command will be: SELECT Books.Book_Title FROM Book_loans
    JOIN Books ON Book_loans.Book_loans_Book_id = Books.Book_id
    WHERE Book_loans_Card_No = (SELECT borrower_Card_Number FROM Borrower WHERE Borrower_Name = "Amit Sharma");
    The SQL code should not have ''' in beginning or end and SQL word in the output.
    """
]

# STREAMLIT APP
st.set_page_config(page_title="I can Retrieve data for you, Just ask!")
st.title("🔍 Query Your Database with AI")
# Description of the database
st.subheader("About the Database")
st.write("This application showcases a library database containing information about books, authors, publishers, library branches, and borrowers. You can query the database using natural language to retrieve specific information.")

# Expander for sample questions
with st.expander("💡 Sample Questions", expanded=False):
    st.markdown("""
    Here are some example questions you can ask:
    - "Show all books published by 'Penguin Random House India'."
    - "List all authors of the book 'The Hobbit'."
    - "Retrieve all borrowers with active loans."
    - "What are the details of the book with ID 5?"
    - "Find all branches of the library located in 'Delhi'."
    - "Show all publishers in the database."
    - "Retrieve the borrowing history of 'Amit Sharma'."
    """)

question = st.text_input("Tell me what you’d like from your database: ", key="input")
submit = st.button("Ask the Question!")

if submit:
    response = get_gemini_response(question, prompt)
    print("Generated SQL Query:", response.strip())

    # Replace double quotes with single quotes around the publisher name
    response = response.replace('"', "'")

    try:
        print("Executing SQL Command:", response)  # Print the final SQL command
        data = read_sql_query(response, "library.db")
        st.subheader("Retrieval Complete! Here is your data:")

        if data:
            for row in data:
                st.write(row)
        else:
            st.warning("No Data Found")

    except sqlite3.OperationalError as e:
        st.error(f"SQL Error: {str(e)}")
        print(f"SQL Error: {str(e)}")


