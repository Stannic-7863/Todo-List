import sqlite3

data_base_path = './data/task_data/task_database.db'
connection = sqlite3.connect(data_base_path)
cursor = connection.cursor()

def main():
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                time_created TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS priority (
                priority_id INTEGER PRIMARY KEY AUTOINCREMENT,
                current_priority TEXT
        )    
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS status (
                status_id INTEGER PRIMARY KEY AUTOINCREMENT,
                current_status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS main (
                task_id INTEGER PRIMARY KEY,
                priority_id INTEGER NOT NULL,
                status_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,

                FOREIGN KEY (task_id) REFERENCES tasks(task_id),
                FOREIGN KEY (priority_id) REFERENCES priority(priority_id),
                FOREIGN KEY (status_id) REFERENCES status(status_id),
                FOREIGN KEY (category_id) REFERENCES category(category_id)
    )   
    """)

    connection.commit()


def commit_new_task_data(task_name, time_created, current_priority, current_status, category):
    main()
    cursor.execute("INSERT INTO tasks (task_name, time_created) VALUES (?, ?)", (task_name, time_created))
    task_id = cursor.lastrowid
    cursor.execute("INSERT INTO priority (current_priority) VALUES (?)", (current_priority,))
    prioirty_id = cursor.lastrowid
    cursor.execute("INSERT INTO status (current_status) VALUES (?)", (current_status,))
    status_id = cursor.lastrowid
    cursor.execute("INSERT INTO category (category) VALUES (?)", (category,))
    category_id = cursor.lastrowid
    cursor.execute("INSERT INTO main (task_id, priority_id, status_id, category_id) VALUES (?,?,?,?)", (task_id, prioirty_id, status_id, category_id))
    connection.commit()

    return task_id

def change_priority_db(prev_priority, new_priority, task_id):
    cursor.execute("""
    SELECT priority_id 
    FROM main
    INNER JOIN priority USING(priority_id)
    WHERE task_id = ? """, (task_id,))

    result = cursor.fetchone()
    for item in result:
        if item:
            priority_id = item

    cursor.execute("""
    UPDATE priority 
    SET current_priority = ? 
    WHERE priority_id = ? AND current_priority = ?
    """, (new_priority, priority_id, prev_priority))

    connection.commit()

def change_status_db(prev_status, new_status, task_id):
    cursor.execute("""
    SELECT status_id 
    FROM main
    INNER JOIN status USING(status_id)
    WHERE task_id = ? """, (task_id,))

    result = cursor.fetchone()
    for item in result:
        if item:
            status_id = item

    cursor.execute("""
    UPDATE status
    SET current_status = ? 
    WHERE status_id = ? AND current_status = ?
    """, (new_status, status_id, prev_status))

    connection.commit()

def fetch_data():
    cursor.execute("""
    SELECT task_name, current_priority, current_status, category, task_id
    FROM main
    INNER JOIN tasks USING(task_id)
    INNER JOIN priority USING(priority_id)
    INNER JOIN status USING(status_id)
    INNER JOIN category USING(category_id)
""")
    results = cursor.fetchall()

    return results


if __name__ == '__main__':
    main()