from GUI import GUI
import json
import requests
from tkinter import END

api_address = "" # standin for now

gui = GUI()

commands = [] # holds user's commands
moveID = 1
turnID = 1

# button functions
def list_all():
    if (len(commands) == 0):
        gui.write_to_terminal("No points")
    for i in range(len(commands)):
        entry = commands[i]
        if entry["cmd"] == "move":
            gui.write_to_terminal_same_line("{ cmd: move ")
            gui.write_to_terminal_same_line(f"d: {entry["d"]} ")
            gui.write_to_terminal_same_line(f"dir: {entry["dir"]} ")
            gui.write_to_terminal_same_line(f"id: {entry["id"]}")
            gui.write_to_terminal(" }")
        else: # cmd is turn
            gui.write_to_terminal_same_line("{ cmd: turn ")
            gui.write_to_terminal_same_line(f"direction: {entry["a"]} ")
            gui.write_to_terminal_same_line(f"id: {entry["id"]}")
            gui.write_to_terminal(" }")

def remove_last():
    if len(commands):
        commands.pop(-1)

def add_command():
    global moveID, turnID, commands
    
    # check which form the user filled in
    distance = gui.dist_entry.get()
    fwdBkwd = gui.direction_selection.get()
    if (distance and fwdBkwd != 0):
        # user filled out move command
        move_command = {
            "cmd" : "move",
            "d" : distance,
            "dir" : fwdBkwd,
            "id" : f"m{moveID}"
        }
        moveID += 1
        commands.append(move_command)
        gui.write_to_terminal(f"Added move command")
        gui.dist_entry.delete(0, END)
        gui.direction_selection.set(0)

    direction = gui.direction_entry.get()
    if direction:
        turn_command = {
            "cmd" : "turn",
            "a" : direction,
            "id" : f"t{turnID}"
        }
        turnID += 1
        commands.append(turn_command)
        gui.write_to_terminal(f"Added turn command")
        gui.direction_entry.delete(0, END)



def send_commands():
    global commands, api_address
    for i in range(len(commands)):
        response = requests.post(api_address, json=commands[i])
        gui.write_to_terminal(f"Sent point {i} and got response {response}")



gui.list_all_button.config(command=list_all)
gui.remove_last_button.config(command=remove_last)
gui.add_point_button.config(command=add_command)
gui.send_button.config(command=send_commands)

gui.root.mainloop()