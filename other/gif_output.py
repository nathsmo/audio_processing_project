import tkinter as tk

class CounterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("5-Second Counter")

        self.counter_label = tk.Label(self.root, text="", font=("Helvetica", 24))
        self.counter_label.pack(pady=20)

        self.countdown(5)

    def countdown(self, remaining):
        if remaining <= 0:
            self.counter_label.configure(text="Time's up!")
            # Add any actions you want to perform after the countdown ends
        else:
            self.counter_label.configure(text=f"Time remaining: {remaining}")
            self.root.after(1000, lambda: self.countdown(remaining - 1))

    def run(self):
        self.root.mainloop()

# Example usage
if __name__ == "__main__":
    counter_app = CounterApp()
    counter_app.run()
