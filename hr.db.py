import sqlite3

conn = sqlite3.connect("hr.db")
c = conn.cursor()

# Only create the table if it doesn't already exist
c.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        designation TEXT,
        salary REAL,
        location TEXT,
        hire_date TEXT
    )
''')

# Sample employee data
employees = [
    (1, "sneha", "HR", "Manager", 75000, "Hyderabad", "2021-01-15"),
    (2, "suma", "IT", "Developer", 68000, "Delhi", "2020-03-22"),
    (3, "mani", "HR", "Recruiter", 58000, "Mumbai", "2022-07-30"),
    (4, "raju", "Finance", "Accountant", 60000, "Chennai", "2019-11-12"),
    (5, "divya", "IT", "Tester", 55000, "Bangalore", "2021-05-10"),
    (6, "arjun", "HR", "Executive", 50000, "Hyderabad", "2023-01-05"),
    (7, "meena", "Marketing", "Lead", 72000, "Pune", "2020-06-18"),
    (8, "vamsi", "Sales", "Representative", 48000, "Delhi", "2022-08-22"),
    (9, "kiran", "Finance", "Analyst", 62000, "Mumbai", "2018-03-14"),
    (10, "latha", "IT", "Developer", 67000, "Chennai", "2019-09-09")
]

# Insert only if table is empty
c.execute("SELECT COUNT(*) FROM employees")
if c.fetchone()[0] == 0:
    c.executemany('INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?)', employees)

conn.commit()
conn.close()


