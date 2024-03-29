import sqlite3
from settings import *
from datetime import datetime, timedelta

data_base_path = 'data/task_database.db'
connection = sqlite3.connect(data_base_path)
cursor = connection.cursor()
current_version = 102

def setupDatabase():
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
                current_status TEXT,
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
        CREATE TABLE IF NOT EXISTS pomodoro (
                pomodoro_id INTEGER PRIMARY KEY AUTOINCREMENT,
                current_round INTEGER DEFAULT 0,
                total_time INTEGER DEFAULT 0
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS session_data (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pomodoro_id INTEGER,
            session_start_time TEXT,
            session_end_time TEXT,
            session_duration INT DEFAULT 0,
            focus_time INT DEFAULT 0,
            
            FOREIGN KEY (pomodoro_id) REFERENCES pomodoro(pomodoro_id)
        )   
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS main (
                task_id INTEGER PRIMARY KEY,
                priority_id INTEGER NOT NULL,
                status_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                pomodoro_id INTEGER NOT NULL,

                FOREIGN KEY (task_id) REFERENCES tasks(task_id),
                FOREIGN KEY (priority_id) REFERENCES priority(priority_id),
                FOREIGN KEY (status_id) REFERENCES status(status_id),
                FOREIGN KEY (category_id) REFERENCES category(category_id),
                FOREIGN KEY (pomodoro_id) REFERENCES pomodoro(pomodoro_id)
    )   
    """)

    connection.commit()

def commit_new_task_data(task_name, time_created, current_priority='none', current_status='not done', category=None):
    cursor.execute("INSERT INTO tasks (task_name, time_created) VALUES (?, ?)", (task_name, time_created))
    task_id = cursor.lastrowid
    cursor.execute("INSERT INTO priority (current_priority) VALUES (?)", (current_priority,))
    prioirty_id = cursor.lastrowid
    cursor.execute("INSERT INTO status (current_status, last_marked_done) VALUES (?, ?)", (current_status, time_created))
    status_id = cursor.lastrowid
    cursor.execute("INSERT INTO category (category) VALUES (?)", (category,))
    category_id = cursor.lastrowid
    cursor.execute("INSERT INTO pomodoro (current_round, total_time) VALUES (?, ?)", (0, 0))
    pomodoro_id = cursor.lastrowid
    cursor.execute("INSERT INTO main (task_id, priority_id, status_id, category_id, pomodoro_id) VALUES (?,?,?,?,?)", (task_id, prioirty_id, status_id, category_id, pomodoro_id))
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
    SELECT task_id, priority_id, status_id, category_id, pomodoro_id
    FROM main
    INNER JOIN tasks USING(task_id)
    INNER JOIN priority USING(priority_id)
    INNER JOIN status USING(status_id)
    INNER JOIN category USING(category_id)
    INNER JOIN pomodoro USING(pomodoro_id)
    WHERE task_id = ?
    """, (_id,))
    result = cursor.fetchone()
    task_id, priority_id, status_id, category_id, pomdoro_id = result

    cursor.execute("DELETE FROM main WHERE task_id = ?", (task_id,))
    cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
    cursor.execute("DELETE FROM priority WHERE priority_id = ?", (priority_id,))
    cursor.execute("DELETE FROM status WHERE status_id = ?", (status_id,))
    cursor.execute("DELETE FROM category WHERE category_id = ?", (category_id,))
    cursor.execute("DELETE FROM pomodoro WHERE pomodoro_id = ?", (pomdoro_id,))
    cursor.execute("DELETE FROM session_data WHERE pomodoro_id = ?", (pomdoro_id,))
    connection.commit()
    
def update_pomodoro_data(pomodoro_id, current_round, total_time):
    cursor.execute(f"""
        UPDATE pomodoro 
        SET current_round = {current_round},
        total_time = {total_time}
        WHERE pomodoro_id = {pomodoro_id} 
                """)
    connection.commit()
    
def fetchTaskTotalFocusTime(pomodoro_id):
    cursor.execute(f"""
        SELECT total_time 
        FROM pomodoro 
        WHERE pomodoro_id = {pomodoro_id}
                """)
    
    return(cursor.fetchone()[0])

def updateTaskName(task_id, name):
    cursor.execute("""UPDATE tasks
                    set task_name = ? 
                    WHERE task_id = ?
                """, (name, task_id))
    connection.commit()

