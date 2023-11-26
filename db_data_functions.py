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
                last_marked_done TEXT
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
    cursor.execute("INSERT INTO status (current_status, last_marked_done) VALUES (?, ?)", (current_status, None))
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

def change_status_db(prev_status, new_status, task_id, date):
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
    SET current_status = ? , last_marked_done = ?
    WHERE status_id = ? AND current_status = ?
    """, (new_status, date, status_id, prev_status))

    connection.commit()

def delete_task_db(_id):
    cursor.execute("""
    SELECT task_id, priority_id, status_id, category_id
    FROM main
    INNER JOIN tasks USING(task_id)
    INNER JOIN priority USING(priority_id)
    INNER JOIN status USING(status_id)
    INNER JOIN category USING(category_id)
    WHERE task_id = ?
    """, (_id,))
    result = cursor.fetchone()
    task_id, priority_id, status_id, category_id = result

    cursor.execute("DELETE FROM main WHERE task_id = ?", (task_id,))
    cursor.execute("DELETE FROM priority WHERE priority_id = ?", (priority_id,))
    cursor.execute("DELETE FROM status WHERE status_id = ?", (status_id,))
    cursor.execute("DELETE FROM category WHERE category_id = ?", (category_id,))

    connection.commit()

def fetch_data():
    main()
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

def get_task_status_count():

    cursor.execute("SELECT COUNT(*) FROM main WHERE status_id IN (SELECT status_id FROM status WHERE current_status = 'not done')")
    not_done = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM main WHERE status_id IN (SELECT status_id FROM status WHERE current_status = 'done')")
    done = cursor.fetchone()[0]

    return not_done, done

def get_task_data_for_bar_chart(LIMIT=14):
    cursor.execute("""
    SELECT 
        strftime('%Y-%m-%d', time_created) AS time,
        SUM(CASE WHEN current_priority = 'high' AND current_status = 'done' THEN 1 ELSE 0 END),
        SUM(CASE WHEN current_priority = 'mid' AND current_status = 'done' THEN 1 ELSE 0 END),
        SUM(CASE WHEN current_priority = 'low' AND current_status = 'done' THEN 1 ELSE 0 END),
        SUM(CASE WHEN current_priority = 'none' AND current_status = 'done' THEN 1 ELSE 0 END),
        SUM(CASE WHEN current_status = 'done' THEN 1 ELSE 0 END),
        SUM(CASE WHEN current_status = 'not done' THEN 1 ELSE 0 END)
    FROM main
    INNER JOIN tasks USING(task_id)
    INNER JOIN priority USING(priority_id)
    INNER JOIN status USING(status_id)
    WHERE time_created >= strftime('%Y-%m-%d', 'now', ?)
    GROUP BY time
""", (f'-{LIMIT} days',))
    
    priority_lst = []
    status_lst = []
    priority_dict = {}
    status_dict = {}
    date_lst = []
    priority_dict['priority high'] = []
    priority_dict['priority mid'] = []
    priority_dict['priority low'] = []
    priority_dict['priority none'] = []
    status_dict['status done'] = []
    status_dict['status not done'] = []
    for item in cursor.fetchall():
        date_created, high, mid, low, none, done, not_done = item
        priority_dict['priority high'].append(high)
        priority_dict['priority mid'].append(mid)
        priority_dict['priority low'].append(low)
        priority_dict['priority none'].append(none)
        status_dict['status done'].append(done)
        status_dict['status not done'].append(not_done)
        date_lst.append(date_created)
    
    priority_lst.append(priority_dict)
    status_lst.append(status_dict)    
    return priority_lst, status_lst, date_lst


def get_done_with_dates():
    cursor.execute("""
    SELECT 
        last_marked_done, COUNT(*) current_status
    FROM status
    WHERE current_status = 'done'
    GROUP BY strftime('%Y-%m-%d', last_marked_done)
""")

    data_dict = {}
    for item in cursor.fetchall():
        date, value = item
        data_dict[date] = value 
    return data_dict
