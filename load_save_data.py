import sqlite3

data_base_path = './data/task_data/task_database.db'
connection = sqlite3.connect(data_base_path)
cursor = connection.cursor()

def main():
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                time_created TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS priority (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                current_priority TEXT
        )    
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                current_status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS main (
                task_id INTEGER PRIMARY KEY,
                priority_id INTEGER NOT NULL,
                status_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,

                FOREIGN KEY (task_id) REFERENCES tasks(id),
                FOREIGN KEY (priority_id) REFERENCES priority(id),
                FOREIGN KEY (status_id) REFERENCES status(id),
                FOREIGN KEY (category_id) REFERENCES category(id)
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

def change_priority_db(task_name, current_priority, new_priority):
    cursor.execute("""
    SELECT main.task_id, task_name
    FROM main
    JOIN tasks ON main.task_id = tasks.id
    JOIN priority ON main.priority_id = priority.id
    WHERE tasks.task_name = ? AND priority.current_priority = ?
    """, (task_name, current_priority))

    result = cursor.fetchone()

    if result:
        task_id, task_name  = result
        cursor.execute("UPDATE priority SET current_priority = ? WHERE current_priority = ?", (new_priority, current_priority))
    
    connection.commit()
    
if __name__ == '__main__':
    main()