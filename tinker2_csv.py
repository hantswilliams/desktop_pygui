import tkinter as tk
from tkinter import filedialog, messagebox, Menu, PhotoImage
import pandas as pd
import sqlite3
import os
import time
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='/Users/hantswilliams/Downloads/app.log')

class CSVAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Analyzer App")
        self.root.geometry("600x400")

        # Initialize menu bar
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add File menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Load CSV", command=self.load_csv)
        file_menu.add_command(label="History", command=self.show_history)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Add Help menu
        help_menu = Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # Initialize main frame and history frame
        self.main_frame = tk.Frame(self.root)
        self.history_frame = tk.Frame(self.root)

        self.setup_main_frame()
        self.setup_history_frame()

        # Start with the main frame
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        # Set up the database file path
        self.app_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(self.app_dir , 'csv_app.db')
        self.setup_history_db()

    def setup_main_frame(self):
        # Frame for buttons
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(anchor='nw', pady=10, padx=10)

        # Button to load CSV
        self.load_button = tk.Button(button_frame, text="Load CSV", command=self.load_csv)
        self.load_button.pack(side=tk.LEFT, padx=(0, 5))

        # Button to show history
        self.history_button = tk.Button(button_frame, text="History", command=self.show_history)
        self.history_button.pack(side=tk.LEFT)

        # Button to save results as text
        self.save_button = tk.Button(button_frame, text="Save Results to Text", command=self.save_results_text)
        self.save_button.pack(side=tk.LEFT, padx=(5, 0))

        # Button to save results as JSON
        self.save_button = tk.Button(button_frame, text="Save Results to JSON", command=self.save_results_json)
        self.save_button.pack(side=tk.LEFT, padx=(5, 0))

        # Text widget to display insights
        self.text = tk.Text(self.main_frame, wrap=tk.WORD)
        self.text.pack(fill=tk.BOTH, expand=1, padx=10, pady=(0, 10))

    def setup_history_frame(self):
        self.history_text = tk.Text(self.history_frame, wrap=tk.WORD)
        self.history_text.pack(fill=tk.BOTH, expand=1, padx=10, pady=(10, 0))

        self.back_button = tk.Button(self.history_frame, text="Back to Main View", command=self.show_main)
        self.back_button.pack(pady=10)

    def setup_history_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS file_history (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              file_path TEXT NOT NULL,
                              access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Error setting up history database: {e}")

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                df = pd.read_csv(file_path)
                self.save_to_sqlite(df, "csv_data.db")
                self.save_to_history(file_path)
                insights = self.generate_insights(df)
                self.display_insights(insights)
                self.current_insights = insights
            except Exception as e:
                logging.error(f"Error loading CSV: {e}")
                messagebox.showerror("Error", f"Failed to load CSV file.\n{e}")

    def generate_insights(self, df):
        try:
            insights = []
            insights.append(f"Number of Rows: {df.shape[0]}")
            insights.append(f"Number of Columns: {df.shape[1]}")
            insights.append(f"Column Names: {', '.join(df.columns)}")
            insights.append("\nColumn Data Types:\n")
            insights.append(df.dtypes.to_string())
            insights.append("\n\nSummary Statistics:\n")
            insights.append(df.describe().to_string())
            return "\n".join(insights)
        except Exception as e:
            logging.error(f"Error generating insights: {e}")
            return "Error generating insights"

    def display_insights(self, insights):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, insights)

    def save_to_sqlite(self, df, db_name):
        try:
            db_path = os.path.join(self.app_dir, db_name)
            conn = sqlite3.connect(db_path)
            df.to_sql('csv_data', conn, if_exists='replace', index=False)
            conn.close()
        except Exception as e:
            logging.error(f"Error saving to SQLite: {e}")

    def save_to_history(self, file_path):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO file_history (file_path) VALUES (?)', (file_path,))
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Error saving to history: {e}")

    def save_results_text(self):
        if hasattr(self, 'current_insights'):
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                try:
                    with open(file_path, 'w') as file:
                        file.write(self.current_insights)
                    messagebox.showinfo("Success", "Results saved successfully.")
                except Exception as e:
                    logging.error(f"Error saving results: {e}")
                    messagebox.showerror("Error", f"Failed to save results.\n{e}")
        else:
            messagebox.showwarning("Warning", "No results to save.")

    def save_results_json(self):
        if hasattr(self, 'current_insights'):
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                try:
                    with open(file_path, 'w') as file:
                        file.write(self.current_insights)
                    messagebox.showinfo("Success", "Results saved successfully.")
                except Exception as e:
                    logging.error(f"Error saving results: {e}")
                    messagebox.showerror("Error", f"Failed to save results.\n{e}")
        else:
            messagebox.showwarning("Warning", "No results to save.")

    def show_about(self):
        messagebox.showinfo("About", "CSV Analyzer App\nVersion 1.0\nDeveloped by Hants Williams, PhD, RN")

    def show_history(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT file_path, access_time FROM file_history ORDER BY access_time DESC')
            records = cursor.fetchall()
            conn.close()

            self.history_text.delete(1.0, tk.END)
            if records:
                history_text = "Recently Accessed Files:\n\n"
                for record in records:
                    history_text += f"{record[1]} - {record[0]}\n"
            else:
                history_text = "No history available."

            self.history_text.insert(tk.END, history_text)

            self.main_frame.pack_forget()
            self.history_frame.pack(fill=tk.BOTH, expand=1)
        except Exception as e:
            logging.error(f"Error showing history: {e}")

    def show_main(self):
        self.history_frame.pack_forget()
        self.main_frame.pack(fill=tk.BOTH, expand=1)

def show_splash_screen(root):
    splash = tk.Toplevel(root)
    splash.title("Loading")
    splash.geometry("300x200")

    # Load and resize the logo image
    logo = PhotoImage(file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'python-icon.png'))
    logo = logo.subsample(logo.width() // 75, logo.height() // 75)  # Resize to fit within 50x50

    # Label to display the logo
    logo_label = tk.Label(splash, image=logo)
    logo_label.image = logo  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=(20, 5))  # Add padding to top (20) and bottom (5)

    label = tk.Label(splash, text="Loading...", font=("Helvetica", 16))
    label.pack(expand=True)
    root.update()
    time.sleep(1)  # Simulate loading time
    splash.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    show_splash_screen(root)  # Show splash screen
    ## sleep for 3 seconds
    time.sleep(1.3)
    app = CSVAnalyzerApp(root)
    root.mainloop()
