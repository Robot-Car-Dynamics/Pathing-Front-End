import customtkinter

class GUI:
    def __init__(self):
        # Set appearance mode and default color theme
        customtkinter.set_appearance_mode("dark")  # Modes: "dark", "light", "system"
        customtkinter.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"
        
        self.root = customtkinter.CTk()
        self.root.title("Robot Car Pathing")
        self.root.geometry("680x540")

        # NOTE: making everything self.var allows access from outside
        # This amount of access is almost certainly overkill though

        # define forms frame with tabbed interface
        self.forms_frame = customtkinter.CTkFrame(self.root, fg_color="transparent")
        self.forms_frame.pack(side="top", fill="y", pady=10, padx=10)
        
        # Create tabbed interface for command types
        self.command_tabs = customtkinter.CTkTabview(
            self.forms_frame,
            width=600,
            height=200,
            fg_color=("#E8F4F8", "#1a1a2e"),
            border_width=2,
            border_color=("#3b8ed0", "#1f6aa5")
        )
        self.command_tabs.pack(padx=10, pady=10)
        
        # Add tabs
        self.command_tabs.add("Movement")
        self.command_tabs.add("Turn")
        self.command_tabs.set("Movement")  # Set default tab

        # ===== MOVEMENT TAB =====
        move_tab = self.command_tabs.tab("Movement")

        self.dist_label = customtkinter.CTkLabel(move_tab, text="Distance:", font=("Arial", 12))
        self.dist_label.grid(column=0, row=0, padx=10, pady=20)
        self.dist_entry = customtkinter.CTkEntry(move_tab, placeholder_text="Enter distance...", width=200)
        self.dist_entry.grid(column=1, row=0, padx=5, pady=20)
        self.dist_units_label = customtkinter.CTkLabel(move_tab, text="meters", font=("Arial", 11))
        self.dist_units_label.grid(column=2, row=0, padx=10, pady=20)
        
        # Always move forward - set direction to 1 and hide the selection
        self.direction_selection = customtkinter.IntVar(self.root, value=1)  # Always forward

        # ===== TURN TAB =====
        turn_tab = self.command_tabs.tab("Turn")
        
        self.direction_label = customtkinter.CTkLabel(turn_tab, text="Direction:", font=("Arial", 12))
        self.direction_label.grid(row=0, column=0, padx=10, pady=20)
        self.direction_entry = customtkinter.CTkEntry(turn_tab, placeholder_text="Enter angle...", width=200)
        self.direction_entry.grid(column=1, row=0, padx=5, pady=20)
        self.direction_units_label = customtkinter.CTkLabel(turn_tab, text="degrees", font=("Arial", 11))
        self.direction_units_label.grid(column=2, row=0, padx=10, pady=20)

        self.explain_label = customtkinter.CTkLabel(turn_tab, text="Note: 90° is straight ahead", font=("Arial", 10, "italic"), text_color=("#555555", "#aaaaaa"))
        self.explain_label.grid(column=1, row=1, pady=(0, 20))

        # define display and buttons
        self.bottom_part = customtkinter.CTkFrame(self.root, fg_color="transparent")
        self.bottom_part.pack(side="bottom", fill="y", pady=10, padx=10)

        # button panel with colored buttons
        self.button_panel = customtkinter.CTkFrame(self.bottom_part, fg_color="transparent")
        self.button_panel.pack(side="top", fill='y', pady=(0, 10))
        
        # Clear button - info style
        self.clear_all_button = customtkinter.CTkButton(
            self.button_panel, 
            text="Clear All",
            fg_color="transparent",
            border_width=2,
            border_color=("#3b8ed0", "#1f6aa5"),
            hover_color=("#d0e8f5", "#2a4a6e"),
            font=("Arial", 12)
        )
        self.clear_all_button.grid(column=0, row=0, padx=5, pady=5)
        
        # Remove button - warning orange/red
        self.remove_last_button = customtkinter.CTkButton(
            self.button_panel, 
            text="Remove Last",
            fg_color=("#ff6b6b", "#c92a2a"),
            hover_color=("#ff5252", "#a61e1e"),
            font=("Arial", 12)
        )
        self.remove_last_button.grid(column=1, row=0, padx=5, pady=5)
        
        # Add button - success green
        self.add_point_button = customtkinter.CTkButton(
            self.button_panel, 
            text="Add Command",
            fg_color=("#51cf66", "#2f9e44"),
            hover_color=("#40c057", "#26803b"),
            font=("Arial", 12)
        )
        self.add_point_button.grid(column=2, row=0, padx=5, pady=5)
        
        # Send button - accent purple (most important action)
        self.send_button = customtkinter.CTkButton(
            self.button_panel, 
            text="Send Commands",
            fg_color=("#845ef7", "#6741d9"),
            hover_color=("#7048e8", "#5a34c1"),
            font=("Arial", 12, "bold")
        )
        self.send_button.grid(column=3, row=0, padx=5, pady=5)

        # Command blocks display area
        self.commands_frame = customtkinter.CTkFrame(self.bottom_part, fg_color="transparent")
        self.commands_frame.pack(fill="both", side="bottom", expand=True)
        
        self.commands_label = customtkinter.CTkLabel(self.commands_frame, text="Command Sequence", font=("Arial", 12, "bold"), anchor="w")
        self.commands_label.pack(side="top", padx=5, pady=(0, 5), fill="x")
        
        # Scrollable frame for command blocks
        self.commands_scrollable = customtkinter.CTkScrollableFrame(
            self.commands_frame,
            fg_color=("#e8e8e8", "#2b2b2b"),
            border_width=2,
            border_color=("#c0c0c0", "#404040"),
            corner_radius=8,
            height=200
        )
        self.commands_scrollable.pack(fill="both", side="bottom", expand=True)
        
        # Empty state message
        self.empty_label = customtkinter.CTkLabel(
            self.commands_scrollable,
            text="No commands yet. Add a movement or turn command to begin.",
            font=("Arial", 11, "italic"),
            text_color=("#888888", "#666666")
        )
        self.empty_label.pack(pady=40)
        
        # Store command block widgets
        self.command_blocks = []
        self.drag_data = {"widget": None, "start_y": 0, "original_index": 0}
        
        # Toast notification system
        self.toast_queue = []
        self.toast_showing = False

    def add_command_block(self, command_data):
        """Add a visual command block to the display"""
        # Hide empty state label if visible
        if self.empty_label.winfo_ismapped():
            self.empty_label.pack_forget()
        
        # Create command block frame
        block = customtkinter.CTkFrame(
            self.commands_scrollable,
            fg_color=("#ffffff", "#1e1e1e"),
            border_width=2,
            border_color=("#3b8ed0", "#1f6aa5"),
            corner_radius=8,
            height=60
        )
        block.pack(fill="x", padx=10, pady=5)
        
        # Determine command type and create content
        if command_data["cmd"] == "move":
            # Always forward now, so we can simplify the display
            cmd_type = "MOVE"
            cmd_color = ("#3b8ed0", "#1f6aa5")
            cmd_text = f"{command_data['d']}m forward"
        else:  # turn
            cmd_type = "TURN"
            cmd_color = ("#9775fa", "#7950f2")
            cmd_text = f"{command_data['a']}°"
        
        # Command type label (left side)
        type_label = customtkinter.CTkLabel(
            block,
            text=cmd_type,
            font=("Arial", 11, "bold"),
            text_color=cmd_color,
            width=60
        )
        type_label.pack(side="left", padx=(15, 10), pady=10)
        
        # Command details (center)
        details_label = customtkinter.CTkLabel(
            block,
            text=cmd_text,
            font=("Arial", 12),
            anchor="w"
        )
        details_label.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        # ID label (right side)
        id_label = customtkinter.CTkLabel(
            block,
            text=f"#{command_data['id']}",
            font=("Arial", 10),
            text_color=("#888888", "#666666"),
            width=50
        )
        id_label.pack(side="right", padx=(10, 5), pady=10)
        
        # Up/Down buttons for reordering
        button_frame = customtkinter.CTkFrame(block, fg_color="transparent", width=60)
        button_frame.pack(side="right", padx=(0, 10))
        
        up_btn = customtkinter.CTkButton(
            button_frame,
            text="↑",
            width=25,
            height=25,
            font=("Arial", 14),
            fg_color="transparent",
            hover_color=("#d0e8f5", "#2a4a6e"),
            border_width=1,
            border_color=("#c0c0c0", "#404040")
        )
        up_btn.pack(side="left", padx=2)
        
        down_btn = customtkinter.CTkButton(
            button_frame,
            text="↓",
            width=25,
            height=25,
            font=("Arial", 14),
            fg_color="transparent",
            hover_color=("#d0e8f5", "#2a4a6e"),
            border_width=1,
            border_color=("#c0c0c0", "#404040")
        )
        down_btn.pack(side="left", padx=2)
        
        # Store block reference
        block.command_data = command_data
        self.command_blocks.append(block)
        
        # Bind reorder buttons
        index = len(self.command_blocks) - 1
        up_btn.configure(command=lambda idx=index: self.move_command_up(idx))
        down_btn.configure(command=lambda idx=index: self.move_command_down(idx))
        
        return block
    
    def move_command_up(self, index):
        """Move a command block up in the sequence"""
        if index > 0:
            # Swap in the list
            self.command_blocks[index], self.command_blocks[index-1] = \
                self.command_blocks[index-1], self.command_blocks[index]
            
            # Reorder visually
            self._refresh_command_display()
    
    def move_command_down(self, index):
        """Move a command block down in the sequence"""
        if index < len(self.command_blocks) - 1:
            # Swap in the list
            self.command_blocks[index], self.command_blocks[index+1] = \
                self.command_blocks[index+1], self.command_blocks[index]
            
            # Reorder visually
            self._refresh_command_display()
    
    def remove_last_command_block(self):
        """Remove the last command block"""
        if self.command_blocks:
            block = self.command_blocks.pop()
            block.destroy()
            
            # Show empty state if no commands left
            if not self.command_blocks:
                self.empty_label.pack(pady=40)
    
    def clear_all_command_blocks(self):
        """Clear all command blocks"""
        for block in self.command_blocks:
            block.destroy()
        self.command_blocks.clear()
        self.empty_label.pack(pady=40)
    
    def get_command_sequence(self):
        """Get the ordered list of commands"""
        return [block.command_data for block in self.command_blocks]
    
    def _refresh_command_display(self):
        """Refresh the visual order of command blocks"""
        for block in self.command_blocks:
            block.pack_forget()
        
        for i, block in enumerate(self.command_blocks):
            block.pack(fill="x", padx=10, pady=5)
            
            # Update button commands with new indices
            button_frame = None
            for child in block.winfo_children():
                if isinstance(child, customtkinter.CTkFrame):
                    for btn_child in child.winfo_children():
                        if isinstance(btn_child, customtkinter.CTkButton):
                            if not button_frame:
                                button_frame = child
                                up_btn = btn_child
                            else:
                                down_btn = btn_child
            
            if button_frame:
                up_btn.configure(command=lambda idx=i: self.move_command_up(idx))
                down_btn.configure(command=lambda idx=i: self.move_command_down(idx))
    
    def show_toast(self, message, toast_type="error"):
        """Show a toast notification
        toast_type: 'error', 'success', 'info', 'warning'
        """
        # Color schemes for different toast types
        colors = {
            "error": {"bg": ("#ff6b6b", "#c92a2a"), "text": "#ffffff"},
            "success": {"bg": ("#51cf66", "#2f9e44"), "text": "#ffffff"},
            "info": {"bg": ("#3b8ed0", "#1f6aa5"), "text": "#ffffff"},
            "warning": {"bg": ("#ffa94d", "#fd7e14"), "text": "#000000"}
        }
        
        color_scheme = colors.get(toast_type, colors["error"])
        
        # Create toast frame
        toast = customtkinter.CTkFrame(
            self.root,
            fg_color=color_scheme["bg"],
            corner_radius=8,
            border_width=0
        )
        
        # Create message label
        label = customtkinter.CTkLabel(
            toast,
            text=message,
            font=("Arial", 12, "bold"),
            text_color=color_scheme["text"]
        )
        label.pack(padx=20, pady=12)
        
        # Position toast at bottom center
        toast.place(relx=0.5, rely=1.0, y=100, anchor="s")
        
        # Animate in
        self._animate_toast_in(toast)
        
        # Schedule hide after 3 seconds
        self.root.after(1000, lambda: self._animate_toast_out(toast))
    
    def _animate_toast_in(self, toast):
        """Animate toast sliding up from bottom"""
        target_y = -20
        current_y = 100
        step = 8
        
        def slide():
            nonlocal current_y
            if current_y > target_y:
                current_y -= step
                toast.place(relx=0.5, rely=1.0, y=current_y, anchor="s")
                self.root.after(10, slide)
            else:
                toast.place(relx=0.5, rely=1.0, y=target_y, anchor="s")
        
        slide()
    
    def _animate_toast_out(self, toast):
        """Animate toast sliding down and destroy"""
        current_y = -20
        target_y = 100
        step = 8
        
        def slide():
            nonlocal current_y
            if current_y < target_y:
                current_y += step
                toast.place(relx=0.5, rely=1.0, y=current_y, anchor="s")
                self.root.after(10, slide)
            else:
                toast.destroy()
        
        slide()

if __name__ == "__main__":
    gui = GUI()
    gui.root.mainloop()
