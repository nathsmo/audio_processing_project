#importing  libraries
import tkinter as tk
from tkinter import messagebox
#from audio_input import user_input_audio#, audio_note_analysis
#from time import time # time function used to calculate time

# Create a class for the login application
class MainApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Welcome page")
        self.root.geometry("600x440")

        # Call the method to create widgets
        self.create_widgets()

    def create_widgets(self):
        # Create a frame to hold the widgets
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Place the frame in the center of the window

        # Username label and text entry box
        self.label_username = tk.Label(frame, text="Username:")
        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_username = tk.Entry(frame)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        ## ----- Buttons ----- ##
        #Login button
        self.login_btn = tk.Button(frame, text='Login', width=20, command=self.login)#change command to login page
        self.login_btn.grid(row=1, column=1, pady=10)
        # Sign up button
        self.signup_btn = tk.Button(frame, text='Sign up', width=20, command=self.signup)# change command to open signup page
        self.signup_btn.grid(row=2, column=1, pady=10)
        #Close window button
        self.close_btn = tk.Button(frame, text='Close window', width=20, command=root.destroy)
        self.close_btn.grid(row=3, column=1, pady=10)

        photo = tk.PhotoImage(file = "five_seconds.gif")
        # Resize image to fit on button
        photoimage = photo.subsample(1, 2)
        # Position image on button
        self.countdown = tk.Button(frame, image = photoimage).pack(side = BOTTOM, pady = 10)
        self.countdown.grid(row=0, column=1, pady=10)
    
    def five_second_countdown(self):
        # Create a frame to hold the widgets
        frame = tk.Frame(self.signup_frame)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Place the frame in the center of the window

        photo = tk.PhotoImage(file = "five_seconds.gif")
        # Resize image to fit on button
        photoimage = photo.subsample(1, 2)
        # Position image on button
        self.countdown = tk.Button(frame, image = photoimage,)
        self.countdown.grid(row=0, column=1, pady=10)
        self.countdown.after(5000, self.signup_frame.destroy)

    def login(self):
        # Get entered username
        username = self.entry_username.get()
        print('the username is: ', username)
        # Add widgets and functionalities for the dashboard
        messagebox.showinfo(message ="Welcome, {}".format(username))
        # Add verification for login code

    def signup_instructions(self, who):
        # Add widgets and functionalities for the dashboard
        #messagebox.showinfo(message="In order to sign up you will have to\n sign three times the same 4 notes. \nAre you ready?\n Press the button to start!")
        # Destroy the current login window
        #self.signup_w.destroy()
        #print('in here')
        if who ==1:
            print('button 1 clicked')
            self.five_second_countdown()
            self.signup_btn1.destroy()
        elif who ==2:
            print('button 2 clicked')
            self.signup_btn2.destroy()
        elif who ==3:
            print('button 3 clicked')
            self.signup_btn3.destroy()
        else:
            pass

    def signup(self):
        self.signup_w = tk.Tk()
        self.signup_w.title("Sign up page")
        self.signup_w.geometry("600x200")\
        
        frame = tk.Frame(self.signup_w)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Place the frame in the center of the window

        # Username label and text entry box
        self.label_username = tk.Label(frame, text="Chosen username:")
        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_username = tk.Entry(frame)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Username2 label and text entry box
        self.label_username2 = tk.Label(frame, text="Again username:")
        self.label_username2.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_username2 = tk.Entry(frame)
        self.entry_username2.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        #First input button
        self.signup_btn1 = tk.Button(frame, text='Test 1', width=10, command=lambda : self.signup_instructions(who=1))
        self.signup_btn1.grid(row=3, column=0, pady=10)
        #Second input button
        self.signup_btn2 = tk.Button(frame, text='Test 2', width=10, command=lambda : self.signup_instructions(who=2))
        self.signup_btn2.grid(row=3, column=1, pady=10)
        #Third input button
        self.signup_btn3 = tk.Button(frame, text='Test 3', width=10, command=lambda : self.signup_instructions(who=3))
        self.signup_btn3.grid(row=3, column=2, pady=10)

        self.finish_signup = tk.Button(frame, text='Sign up', width=10, command=lambda : self.verify_usernames())
        self.finish_signup.grid(row=4, column=1, pady=10)        


    def verify_usernames(self):
        ####---- code to verify both usernames are the same ----####
        if self.entry_username.get() == self.entry_username2.get():
            print('same username')
        else:
            print('different username')
            messagebox.showinfo(message="The usernames are different, please try again.")

    """
    def close_after_5s(self):
        self.root2.destroy()
        print('destroyed')

    def singup_sing(self):
        print('entering loop')
        self.root2 = tk.Tk()
        prompt = 'Sing 4 tones please, you have 5 seconds.'
        # Add widgets and functionalities for the dashboard
        sing_lbl = tk.Label(self.root2, text=prompt, width=len(prompt))
        sing_lbl.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.root2.after(2000, self.close_after_5s)
        self.root2.mainloop()
        print('out of loop')"""
        


### Code for pop up window
"""
visual=tk.Label(root,text='Waiting...', font=(8))
#visual.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)
visual.place(x=150,y=460)
visual.after(5000, function_to_execute) #root.destroy)# change to have a function just for destroying a window
"""

# Main entry point of the program
if __name__ == "__main__":
    # Create the main Tkinter window and the LoginApp instance
    root = tk.Tk(screenName='Welcome page', className='Welcome page')
    app = MainApp(root)
    
    # Start the main loop for the application
    root.mainloop()
