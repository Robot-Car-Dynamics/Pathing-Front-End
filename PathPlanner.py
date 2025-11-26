from GUI import GUI
import json
import requests

api_address = "" # standin for now

gui = GUI()

commands = [] # holds user's commands
moveID = 1
turnID = 1

# button functions
def clear_all():
    global commands
    commands.clear()
    gui.clear_all_command_blocks()

def list_all():
    """Debug function - prints to console"""
    if (len(commands) == 0):
        print("No commands")
    for i in range(len(commands)):
        entry = commands[i]
        if entry["cmd"] == "move":
            print(f"{{ cmd: move d: {entry['d']} dir: {entry['dir']} id: {entry['id']} }}")
        else:
            print(f"{{ cmd: turn direction: {entry['a']} id: {entry['id']} }}")

def remove_last():
    if len(commands):
        commands.pop(-1)
        gui.remove_last_command_block()

def add_command():
    global moveID, turnID, commands
    
    # Check which tab is currently active
    active_tab = gui.command_tabs.get()
    
    if active_tab == "Movement":
        # Process movement command (always forward)
        distance = gui.dist_entry.get()
        
        if not distance:
            gui.show_toast("Please enter a distance", "error")
            return
            
        move_command = {
            "cmd" : "move",
            "d" : distance,
            "dir" : 1,  # Always forward
            "id" : f"m{moveID}"
        }
        moveID += 1
        commands.append(move_command)
        gui.add_command_block(move_command)
        gui.dist_entry.delete(0, "end")
        gui.show_toast("Movement command added", "success")
        
    elif active_tab == "Turn":
        # Process turn command
        direction = gui.direction_entry.get()
        
        if not direction:
            gui.show_toast("Please enter an angle", "error")
            return
            
        turn_command = {
            "cmd" : "turn",
            "a" : direction,
            "id" : f"t{turnID}"
        }
        turnID += 1
        commands.append(turn_command)
        gui.add_command_block(turn_command)
        gui.direction_entry.delete(0, "end")
        gui.show_toast("Turn command added", "success")



def send_commands():
    global commands, api_address
    
    # Get the current sequence order from GUI
    commands = gui.get_command_sequence()
    
    if len(commands) == 0:
        gui.show_toast("No commands to send", "warning")
        return
    
    print("Final command sequence to send:")
    list_all()
    print(f"Sending {len(commands)} commands...")
    
    gui.show_toast(f"Sending {len(commands)} commands...", "info")
    
    for i in range(len(commands)):
        try:
            response = requests.post(api_address, json=commands[i])
            print(f"Sent command {i+1}/{len(commands)} - Status: {response.status_code}")
        except Exception as e:
            print(f"Error sending command {i+1}: {e}")
            gui.show_toast(f"Error sending command {i+1}", "error")
            return
    
    gui.show_toast("All commands sent successfully!", "success")



gui.clear_all_button.configure(command=clear_all)
gui.remove_last_button.configure(command=remove_last)
gui.add_point_button.configure(command=add_command)
gui.send_button.configure(command=send_commands)

gui.root.mainloop()