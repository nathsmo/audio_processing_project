import tkinter as tk
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("600x440")

        self.create_widgets()

    def create_widgets(self):
        # Create a frame to hold the widgets
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.label_username = tk.Label(frame, text="Username:")
        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_username = tk.Entry(frame)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        self.label_password = tk.Label(frame, text="Password:")
        self.label_password.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_password = tk.Entry(frame, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        self.show_password_var = tk.IntVar()
        self.checkbox_show_password = tk.Checkbutton(frame, text="Show Password", variable=self.show_password_var, command=self.toggle_show_password)
        self.checkbox_show_password.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        self.button_login = tk.Button(frame, text="Login", command=self.login)
        self.button_login.grid(row=3, column=1, pady=10)

    def toggle_show_password(self):
        if self.show_password_var.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        correct_username = "user"
        correct_password = "password"

        if username == correct_username and password == correct_password:
            tk.messagebox.showinfo("Login Successful", "Welcome, {}".format(username))
            self.root.destroy()
            self.open_dashboard()
        else:
            tk.messagebox.showerror("Login Failed", "Invalid username or password")

    def open_dashboard(self):
        dashboard_window = tk.Tk()
        dashboard_window.title("Dashboard")
        dashboard_window.geometry("400x200")

        label_dashboard = tk.Label(dashboard_window, text="Welcome to the Dashboard!")
        label_dashboard.pack(pady=20)

        # Create a button and center it
        button_in_dashboard = tk.Button(dashboard_window, text="New Button")
        button_in_dashboard.pack(pady=10)

        dashboard_window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
