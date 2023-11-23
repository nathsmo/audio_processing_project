import tkinter as tk
import customtkinter
from gui_audio_input import user_input_audio_signup
from other.note_analysis import audio_note_analysis

# Set appearance mode and default color theme using customtkinter
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

# Create a class for the login application
class SignupApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Sign Up")
        self.root.geometry("600x440")

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

        # self.label_password = tk.Label(frame, text="Password:")
        # self.label_password.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        # self.entry_password = tk.Entry(frame, show="*")  # 'show="*"' hides the password characters
        # self.entry_password.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        # # Create a checkbox to show/hide the password
        # self.show_password_var = tk.IntVar()
        # self.checkbox_show_password = tk.Checkbutton(frame, text="Show Password", variable=self.show_password_var, command=self.toggle_show_password)
        # self.checkbox_show_password.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        # Create a login button with the command to trigger the login process
        self.button_signup = tk.Button(frame, text="Sign up", command=self.signup)
        self.button_signup.grid(row=3, column=1, pady=10)

    def toggle_show_password(self):
        # Toggle the password visibility based on the checkbox state
        if self.show_password_var.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def signup(self):
        # Get entered username and password
        username = self.entry_username.get()

        for i in range(3):
            # Get the password. Sing 3 times.
            tk.messagebox.showinfo("Welcome, {}".format(username), "Pass: '+i'. Please sing four tones for your password. Remember they need to be the same.")
            user_input_audio_signup(str(i), username)
            #audio_note_analysis('./audio_input/password'+str(i)+'_'+username+'.wav')
        
        # Destroy the current login window
        self.root.destroy()

        # Create a new window or change the page to the dashboard
        LoginApp(root)


    def open_dashboard(self):
        # Create a new window for the dashboard
        dashboard_window = tk.Tk()
        dashboard_window.title("Dashboard")
        dashboard_window.geometry("400x200")

        # Add widgets and functionalities for the dashboard
        label_dashboard = tk.Label(dashboard_window, text="Welcome to the Dashboard!")
        label_dashboard.pack(pady=20)

        # Create a button and center it
        # button_in_dashboard = tk.Button(dashboard_window, text="New Button")
        # button_in_dashboard.pack(pady=10)

        # Start the main loop for the dashboard window
        dashboard_window.mainloop()

# Main entry point of the program
if __name__ == "__main__":
    # Create the main Tkinter window and the LoginApp instance
    root = tk.Tk()
    app = LoginApp(root)
    
    # Start the main loop for the application
    root.mainloop()
