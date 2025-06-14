import sqlite3

try:
    # Connect to SQLite DB (creates hr.db if it doesn't exist)
    conn = sqlite3.connect("hr.db")
    cursor = conn.cursor()

    # Drop table if it already exists
    cursor.execute("DROP TABLE IF EXISTS employees")

    # Create new table
    cursor.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        designation TEXT,
        salary INTEGER,
        location TEXT,
        hire_date TEXT
    )
    """)

    # Employee data
    employees = [
        (1, "Alice Johnson", "HR", "HR Manager", 75000, "New York", "2018-03-12"),
        (2, "Bob Smith", "HR", "HR Executive", 60000, "New York", "2019-07-23"),
        (3, "Carla James", "HR", "HR Analyst", 58000, "Los Angeles", "2020-01-15"),
        (4, "David Lee", "HR", "HR Coordinator", 55000, "Chicago", "2021-05-10"),
        (5, "Eva Brown", "HR", "HR Specialist", 72000, "Miami", "2017-10-01"),
        (6, "Frank Wright", "HR", "HR Generalist", 68000, "Austin", "2016-08-22"),
        (7, "Grace Kim", "HR", "HR Director", 90000, "Boston", "2015-06-05"),
        (8, "Henry Miller", "HR", "HR Consultant", 77000, "Denver", "2020-11-30"),
        (9, "Isla Davis", "HR", "Recruiter", 61000, "San Diego", "2022-02-17"),
        (10, "Jack Wilson", "HR", "Compensation Analyst", 88000, "Seattle", "2019-09-14"),
        (11, "Laura Smith", "IT", "Software Engineer", 95000, "New York", "2019-08-12"),
        (12, "Mark Brown", "IT", "Data Analyst", 85000, "San Francisco", "2020-05-23"),
        (13, "Nina Garcia", "IT", "DevOps Engineer", 92000, "Austin", "2021-01-05"),
        (14, "Owen Carter", "IT", "Frontend Developer", 87000, "Chicago", "2018-11-30"),
        (15, "Paul Adams", "IT", "Backend Developer", 88000, "Los Angeles", "2017-06-25"),
        (16, "Quinn Parker", "IT", "Database Admin", 91000, "Seattle", "2016-12-15"),
        (17, "Rachel Green", "IT", "IT Manager", 99000, "Denver", "2015-10-10"),
        (18, "Steve Nolan", "IT", "UX Designer", 83000, "Miami", "2022-03-17"),
        (19, "Tina White", "IT", "Product Manager", 98000, "Boston", "2019-09-01"),
        (20, "Uma Patel", "IT", "AI Specialist", 102000, "San Diego", "2023-01-09"),
        (21, "Victor Cruz", "Finance", "Accountant", 72000, "New York", "2018-04-11"),
        (22, "Wendy Hall", "Finance", "Financial Analyst", 76000, "Chicago", "2019-07-21"),
        (23, "Xavier King", "Finance", "Treasurer", 82000, "Miami", "2020-12-01"),
        (24, "Yara Evans", "Finance", "CFO", 120000, "San Francisco", "2015-08-14"),
        (25, "Zane Brooks", "Finance", "Finance Manager", 95000, "Seattle", "2016-10-10"),
        (26, "Alan Moore", "Finance", "Auditor", 79000, "Denver", "2021-06-18"),
        (27, "Betty Adams", "Finance", "Controller", 86000, "Boston", "2017-11-29"),
        (28, "Chris Young", "Finance", "Risk Manager", 90000, "Austin", "2020-04-03"),
        (29, "Diana Grant", "Finance", "Budget Analyst", 73000, "Los Angeles", "2022-02-27"),
        (30, "Eli Watson", "Finance", "Investment Analyst", 88000, "San Diego", "2019-05-13"),
        (31, "Fiona Shaw", "Marketing", "Marketing Manager", 88000, "Chicago", "2018-07-01"),
        (32, "George Hill", "Marketing", "SEO Specialist", 70000, "Boston", "2019-10-22"),
        (33, "Holly West", "Marketing", "Content Writer", 67000, "Austin", "2021-02-14"),
        (34, "Ian Knight", "Marketing", "Social Media Manager", 72000, "Seattle", "2020-08-11"),
        (35, "Jasmine Lin", "Marketing", "Graphic Designer", 69000, "New York", "2017-03-25"),
        (36, "Kevin Blake", "Marketing", "Brand Manager", 83000, "Miami", "2016-06-30"),
        (37, "Lily Fox", "Marketing", "PR Specialist", 76000, "Denver", "2022-01-19"),
        (38, "Mike Rose", "Marketing", "Ad Campaign Lead", 82000, "Los Angeles", "2019-04-10"),
        (39, "Nora Kim", "Marketing", "Event Coordinator", 71000, "San Diego", "2018-12-07"),
        (40, "Oscar Dean", "Marketing", "Market Researcher", 75000, "San Francisco", "2020-10-05"),
        (41, "Pamela Holt", "Operations", "Ops Manager", 93000, "Austin", "2017-09-03"),
        (42, "Quincy Reed", "Operations", "Logistics Lead", 87000, "Chicago", "2016-11-15"),
        (43, "Rita Long", "Operations", "Facilities Manager", 89000, "Seattle", "2015-01-08"),
        (44, "Sam Watts", "Operations", "Operations Analyst", 79000, "Miami", "2018-06-20"),
        (45, "Tasha Owen", "Operations", "Inventory Specialist", 73000, "Los Angeles", "2019-03-03"),
        (46, "Ulysses Nash", "Operations", "Process Engineer", 82000, "Denver", "2021-07-09"),
        (47, "Vanessa Diaz", "Operations", "Quality Manager", 88000, "San Francisco", "2020-05-28"),
        (48, "Walter Shaw", "Operations", "Procurement Officer", 80000, "Boston", "2019-11-16"),
        (49, "Xena Voss", "Operations", "Warehouse Manager", 85000, "New York", "2022-09-04"),
        (50, "Yusuf Khan", "Operations", "Fleet Manager", 81000, "San Diego", "2018-02-13")
    ]

    # Insert data
    cursor.executemany("""
    INSERT INTO employees (id, name, department, designation, salary, location, hire_date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, employees)

    # Save changes
    conn.commit()
    print("✅ HR database created with 50 employees.")

except sqlite3.Error as e:
    print("❌ SQLite Error:", e)

finally:
    # Close connection
    if conn:
        conn.close()
