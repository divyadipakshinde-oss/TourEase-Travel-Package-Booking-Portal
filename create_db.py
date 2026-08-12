import sqlite3

# Connect Database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user'
)
""")

# Packages Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_name TEXT NOT NULL,
    destination TEXT NOT NULL,
    duration TEXT,
    price REAL,
    description TEXT,
    image TEXT,
    seats INTEGER,
    category TEXT,
    transport Text,
    hotel Text,
    meals Text,
    sightseeing Text

)
""")

# Bookings Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    package_name TEXT NOT NULL,
    travel_date TEXT NOT NULL,
    travelers INTEGER NOT NULL,
    message TEXT,
    booking_date TEXT
)
""")

# Contact Messages Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    subject TEXT,
    message TEXT
)
""")

# Testimonials Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS testimonials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    review TEXT,
    rating INTEGER
)
""")

# Destinations Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS destinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_name TEXT,
    image TEXT,
    description TEXT
)
""")

# Invoices Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    invoice_number TEXT,
    amount REAL
)
""")

# Save Changes
conn.commit()
conn.close()

print("Database created successfully!")