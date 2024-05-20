import sqlite3
from tkinter import Tk, Label, Entry, Button, messagebox
import os
import logging

logging.basicConfig(level=logging.DEBUG, filename='/Users/hantswilliams/Downloads/app.log')

try:
    # Database connection and table creation
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'tasks.db')
    conn = sqlite3.connect(db_path)
    
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (task text)''')
    conn.commit()

    c.execute('''CREATE TABLE IF NOT EXISTS tasks (task text)''')
    conn.commit()

    def add_task():
        task = entry.get()
        c.execute("INSERT INTO tasks VALUES (?)", (task,))
        conn.commit()
        entry.delete(0, 'end')

    window = Tk()
    window.title("Task Manager")
    label = Label(window, text="Enter Task:")
    label.pack()

    entry = Entry(window)
    entry.pack()

    button = Button(window, text="Add Task", command=add_task)
    button.pack()

    window.mainloop()

    conn.close()

except Exception as e:
    logging.error(f"Error: {e}")
    
    messagebox.showerror("Error", f"An error occurred.\n{e}")
    
    errorMessage = f"Database Error: {e}"
    
    with open('/Users/hantswilliams/Downloads/error.log', 'w') as f:
        f.write(errorMessage)    
        ## display an error message to the user 
        messagebox.showerror("Error", f"Failed to connect to database.\n{e}")
        ## exit the application
    
    exit()



