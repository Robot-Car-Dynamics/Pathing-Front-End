import tkinter as tk

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Robot Car Pathing")
        self.root.geometry("680x540")

        # NOTE: making everything self.var allows access from outside
        # This amount of access is almost certainly overkill though

        # define forms frame
        self.forms_frame = tk.Frame(self.root)
        self.forms_frame.pack(side="top", fill="y", pady=10, padx=10)

        # define move form
        self.move_form = tk.Frame(self.forms_frame)
        self.move_form.pack(side="top", fill='y', pady=10, padx=10)

        self.dist_label = tk.Label(self.move_form, text="Distance:")
        self.dist_label.grid(column=0, row=0, padx=10, pady=10)
        self.dist_entry = tk.Entry(self.move_form)
        self.dist_entry.grid(column=1, row=0)
        self.dist_units_label = tk.Label(self.move_form, text="meters")
        self.dist_units_label.grid(column=2, row=0)
        self.direction_frame = tk.Frame(self.move_form)
        self.direction_frame.grid(column=1, row=1)
        self.direction_selection = tk.IntVar(self.root)
        self.forward_radio = tk.Radiobutton(self.direction_frame, value=1, variable=self.direction_selection, text="Forward")
        self.forward_radio.pack(side="left", fill='y', padx=10)
        self.backward_radio = tk.Radiobutton(self.direction_frame, value=-1, variable=self.direction_selection, text="Backward")
        self.backward_radio.pack(side="right", fill='y', padx=10)


        # define turn form
        self.turn_form = tk.Frame(self.forms_frame)
        self.turn_form.pack(side="bottom", fill='y', pady=10, padx=20)
        self.direction_label = tk.Label(self.turn_form, text="Direction")
        self.direction_label.grid(row=0, column=0, padx=10, pady=10)
        self.direction_entry = tk.Entry(self.turn_form)
        self.direction_entry.grid(column=1, row=0, padx=10, pady=10)
        self.direction_units_label = tk.Label(self.turn_form, text="degrees")
        self.direction_units_label.grid(column=2, row=0)

        self.explain_label = tk.Label(self.turn_form, text="Note that 90 degrees is straight ahead")
        self.explain_label.grid(column=1, row=1)

        # define display and buttons
        self.bottom_part = tk.Frame(self.root) # not a great name
        self.bottom_part.pack(side="bottom", fill="y", pady=10, padx=10)

        # button panel
        self.button_panel = tk.Frame(self.bottom_part)
        self.button_panel.pack(side="top", fill='y')
        self.list_all_button = tk.Button(self.button_panel, text="List Current Points")
        self.list_all_button.grid(column=0, row=0)
        self.remove_last_button = tk.Button(self.button_panel, text="Remove Last Point")
        self.remove_last_button.grid(column=1, row=0)
        self.add_point_button = tk.Button(self.button_panel, text="Add Current Point")
        self.add_point_button.grid(column=2, row=0)
        self.send_button = tk.Button(self.button_panel, text="Send Points")
        self.send_button.grid(column=3, row=0)

        # "terminal" to show messages to user
        self.terminal = tk.Text(master=self.bottom_part, bg="black", fg="lime", insertbackground="white", height=540, width=80)
        self.terminal.pack(fill="y", side="bottom")
        self.terminal.insert("end", "Path Planner Interface.\nPlease choose an option to begin\n")
        self.terminal.config(state="disabled") # to prevent the user from writing

    def write_to_terminal(self, text):
        self.terminal.config(state="normal")
        self.terminal.insert("end", text + '\n')
        self.terminal.see("end")
        self.terminal.config(state="disabled")

    def write_to_terminal_same_line(self, text):
        self.terminal.config(state="normal")
        self.terminal.insert("end", text)
        self.terminal.see("end")
        self.terminal.config(state="disabled")

if __name__ == "__main__":
    gui = GUI()
    gui.root.mainloop()
