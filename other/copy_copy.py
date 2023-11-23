import tkinter as tk
import customtkinter
from gui_audio_input import user_input_audio
from other.note_analysis import audio_note_analysis

# Set appearance mode and default color theme using customtkinter
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

# Create a class for the login application
class LoginApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Login")
        self.root.geometry("600x440")

        # Track the number of signups
        self.signup_count = 0

        # Call the method to create widgets
        self.create_widgets()

    def create_widgets(self):
        # Create a frame to hold the widgets
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Place the frame in the center of the window

        # Create labels and entry widgets for username and password
        self.label_username = tk.Label(frame, text="Username:")
        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_username = tk.Entry(frame)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Create a signup button with the command to trigger the signup process
        self.button_signup = tk.Button(frame, text="Sign Up", command=self.signup)
        self.button_signup.grid(row=1, column=0, pady=10)

        # Create a login button with the command to trigger the login process
        self.button_login = tk.Button(frame, text="Login", command=self.login)
        self.button_login.grid(row=1, column=1, pady=10)

    def signup(self):
        # Create a new window for the dashboard
        dashboard_window = tk.Tk()
        dashboard_window.title("Sign up page")
        dashboard_window.geometry("400x200")

        # Add widgets and functionalities for the dashboard
        label_dashboard = tk.Label(dashboard_window, 
                                   text="In order to sign up you will have to\n sign three times the same 4 notes. \nAre you ready?\n Press the button to start!")
        label_dashboard.pack(pady=20)

        # Create labels and entry widgets for username and password
        self.label_username = tk.Label(frame, text="Username:")
        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_username = tk.Entry(frame)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        username = self.entry_username.get()

        for i in range(3):
            # Get the password. Sing 3 times.
            self.button_sing = tk.Button(label_dashboard, text="Ready", command=user_input_audio())
            self.button_sing.grid(row=1, column=1, pady=10)

                    # Save the username to a file
            filename = f"signup_{self.signup_count + 1}.txt"
            with open(filename, "w") as file:
                file.write(username)

            # Increment the signup count
            self.signup_count += 1

        # Provide feedback to the user
        #tk.messagebox.showinfo("Signup Successful", "Signup successful! You can now login.")

    def login(self):
        # Get entered username
        username = self.entry_username.get()

        # Check if the username exists in any of the signup files
        for i in range(1, self.signup_count + 1):
            filename = f"signup_{i}.txt"
            with open(filename, "r") as file:
                saved_username = file.read().strip()
                if username == saved_username:
                    tk.messagebox.showinfo("Welcome, {}".format(username), "Correct username, now... SING to me Paolo!")
                    user_input_audio()
                    audio_note_analysis('./audio_input/output.wav')

                    # Destroy the current login window
                    self.root.destroy()

                    # Create a new window or change the page to the dashboard
                    self.open_dashboard()
                    return

        # If the loop completes, the username was not found in any signup files
        tk.messagebox.showerror("Login Failed", "Invalid username")

    def open_dashboard(self):
        # Create a new window for the dashboard
        dashboard_window = tk.Tk()
        dashboard_window.title("Dashboard")
        dashboard_window.geometry("400x200")

        # Add widgets and functionalities for the dashboard
        label_dashboard = tk.Label(dashboard_window, text="Welcome to the Dashboard!")
        label_dashboard.pack(pady=20)

        # Start the main loop for the dashboard window
        dashboard_window.mainloop()

# Main entry point of the program
if __name__ == "__main__":
    # Create the main Tkinter window and the LoginApp instance
    root = tk.Tk()
    app = LoginApp(root)
    
    # Start the main loop for the application
    root.mainloop()
