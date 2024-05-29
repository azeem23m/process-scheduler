import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk


def formate(ar):
    Formatted = [[], []]
    for i in range(1, len(ar)):
        Formatted[0].append('Process ' + str(ar[i][0]))
        Formatted[1].append(ar[i][7])
    return Formatted


def ganttChart(ar):
    fig, ax = plt.subplots()
    ax.set_yticks(np.arange(len(ar[0])))
    ax.set_yticklabels(ar[0])
    cur = 0
    for i in range(len(ar[0])):
        start_value = cur
        end_value = ar[1][i]
        ax.barh(i, end_value - start_value, left=start_value, height=0.5, align='center')
        cur = end_value
    max_value = max(max(ar[1]), max(ar[1]) + max(ar[1]))
    ax.set_xlim(0, max_value)
    ax.set_xlabel('Value')
    plt.show()


class gui():
    def __init__(self, root):
        self.root = root
        self.root.title("Non preemptive priority")
        self.root.geometry("700x600")

       

        self.processes = []  # [for checking the values of the time]
        self.vaildProcesses = []

        self.label_processes = tk.Label(root, text="Number of processes:", bg="#818181", fg="black", font=("Arial", 20))
        self.label_processes.pack(pady=10)
        self.entry_processes = tk.Entry(root, bd=0)
        self.entry_processes.pack(pady=5)

        self.btn_submit_processes = tk.Button(root, text="Submit", command=self.create_process_form, bg="#424242", fg="white", font=("Arial", 12))
        self.btn_submit_processes.pack(padx=10)

        self.init_buttons()  # Initialize buttons

    def init_buttons(self):
        # Create a frame to contain the buttons
        button_frame = tk.Frame(self.root, bg="#818181", bd=0)
        button_frame.pack(side=tk.BOTTOM)

        # Adding restart and close buttons
        restart_button = tk.Button(button_frame, text="Restart", command=self.restart_program, bg="#333333",
                                   fg="white", font=("Arial", 12))
        restart_button.pack(side=tk.LEFT, padx=10, pady=10)

        close_button = tk.Button(button_frame, text="Close", command=self.close_program, bg="#333333", fg="white",
                                 font=("Arial", 12))
        close_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Change close button color to red when hovered over
        close_button.bind("<Enter>", lambda event: close_button.config(bg="#f44336", activebackground="#f44336"))
        close_button.bind("<Leave>", lambda event: close_button.config(bg="#333333", activebackground="#333333"))

    def restart_program(self):
        self.root.destroy()  # Close the result window
        plt.close('all')  # Close all figure windows
        self.root.quit()
        self.root = tk.Tk()
        ob = gui(self.root)
        self.root.mainloop()

    def close_program(self):
        self.root.destroy()  # Close the result window
        plt.close('all')  # Close all figure windows

    # $
    def create_process_form(self):
        try:
            num_processes = int(self.entry_processes.get())
            if num_processes <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number !!!!")
            return

        # Create a frame for the input fields
        input_frame = tk.Frame(self.root, bg="#818181", bd=0)
        input_frame.pack(pady=20)

        # Labels
        tk.Label(input_frame, text="Arrival Time", bg="#818181", fg="black", font=("Arial", 12)).grid(row=1, column=1, padx=5, pady=5)
        tk.Label(input_frame, text="Burst Time", bg="#818181", fg="black", font=("Arial", 12)).grid(row=1, column=2, padx=5, pady=5)
        tk.Label(input_frame, text="Priority", bg="#818181", fg="black", font=("Arial", 12)).grid(row=1, column=3, padx=5, pady=5)

        # Input fields
        for i in range(num_processes):
            tk.Label(input_frame, text=f"Process {i + 1}").grid(row=i + 2, column=0, padx=5, pady=5)
            entry_arrival = tk.Entry(input_frame)
            entry_arrival.grid(row=i + 2, column=1, padx=5, pady=5)
            entry_burst = tk.Entry(input_frame)
            entry_burst.grid(row=i + 2, column=2, padx=5, pady=5)
            entry_priority = tk.Entry(input_frame)
            entry_priority.grid(row=i + 2, column=3, padx=5, pady=5)
            self.processes.append([entry_arrival, entry_burst, entry_priority])

        # Place the 'Run' button below the input fields
        tk.Button(self.root, text="Run", command=self.simulate_fcfs).pack(pady=10)
        self.btn_submit_processes.config(state="disabled")

    def simulate_fcfs(self):
        counter = 1
        self.vaildProcesses.append([0, 0, 0, 0, 0, 0, 0, 0])
        for entry_arrival, entry_burst, entry_prioriy in self.processes:
            try:
                arrival_time = int(entry_arrival.get())
                burst_time = int(entry_burst.get())
                priority = int(entry_prioriy.get())
                if arrival_time < 0 or burst_time <= 0 or priority <= 0:
                    raise ValueError
                self.vaildProcesses.append([counter, arrival_time, burst_time, priority, 0, 0, 0, 0])
                counter += 1
            except ValueError:
                messagebox.showerror("Error", "Unvaild value for arrival or burst time!!! ")
                return
        self.SortData()

    def SortData(self):
        zero_record = self.vaildProcesses[0]
        first_record = self.vaildProcesses[1]
        self.sorted_data = [zero_record] + [first_record] + sorted(self.vaildProcesses[2:], key=lambda x: x[3])
        self.Calc_all_operation()

    def Calc_all_operation(self):
        previousIndex = 0
        for record in self.sorted_data[1:]:
            record[7] = self.sorted_data[previousIndex][7] + record[2]
            record[4] = (record[7] - record[1])
            record[5] = record[4] - record[2]
            record[6] = self.sorted_data[previousIndex][7] - record[1]
            previousIndex += 1;
        self.clear_frame()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.DisplayData()

    def DisplayData(self):
        self.root.geometry("900x600")
        self.My_tree = ttk.Treeview(self.root)
        self.My_tree['columns'] = (
            "arrival_time", "turnaround", "burst_time", "waiting_time", "respond_time", "terminate")

        self.My_tree.column("#0", width=150, stretch=tk.NO)
        self.My_tree.column("arrival_time", anchor=tk.CENTER, width=150)
        self.My_tree.column("turnaround", anchor=tk.CENTER, width=150)
        self.My_tree.column("burst_time", anchor=tk.CENTER, width=150)
        self.My_tree.column("waiting_time", anchor=tk.CENTER, width=150)
        self.My_tree.column("respond_time", anchor=tk.CENTER, width=150)
        self.My_tree.column("terminate", anchor=tk.CENTER, width=150)

        self.My_tree.heading("#0", text="Process Name", anchor=tk.CENTER)
        self.My_tree.heading("arrival_time", text="Arrival time", anchor=tk.CENTER)
        self.My_tree.heading("burst_time", text="Busrt time", anchor=tk.CENTER)
        self.My_tree.heading("turnaround", text="Turnaround", anchor=tk.CENTER)
        self.My_tree.heading("waiting_time", text="Waiting time", anchor=tk.CENTER)
        self.My_tree.heading("respond_time", text="Respond time", anchor=tk.CENTER)
        self.My_tree.heading("terminate", text="Terminate", anchor=tk.CENTER)

        self.root.style = ttk.Style()
        self.root.style.configure("Custom.Treeview.Separator", background="light gray")

        count = 0
        for record in self.sorted_data:
            if count != 0:
                self.My_tree.insert(parent='', index='end', iid=count, text="Process" + str(record[0]),
                                    values=(record[1], record[4], record[2], record[5], record[6], record[7]))
            count += 1

        self.My_tree.pack(pady=20)

        # Adding restart and close buttons
        restart_button = tk.Button(self.root, text="Restart", command=self.restart_program, bg="#333333",
                                   fg="white", font=("Arial", 12))
        restart_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        close_button = tk.Button(self.root, text="Close", command=self.close_program, bg="#333333", fg="white",
                                 font=("Arial", 12))
        close_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        close_button.bind("<Enter>", lambda event: close_button.config(bg="#f44336", activebackground="#f44336"))
        close_button.bind("<Leave>", lambda event: close_button.config(bg="#333333", activebackground="#333333"))

        ganttChart(formate(self.sorted_data))


root = tk.Tk()
ob = gui(root)
root.mainloop()
