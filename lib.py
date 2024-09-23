import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Publishers (
    publisher_id INTEGER PRIMARY KEY,
    Publisher_Name TEXT NOT NULL UNIQUE,
    Publisher_Address TEXT NOT NULL,
    Publisher_Phonenumber TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
    Book_id INTEGER PRIMARY KEY,
    Book_Title TEXT NOT NULL,
    Book_Publisher_Name TEXT NOT NULL,
    FOREIGN KEY (Book_Publisher_Name) REFERENCES Publishers (Publisher_Name)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS library_branch (
    library_branch_Branch_id INTEGER PRIMARY KEY,
    library_branch_BranchName TEXT NOT NULL UNIQUE,
    library_branch_BranchAddress TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Borrower (
    borrower_Card_Number INTEGER PRIMARY KEY,
    Borrower_Name TEXT NOT NULL,
    Borrower_Address TEXT NOT NULL,
    Borrower_Phone_number TEXT NOT NULL UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Book_loans (
    Book_Loans_id INTEGER PRIMARY KEY,
    Book_loans_Book_id INTEGER,
    Book_loans_Branch_id INTEGER,
    Book_loans_Card_No INTEGER,
    Book_loans_Date_Out TEXT NOT NULL,
    Book_loans_Due_Date TEXT NOT NULL,
    FOREIGN KEY (Book_loans_Book_id) REFERENCES Books (Book_id),
    FOREIGN KEY (Book_loans_Branch_id) REFERENCES library_branch (library_branch_Branch_id),
    FOREIGN KEY (Book_loans_Card_No) REFERENCES Borrower (borrower_Card_Number)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Book_Authors (
    Book_Author_id INTEGER PRIMARY KEY,
    Book_Authors_Book_id INTEGER,
    Book_Author_Name TEXT NOT NULL,
    FOREIGN KEY (Book_Authors_Book_id) REFERENCES Books (Book_id)
)
''')

# Function to insert data safely
def insert_data(query, data):
    try:
        cursor.executemany(query, data)
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")

# Insert data into Publishers table
insert_data('''
    INSERT INTO Publishers(publisher_id, Publisher_Name, Publisher_Address, Publisher_Phonenumber)
    VALUES (?, ?, ?, ?)
''', [
    (1, 'Penguin Random House India', '1 Nehru Place, New Delhi, Delhi', '+91-1234567890'),
    (2, 'HarperCollins India', '10 Connaught Place, New Delhi, Delhi', '+91-2345678901'),
    (3, 'Rupa Publications India', '20 Lajpat Nagar, New Delhi, Delhi', '+91-3456789012'),
    (4, 'SAGE Publications India', '30 Vasant Vihar, New Delhi, Delhi', '+91-4567890123'),
    (5, 'Oxford University Press India', '40 Daryaganj, New Delhi, Delhi', '+91-5678901234'),
    (6, 'Bloomsbury Publishing India', '50 Okhla, New Delhi, Delhi', '+91-6789012345'),
    (7, 'Westland Publications India', '60 Rajouri Garden, New Delhi, Delhi', '+91-7890123456'),
    (8, 'Pustak Mahal Publications India', '70 Paharganj, New Delhi, Delhi', '+91-8901234567'),
    (9, 'Hachette India', '80 Saket, New Delhi, Delhi', '+91-9012345678'),
    (10, 'Aleph Book Company', '90 Vasant Kunj, New Delhi, Delhi', '+91-9876543210')
])

# Insert data into Books table
insert_data('''
    INSERT INTO Books (Book_id, Book_Title, Book_Publisher_Name)
    VALUES (?, ?, ?)
''', [
    (1, 'The Sorcerer\'s Stone', 'Penguin Random House India'),
    (2, 'The Chamber of Secrets', 'Penguin Random House India'),
    (3, 'The Prisoner of Azkaban', 'Penguin Random House India'),
    (4, 'The Goblet of Fire', 'Penguin Random House India'),
    (5, 'The Order of the Phoenix', 'Penguin Random House India'),
    (6, 'The Half-Blood Prince', 'Penguin Random House India'),
    (7, 'The Deathly Hallows', 'Penguin Random House India'),
    (8, 'The Dark Knight', 'Bloomsbury Publishing India'),
    (9, 'The Man of Steel', 'Bloomsbury Publishing India'),
    (10, 'The Amazing Spider-Man', 'Rupa Publications India'),
    (11, 'The Avengers Assemble', 'Rupa Publications India'),
    (12, 'The Vampire Diaries: The Awakening', 'Penguin Random House India'),
    (13, 'The Vampire Diaries: The Struggle', 'Penguin Random House India'),
    (14, 'The Vampire Diaries: The Fury', 'Penguin Random House India'),
    (15, 'The Vampire Diaries: Dark Reunion', 'Penguin Random House India'),
    (16, 'The Lord of the Rings: The Fellowship of the Ring', 'Bloomsbury Publishing India'),
    (17, 'The Lord of the Rings: The Two Towers', 'Bloomsbury Publishing India'),
    (18, 'The Lord of the Rings: The Return of the King', 'Bloomsbury Publishing India'),
    (19, 'The Hobbit', 'Rupa Publications India'),
    (20, 'The Silmarillion', 'Rupa Publications India')
])

# Insert data into library_branch table
insert_data('''
    INSERT INTO library_branch(library_branch_Branch_id, library_branch_BranchName, library_branch_BranchAddress)
    VALUES (?, ?, ?)
''', [
    (1, 'Central Library', '100 Main Street, New Delhi, Delhi'),
    (2, 'East Side Library', '200 East Road, New Delhi, Delhi'),
    (3, 'West Side Library', '300 West Road, New Delhi, Delhi'),
    (4, 'North Library', '400 North Avenue, New Delhi, Delhi'),
    (5, 'South Library', '500 South Lane, New Delhi, Delhi'),
    (6, 'Gurgaon Library', '50 MG Road, Gurgaon, Haryana'),
    (7, 'Faridabad Central Library', '15 Sector 14, Faridabad, Haryana'),
    (8, 'Noida International Library', '25 Sector 62, Noida, Uttar Pradesh'),
    (9, 'Greater Noida Library', '35 Greater Noida, Uttar Pradesh'),
    (10, 'Delhi South Library', '45 Hauz Khas, New Delhi, Delhi')
])

# Insert data into Borrower table
insert_data('''
    INSERT INTO Borrower (borrower_Card_Number, Borrower_Name, Borrower_Address, Borrower_Phone_number) 
    VALUES (?, ?, ?, ?)
''', [
    (1, 'Amit Sharma', '123 Main St, New Delhi', '+911234567890'),
    (2, 'Sneha Gupta', '456 Elm St, New Delhi', '+919876543210'),
    (3, 'Rahul Verma', '789 Maple St, New Delhi', '+911234567891'),
    (4, 'Nisha Kumar', '321 Oak St, New Delhi', '+919876543211'),
    (5, 'Vikram Singh', '654 Pine St, New Delhi', '+911234567892'),
    (6, 'Saurabh Kumar', '1101 QRS Lane, Delhi', '+91785412396'),
    (7, 'Tanvi Bansal', '1202 TUV Road, Noida', '+91875624185'),
    (8, 'Karan Singh', '1303 WXY Street, Ghaziabad', '+91712345678'),
    (9, 'Riya Sharma', '1404 ABC Avenue, Faridabad', '+91987654322'),
    (10, 'Mohit Chawla', '1505 DEF Lane, Gurgaon', '+91123456700')
])

# Insert data into Book_loans table
insert_data('''
    INSERT INTO Book_loans (Book_Loans_id, Book_loans_Book_id, Book_loans_Branch_id, Book_loans_Card_No, Book_loans_Date_Out, Book_loans_Due_Date)
    VALUES (?, ?, ?, ?, ?, ?)
''', [
    (1, 1, 1, 1, '2023-09-01', '2023-09-15'),
    (2, 2, 2, 2, '2023-09-02', '2023-09-16'),
    (3, 3, 1, 3, '2023-09-03', '2023-09-17'),
    (4, 4, 3, 4, '2023-09-04', '2023-09-18'),
    (5, 5, 2, 5, '2023-09-05', '2023-09-19'),
    (6, 6, 1, 6, '2023-09-06', '2023-09-20'),
    (7, 7, 3, 7, '2023-09-07', '2023-09-21'),
    (8, 8, 2, 8, '2023-09-08', '2023-09-22'),
    (9, 9, 1, 9, '2023-09-09', '2023-09-23'),
    (10, 10, 3, 10, '2023-09-10', '2023-09-24')
])

# Insert data into Book_Authors table
insert_data('''
    INSERT INTO Book_Authors (Book_Authors_Book_id, Book_Author_Name)
    VALUES (?, ?)
''', [
    (1, 'J.K. Rowling'),  # The Sorcerer's Stone
    (2, 'J.K. Rowling'),  # The Chamber of Secrets
    (3, 'J.K. Rowling'),  # The Prisoner of Azkaban
    (4, 'J.K. Rowling'),  # The Goblet of Fire
    (5, 'J.K. Rowling'),  # The Order of the Phoenix
    (6, 'J.K. Rowling'),  # The Half-Blood Prince
    (7, 'J.K. Rowling'),  # The Deathly Hallows
    (8, 'Christopher Nolan'),  # The Dark Knight
    (9, 'David S. Goyer'),  # The Man of Steel
    (10, 'Stan Lee'),  # The Amazing Spider-Man
    (11, 'Stan Lee'),  # The Avengers Assemble
    (12, 'L.J. Smith'),  # The Vampire Diaries: The Awakening
    (13, 'L.J. Smith'),  # The Vampire Diaries: The Struggle
    (14, 'L.J. Smith'),  # The Vampire Diaries: The Fury
    (15, 'L.J. Smith'),  # The Vampire Diaries: Dark Reunion
    (16, 'J.R.R. Tolkien'),  # The Lord of the Rings: The Fellowship of the Ring
    (17, 'J.R.R. Tolkien'),  # The Lord of the Rings: The Two Towers
    (18, 'J.R.R. Tolkien'),  # The Lord of the Rings: The Return of the King
    (19, 'J.R.R. Tolkien'),  # The Hobbit
    (20, 'J.R.R. Tolkien')   # The Silmarillion
])


# Commit changes and close the connection
conn.commit()
conn.close()

print("Database created and data inserted successfully.")


