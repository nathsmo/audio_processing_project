# Importing libraries
import tkinter as tk
from tkinter import messagebox
### Our own libraries
from code_audio import login_attempt, password_creation
from gui_audio_input import user_input_audio, user_input_audio_signup
import pandas as pd
# Create a class for the login application

class MainApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Welcome page")
        self.root.geometry("600x440")
        self.password_df = 'section_outputs.csv'

        # Call the method to create widgets
        self.create_widgets()

    def create_widgets(self):
        # Create a frame to hold the widgets
        self.frame = tk.Frame(self.root)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Place the frame in the center of the window

        # Username label and text entry box
        self.label_username = tk.Label(self.frame, text="Username:")
        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_username = tk.Entry(self.frame)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        ## ----- Buttons ----- ##
        #Login button
        self.login_btn = tk.Button(self.frame, text='Login', width=20, command=self.login)#change command to login page
        self.login_btn.grid(row=1, column=1, pady=10)
        # Sign up button
        self.signup_btn = tk.Button(self.frame, text='Sign up', width=20, command=self.signup)# change command to open signup page
        self.signup_btn.grid(row=2, column=1, pady=10)
        #Close window button
        self.close_btn = tk.Button(self.frame, text='Close window', width=20, command=root.destroy)
        self.close_btn.grid(row=3, column=1, pady=10)

    def init_countdown(self, og_time):
        self.countdown_frame = tk.Tk()
        self.countdown_frame.title("5-Second Counter")

        self.counter_label = tk.Label(self.countdown_frame, text="", font=("Helvetica", 24))
        self.counter_label.pack(pady=20)

        self.countdown(og_time)

    def countdown(self, remaining):
        if remaining <= 0:
            self.counter_label.configure(text="Time's up!")
            # Add any actions you want to perform after the countdown ends
        else:
            self.counter_label.configure(text=f"Time remaining: {remaining}")
            self.countdown_frame.after(1000, lambda: self.countdown(remaining - 1))

    def login(self):
        # Get entered username
        username = self.entry_username.get()
        print('The username is: ', username)
        # Add widgets and functionalities for the dashboard
        if self.verify_usernames(login=True):
            entry_path, entry = user_input_audio(username)
            if login_attempt(entry_path, entry, self.password_df, username):
                tk.showinfo(message ="Welcome, {}".format(username))
                #Add code to send user to the dashboard
            else:
                tk.showinfo(message ="Wrong password, please try again")
            return
        else:
            return 
        
    def signup_instructions(self, who):
        if self.verify_usernames(): 
            if who ==1:
                print('button 1 clicked')
                #self.signup_btn1.configure(bg="green", text='Recording...')
                if user_input_audio_signup(self.entry_username1, who):
                    self.signup_btn1.destroy()
                    self.signup_btn1 = tk.Label(self.framesu, text='Finished', width=10)
                    self.signup_btn1.grid(row=3, column=0, pady=10)
            elif who ==2:
                print('button 2 clicked')
                #self.signup_btn2.configure(bg="green", text='Recording...')
                if user_input_audio_signup(self.entry_username1, who):
                    self.signup_btn2.destroy()
                    self.signup_btn2 = tk.Label(self.framesu, text='Finished', width=10)
                    self.signup_btn2.grid(row=3, column=1, pady=10)
            elif who ==3:
                print('button 3 clicked')
                if user_input_audio_signup(self.entry_username1, who):
                    self.signup_btn3.destroy()
                    self.signup_btn3 = tk.Label(self.framesu, text='Finished', width=10)
                    self.signup_btn3.grid(row=3, column=2, pady=10)            
            #self.init_countdown(5)
             
        else:
            pass

    def signup(self):
        self.signup_w = tk.Tk()
        self.signup_w.title("Sign up page")
        self.signup_w.geometry("600x200")
        
        self.framesu = tk.Frame(self.signup_w)
        self.framesu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Place the frame in the center of the window

        # Username label and text entry box
        self.label_username = tk.Label(self.framesu, text="Chosen username:")
        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_username1 = tk.Entry(self.framesu)
        self.entry_username1.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Username2 label and text entry box
        self.label_username2 = tk.Label(self.framesu, text="Again username:")
        self.label_username2.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_username2 = tk.Entry(self.framesu)
        self.entry_username2.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        #First input button
        self.signup_btn1 = tk.Button(self.framesu, text='Record', width=10, command=lambda : self.signup_instructions(who=1))
        self.signup_btn1.grid(row=3, column=0, pady=10)

        #Second input button
        self.signup_btn2 = tk.Button(self.framesu, text='Record', width=10, command=lambda : self.signup_instructions(who=2))
        self.signup_btn2.grid(row=3, column=1, pady=10)

        #Third input button
        self.signup_btn3 = tk.Button(self.framesu, text='Record', width=10, command=lambda : self.signup_instructions(who=3))
        self.signup_btn3.grid(row=3, column=2, pady=10)

        # Final verification for sign-up - button
        # Add verification code for the sign-up
        self.finish_signup = tk.Button(self.framesu, text='Sign up', width=10, command=lambda : self.verify_usernames())
        self.finish_signup.grid(row=4, column=1, pady=10)

    def verify_usernames(self, login=False):
        ####---- code to verify both usernames are the same ----####
        database = pd.read_csv(self.password_df)

        if login:
            #verify user exists in database
            if self.entry_username.get() not in database.user.values:
                messagebox.showinfo(message="The username doesn't exist, please try again.")
                return False
            else:
                return True
        else:
            #verify user doesn't exist in database
            if (len(self.entry_username1.get()) > 0) and (self.entry_username1.get() == self.entry_username2.get()):
                print('same username')
                return True
            else:
                print('Different username, or no username entered')
                messagebox.showinfo(message="The usernames are different or you haven't entered a username, please try again.")
                return False


# Main entry point of the program
if __name__ == "__main__":
    # Create the main Tkinter window and the LoginApp instance
    root = tk.Tk(screenName='Welcome page', className='Welcome page')
    app = MainApp(root)
    
    # Start the main loop for the application
    root.mainloop()
