import tkinter as tk
from tkinter import messagebox
from professor_panel import ProfessorGUI
from students_panel import StudentGUI
from lms.lms import LMS
from lms.professors import Professor

# Load LMS Data
lms = LMS()
professor = Professor.load_data(lms)
student = None  # Student login will be manual

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LMS Login")
        self.root.geometry("400x300")

        tk.Label(root, text="User ID:").pack(pady=5)
        self.user_id_entry = tk.Entry(root)
        self.user_id_entry.pack(pady=5)

        tk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()

        # Check for professor login
        if int(user_id) in lms.professors and lms.professors[int(user_id)].password == password:
            self.root.destroy()  # Close login window
            ProfessorGUI(lms.professors[int(user_id)], lms)  # Open professor dashboard
            return

        # Check for student login
        if int(user_id) in lms.students and lms.students[int(user_id)].password == password:
            self.root.destroy()
            StudentGUI(lms.students[int(user_id)], lms)  # Open student dashboard
            return

        messagebox.showerror("Login Failed", "Invalid ID or Password")

# Run GUI
root = tk.Tk()
app = LoginApp(root)
root.mainloop()
