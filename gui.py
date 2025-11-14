import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, colorchooser
import os
import json

class UVSimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UVsim")
        self.root.geometry("1200x900")
        
        self.current_file_path = None
        self.program_data = []
        
        self.load_color_scheme()
        self.apply_color_scheme()
        self.create_menu()
        
        main_frame = tk.Frame(root, bg=self.primary_color)
        main_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        left_frame = tk.Frame(main_frame, bg=self.primary_color)
        left_frame.pack(side=tk.LEFT, expand=True, fill="both", padx=(0, 5))
        
        tk.Label(left_frame, text="Program Instructions (000-249)", 
                 font=("Courier", 12, "bold"), bg=self.primary_color, 
                 fg=self.off_color).pack()
        
        self.instruction_editor = scrolledtext.ScrolledText(
            left_frame, wrap=tk.WORD, font=("Courier", 12), 
            width=40, bg="white", fg="black"
        )
        self.instruction_editor.pack(expand=True, fill="both")
        
        right_frame = tk.Frame(main_frame, bg=self.primary_color)
        right_frame.pack(side=tk.RIGHT, expand=True, fill="both")
        
        tk.Label(right_frame, text="Output", font=("Courier", 12, "bold"), 
                 bg=self.primary_color, fg=self.off_color).pack()
        
        self.output_screen = scrolledtext.ScrolledText(
            right_frame, wrap=tk.WORD, font=("Courier", 14), 
            bg="white", fg="black"
        )
        self.output_screen.pack(expand=True, fill="both")
        
        self.output_screen.insert(tk.END, "Welcome to UVsim!\n")
        self.output_screen.insert(tk.END, "Click 'File -> Open' to load a BasicML file.\n")
        self.output_screen.insert(tk.END, "Once loaded you may edit the instructions, then click 'Run' to execute.\n")
        self.output_screen.see(tk.END)
        
        bottom_frame = tk.Frame(root, bg=self.primary_color)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.user_input = tk.Entry(bottom_frame, font=("Courier", 18))
        self.user_input.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10, pady=15)
        self.user_input.bind("<Return>", self.handle_enter)
        
        self.run_button = tk.Button(
            bottom_frame, text="Run", height=2, width=7,
            command=self.run_program, bg=self.off_color,
            fg=self.primary_color
        )
        self.run_button.pack(side=tk.RIGHT, padx=2)
        
        self.reset_button = tk.Button(
            bottom_frame, text="Reset", height=2, width=7, 
            command=self.reset_program, bg=self.off_color, 
            fg=self.primary_color
        )
        self.reset_button.pack(side=tk.RIGHT, padx=2)
        
        self.enter_button = tk.Button(
            bottom_frame, text="Enter", command=self.handle_enter, 
            height=2, width=7, bg=self.off_color, fg=self.primary_color
        )
        self.enter_button.pack(side=tk.RIGHT, padx=2)
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_command(label="Save As", command=self.save_file_as)
        filemenu.add_separator()
        filemenu.add_command(label="Close", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        settingsmenu = tk.Menu(menubar, tearoff=0)
        settingsmenu.add_command(label="Change Color Scheme", command=self.change_colors)
        settingsmenu.add_command(label="Reset to Default Colors", command=self.reset_colors)
        menubar.add_cascade(label="Settings", menu=settingsmenu)
        
        self.root.config(menu=menubar)
    
    def load_color_scheme(self):
        config_file = "config.json"
        default_primary = "#4C721D"
        default_off = "#FFFFFF"
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.primary_color = config.get("primary_color", default_primary)
                    self.off_color = config.get("off_color", default_off)
            except:
                self.primary_color = default_primary
                self.off_color = default_off
        else:
            self.primary_color = default_primary
            self.off_color = default_off
    
    def save_color_scheme(self):
        config_file = "config.json"
        config = {
            "primary_color": self.primary_color,
            "off_color": self.off_color
        }
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    def apply_color_scheme(self):
        self.root.configure(bg=self.primary_color)
    
    def change_colors(self):
        primary = colorchooser.askcolor(
            title="Choose Primary Color",
            initialcolor=self.primary_color
        )
        
        if primary[1]:
            self.primary_color = primary[1]
            
            off = colorchooser.askcolor(
                title="Choose Secondary Color",
                initialcolor=self.off_color
            )
            
            if off[1]:
                self.off_color = off[1]
                self.save_color_scheme()
                
                messagebox.showinfo(
                    "Color Scheme Saved",
                    "Color scheme saved! Restart the app to see changes."
                )
    
    def reset_colors(self):
        self.primary_color = "#4C721D"
        self.off_color = "#FFFFFF"
        self.save_color_scheme()
        
        messagebox.showinfo(
            "Colors Reset",
            "Colors reset to UVU defaults! Restart the app to see changes."
        )
    
    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a BasicML file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            self.current_file_path = file_path
            self.load_file_content(file_path)
    
    def load_file_content(self, file_path):
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                self.program_data = []
                self.instruction_editor.delete(1.0, tk.END)
                
                for i, line in enumerate(lines):
                    if i >= 100:
                        self.output_screen.insert(
                            tk.END,
                            f"Warning: File has more than 100 entries. Only first 100 loaded.\n"
                        )
                        break
                    
                    line = line.strip()
                    if line:
                        self.program_data.append(line)
                        self.instruction_editor.insert(
                            tk.END,
                            f"{i:02d}: {line}\n"
                        )
                
                self.output_screen.insert(
                    tk.END,
                    f"Loaded {len(self.program_data)} instructions from {file_path}\n"
                )
                self.output_screen.insert(
                    tk.END,
                    "Edit instructions as needed, then click 'Run' to execute.\n"
                )
                self.output_screen.see(tk.END)
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not load file:\n{str(e)}")
    
    def save_file(self):
        if self.current_file_path:
            self.save_to_file(self.current_file_path)
        else:
            self.save_file_as()
    
    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            title="Save BasicML file as",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            self.current_file_path = file_path
            self.save_to_file(file_path)
    
    def save_to_file(self, file_path):
        try:
            content = self.instruction_editor.get(1.0, tk.END)
            lines = content.strip().split('\n')
            instructions = []
            
            for line in lines:
                if ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        instruction = parts[1].strip()
                        if instruction:
                            instructions.append(instruction)
            
            if len(instructions) > 100:
                instructions = instructions[:100]
                messagebox.showwarning(
                    "Too Many Instructions",
                    "Only the first 100 instructions were saved."
                )
            
            with open(file_path, 'w') as f:
                for instruction in instructions:
                    f.write(instruction + '\n')
            
            self.output_screen.insert(
                tk.END,
                f"Saved {len(instructions)} instructions to {file_path}\n"
            )
            self.output_screen.see(tk.END)
            
            messagebox.showinfo("Success", f"File saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{str(e)}")
    
    def run_program(self):
        pass
    
    def reset_program(self):
        self.instruction_editor.delete(1.0, tk.END)
        self.output_screen.delete(1.0, tk.END)
        self.program_data = []
        self.current_file_path = None
        
        self.output_screen.insert(tk.END, "Program reset. Load a new file to begin.\n")
        self.output_screen.see(tk.END)
    
    def handle_enter(self, event=None):
        user_text = self.user_input.get()
        if user_text.strip():
            self.output_screen.insert(tk.END, f"> {user_text}\n")
            self.output_screen.see(tk.END)
            self.user_input.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a command.")
    
    def upload_file(self):
        self.open_file()

if __name__ == "__main__":
    root = tk.Tk()
    app = UVSimGUI(root)
    root.mainloop()