def getTaskName(taskId):
    cursor.execute("""
                SELECT task_name
                FROM main
                INNER JOIN tasks USING(task_id)
                WHERE task_id = ?
                """, (taskId, ))
    return cursor.fetchone()[0]

def insertNewSessionData(pomodoro_id):
    cursor.execute("""
        INSERT INTO session_data (pomodoro_id, session_start_time) VALUES (?, ?)
                """, (pomodoro_id, datetime.now().strftime('%Y-%m-%d %H:%M')))
    
    connection.commit()
    return cursor.lastrowid


def updateSessionData(session_id, total_duration, focus_time):
    cursor.execute(f"""
        UPDATE session_data
        SET session_duration = ?,
        focus_time = ?,
        session_end_time = ?
        WHERE session_id = ? 
                """, (total_duration, focus_time, datetime.now().strftime('%Y-%m-%d %H:%M'), session_id))
    connection.commit()
    
def fetchPomodoroId(task_id):
    cursor.execute("""
        SELECT pomodoro_id 
        FROM main
        INNER JOIN pomodoro USING(pomodoro_id)
        WHERE task_id = ?
                """, (task_id,))
    
    return(cursor.fetchone()[0])

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

def fetchPiegraphData():
    cursor.execute("SELECT COUNT(*) FROM main WHERE status_id IN (SELECT status_id FROM status WHERE current_status = 'not done')")
    not_done = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM main WHERE status_id IN (SELECT status_id FROM status WHERE current_status = 'done')")
    done = cursor.fetchone()[0]

    undone_task = {'name' : 'Not Completed', 
                'value': not_done, 
                'primary_color': piegraphPrimaryUndoneColor, 
                'secondary_color': piegraphSecondaryUndoneColor}
    
    done_task = {'name' : 'Completed', 
                'value': done, 
                'primary_color': piegraphPrimaryDoneColor, 
                'secondary_color': piegraphSecondaryDoneColor}
    
    return [undone_task, done_task]

def fetchBarGraphPriorityData(LIMIT=20):
    cursor.execute("""
    SELECT 
        strftime('%Y-%m-%d', last_marked_done) AS time,
        SUM(CASE WHEN current_priority = 'high' AND current_status = 'done' THEN 1 ELSE 0 END),
        SUM(CASE WHEN current_priority = 'mid' AND current_status = 'done' THEN 1 ELSE 0 END),
        SUM(CASE WHEN current_priority = 'low' AND current_status = 'done' THEN 1 ELSE 0 END),
        SUM(CASE WHEN current_priority = 'none' AND current_status = 'done' THEN 1 ELSE 0 END)
    FROM main
    INNER JOIN tasks USING(task_id)
    INNER JOIN priority USING(priority_id)
    INNER JOIN status USING(status_id)
    WHERE time >= strftime('%Y-%m-%d', 'now', ?)
    GROUP BY time
""", (f'-{LIMIT} days',))
    
    all_dates = [datetime.now() - timedelta(i) for i in range(LIMIT)]
    all_dates = [date.strftime('%Y-%m-%d') for date in all_dates]
    all_dates.reverse()
    data_lst = []
    dates_done = []
    high = {'label': 'High', 'values': []}
    mid = {'label': 'Mid', 'values': []}
    low = {'label': 'Low', 'values': []}
    none = {'label': 'None', 'values': []}
    
    for item in cursor.fetchall():
        date_done, h, m, l, n = item
        high['values'].append(h)
        mid['values'].append(m)
        low['values'].append(l)
        none['values'].append(n)
        dates_done.append(date_done)

    high['color'] = priorityHighColor
    mid['color'] = priorityMidColor
    low['color'] = priorityLowColor
    none['color'] = priorityNoneColor
        
    data_lst.append(high)
    data_lst.append(mid)
    data_lst.append(low)
    data_lst.append(none)

    return data_lst, dates_done, all_dates, LIMIT

def fetchPomodoroAllSessionDataForSingleTask(taskId):
    pomodoroId = fetchPomodoroId(taskId)
    
    cursor.execute("""
        SELECT session_start_time, session_end_time, focus_time, session_duration
        FROM main
        INNER JOIN session_data USING(pomodoro_id)
        WHERE pomodoro_id = ?
                """, (pomodoroId, ))
    
    return cursor.fetchall()