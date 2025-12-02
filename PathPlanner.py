from GUI import GUI
import json
import requests

api_address = "http://192.168.4.1/api/path" # standin for now
pose_api_address = "http://192.168.4.1/api/pose"  # Will be set based on api_address

gui = GUI()

commands = [] # holds user's commands
moveID = 1
turnID = 1

# button functions
def update_pose():
    """Request current pose from robot and update display"""
    global pose_api_address
    
    # Set pose API address if not set
    if not pose_api_address and api_address:
        # Extract base URL from api_address and add /api/pose
        pose_api_address = api_address.replace('/api/', '/api/pose')
    
    if not pose_api_address:
        gui.show_toast("API address not configured", "error")
        return
    
    try:
        response = requests.get(pose_api_address, timeout=2)
        
        if response.status_code == 200:
            data = response.json()
            
            # Parse response format: {"H":"...", "pose":{"x":..., "y":...}}
            if "pose" in data:
                x = float(data["pose"]["x"])
                y = float(data["pose"]["y"])
                
                # Update the display
                gui.update_pose_display(x, y)
                gui.show_toast(f"Pose updated: ({x:.2f}, {y:.2f})", "success")
            else:
                gui.show_toast("Invalid pose data format", "error")
        else:
            gui.show_toast(f"Failed to get pose: {response.status_code}", "error")
            
    except requests.exceptions.Timeout:
        gui.show_toast("Pose request timed out", "error")
    except requests.exceptions.ConnectionError:
        gui.show_toast("Cannot connect to robot", "error")
    except Exception as e:
        gui.show_toast(f"Error getting pose: {str(e)}", "error")
        print(f"Pose error: {e}")

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

def add_preset_move(distance):
    """Add a movement command with preset distance"""
    global moveID, commands
    
    move_command = {
        "cmd" : "move",
        "d" : distance,
        "dir" : 1,  # Always forward
        "id" : f"m{moveID}"
    }
    moveID += 1
    commands.append(move_command)
    gui.add_command_block(move_command)
    gui.show_toast(f"Move {distance}m added", "success")

def add_preset_turn(angle):
    """Add a turn command with preset angle"""
    global turnID, commands
    
    turn_command = {
        "cmd" : "turn",
        "a" : angle,
        "id" : f"t{turnID}"
    }
    turnID += 1
    commands.append(turn_command)
    gui.add_command_block(turn_command)
    gui.show_toast(f"Turn {angle}° added", "success")

def add_command():
    global moveID, turnID, commands
    
    # Check which tab is currently active
    active_tab = gui.command_tabs.get()
    
    if active_tab == "Movement":
        # Process custom movement command
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
        # Process custom turn command
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
            print(api_address)
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

gui.update_pose_button.configure(command=update_pose)

# Configure preset distance buttons
preset_distances = ["0.1", "0.15", "0.2", "0.25"]
for i, btn in enumerate(gui.preset_dist_buttons):
    btn.configure(command=lambda d=preset_distances[i]: add_preset_move(d))

# Configure preset angle buttons
preset_angles = ["10", "45", "90", "180"]
for i, btn in enumerate(gui.preset_angle_buttons):
    btn.configure(command=lambda a=preset_angles[i]: add_preset_turn(a))

gui.root.mainloop()
