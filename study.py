import tkinter as tk
from tkinter import messagebox
import time
from win10toast import ToastNotifier



class WorkoutTimer:
    def __init__(self, root):
        self.timer_mode="workout"
        self.root = root
        self.root.title("Workout Timer")

        self.workout_time = tk.StringVar()
        self.rest_time = tk.StringVar()
        self.num_intervals = tk.StringVar()

        self.workout_label = None
        self.rest_label = None

        self.toaster = ToastNotifier()

        self.create_widgets()

    def create_widgets(self):
        # Label and Entry for Workout Time
        tk.Label(self.root, text="Workout Time (in seconds):").grid(row=0, column=0, padx=10, pady=5)
        self.workout_entry = tk.Entry(self.root, textvariable=self.workout_time)
        self.workout_entry.grid(row=0, column=1, padx=10, pady=5)

        # Label and Entry for Rest Time
        tk.Label(self.root, text="Rest Time (in seconds):").grid(row=1, column=0, padx=10, pady=5)
        self.rest_entry = tk.Entry(self.root, textvariable=self.rest_time)
        self.rest_entry.grid(row=1, column=1, padx=10, pady=5)

        # Label and Entry for Number of Intervals
        tk.Label(self.root, text="Number of Intervals:").grid(row=2, column=0, padx=10, pady=5)
        self.interval_entry = tk.Entry(self.root, textvariable=self.num_intervals)
        self.interval_entry.grid(row=2, column=1, padx=10, pady=5)

        # Start Button
        self.start_button = tk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Stop Button
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # Labels for displaying countdown timers
        self.workout_label = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.workout_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.rest_label = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.rest_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    def start_timer(self):
        try:
            workout_time = int(self.workout_time.get())
            rest_time = int(self.rest_time.get())
            num_intervals = int(self.num_intervals.get())

            if workout_time <= 0 or rest_time <= 0 or num_intervals <= 0:
                messagebox.showwarning("Warning", "Please enter valid values (greater than 0).")
                return

            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

            for _ in range(num_intervals):
                self.update_timer_label(self.workout_label, f"Workout: {workout_time}")
                self.update_timer_label(self.rest_label, f"Rest: {rest_time}")

                # Workout time
                print("Workout Timer is running...")
                self.timer_mode="workout"
                self.countdown(workout_time)
                self.update_timer_label(self.workout_label, "Workout: Done!")

                # Show rest time notification
                self.show_notification("Rest Time", f"Rest for {rest_time} seconds starts now!")
                # Rest time
                print("Rest Timer is running...")
                self.timer_mode="rest"
                self.countdown(rest_time)
                self.update_timer_label(self.rest_label, "Rest: Done!")
                # Show workout time notification
                self.show_notification("Workout Time", f"Workout for {workout_time} seconds starts now!")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer values.")

    def stop_timer(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def countdown(self, seconds):
        for sec in range(seconds, -1, -1):
            self.root.update()
            time.sleep(1)
            if sec != 0:
                
                self.update_timer_label(self.workout_label if "Workout" in self.workout_label.cget("text") else self.rest_label, f"{sec} seconds left")
            else:
                break

    def update_timer_label(self, label, text):
        label.config(text=self.timer_mode + ": " +text)
        self.root.update()

    def show_notification(self, title, message):
        self.toaster.show_toast(title, message, duration=5, threaded=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = WorkoutTimer(root)
    root.mainloop()