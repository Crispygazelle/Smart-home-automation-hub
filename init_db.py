import sqlite3

def init_db():
    # This will create a file named 'smarthome.db' in your current directory
    conn = sqlite3.connect('smarthome.db')
    cursor = conn.cursor()

    # Create devices table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS devices (
        device_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        mqtt_topic TEXT NOT NULL,
        current_state TEXT NOT NULL
    )
    ''')

    # Create schedules table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedules (
        schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER,
        action_time TEXT NOT NULL,
        target_state TEXT NOT NULL,
        FOREIGN KEY(device_id) REFERENCES devices(device_id)
    )
    ''')

    # Inject a test device to save time later
    cursor.execute('''
    INSERT INTO devices (name, mqtt_topic, current_state) 
    SELECT 'Living Room Light', 'home/living_room/light', 'OFF'
    WHERE NOT EXISTS (SELECT 1 FROM devices WHERE mqtt_topic = 'home/living_room/light')
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully with test device.")

if __name__ == '__main__':
    init_db()
