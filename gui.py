import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, colorchooser

def rgb_to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"

class UVSimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UVsim")
        self.root.geometry("1200x900")

        self.theme = {
            "primary": rgb_to_hex(76, 114, 29),
            "off": rgb_to_hex(255, 255, 255),
        }

        # Output Screen
        self.output_screen = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 14))
        self.output_screen.pack(expand=True, fill="both", padx=5, pady=5)

        self.output_screen.insert(tk.END, "Click 'Upload' to upload a text file with BasicML commands to start.\n")
        self.output_screen.see(tk.END)

        # Bottom frame for user input
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.user_input = tk.Entry(self.bottom_frame, font=("Courier", 18))
        self.user_input.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10, pady=15)
        self.user_input.bind("<Return>", self.handle_enter)

        self.upload_button = tk.Button(self.bottom_frame, text="Upload", command=self.upload_file, height=2)
        self.upload_button.pack(side=tk.RIGHT, padx=2)

        self.reset_button = tk.Button(self.bottom_frame, text="Reset", height=2, width=7, command=self.reset_ui)
        self.reset_button.pack(side=tk.RIGHT, padx=2)

        self.enter_button = tk.Button(self.bottom_frame, text="Enter", command=self.handle_enter, height=2, width=7)
        self.enter_button.pack(side=tk.RIGHT, padx=2)

        # Menubar
        menubar = tk.Menu(root)
        # File menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Close", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Edit file", command=lambda: None)
        menubar.add_cascade(label='Edit', menu=editmenu)

        # Theme menu
        thememenu = tk.Menu(menubar, tearoff=0)
        thememenu.add_command(label="Set Primary Color…", command=self.choose_primary)
        thememenu.add_command(label="Set Off Color…", command=self.choose_off)
        thememenu.add_separator()
        thememenu.add_command(label="Swap Colors", command=self.swap_colors)
        thememenu.add_command(label="Reset Default Theme", command=self.reset_theme)
        menubar.add_cascade(label="Theme", menu=thememenu)

        self.root.config(menu=menubar)

        # Keep references to things we recolor together
        self._buttons = [self.upload_button, self.reset_button, self.enter_button]
        self._menus = [menubar, filemenu, editmenu, thememenu]

        self.apply_theme()

    def apply_theme(self):
        primary = self.theme["primary"]
        off = self.theme["off"]

        # Window & frames
        self.root.configure(bg=off)
        self.bottom_frame.configure(bg=off)

        # - Use off for background, dark text for readability, primary as selection & cursor
        self.output_screen.configure(
            bg=off,
            fg="#111111",
            insertbackground=primary,  # caret color
            selectbackground=primary,
            selectforeground="#FFFFFF"
        )
        self.output_screen.configure(highlightthickness=1, highlightbackground=primary)

        # Entry
        self.user_input.configure(
            bg="#FFFFFF",
            fg="#111111",
            insertbackground=primary,
            highlightthickness=1,
            highlightbackground=primary,
            relief="solid",
            bd=1
        )

        # Buttons (primary background, off/white text)
        for btn in self._buttons:
            btn.configure(
                bg=primary,
                fg="#FFFFFF",
                activebackground=primary,
                activeforeground="#FFFFFF",
                relief="raised",
                bd=1,
                highlightthickness=0
            )

        # Menus
        try:
            self.root.option_add("*Menu.background", off)
            self.root.option_add("*Menu.foreground", "#111111")
            self.root.option_add("*Menu.activeBackground", primary)
            self.root.option_add("*Menu.activeForeground", "#FFFFFF")
        except Exception:
            pass

    def choose_primary(self):
        color_tuple = colorchooser.askcolor(title="Choose Primary Color", initialcolor=self.theme["primary"])
        if color_tuple and color_tuple[1]:
            self.theme["primary"] = color_tuple[1]
            self.apply_theme()

    def choose_off(self):
        color_tuple = colorchooser.askcolor(title="Choose Off Color", initialcolor=self.theme["off"])
        if color_tuple and color_tuple[1]:
            self.theme["off"] = color_tuple[1]
            self.apply_theme()

    def swap_colors(self):
        self.theme["primary"], self.theme["off"] = self.theme["off"], self.theme["primary"]
        self.apply_theme()

    def reset_theme(self):
        self.theme["primary"] = rgb_to_hex(76, 114, 29)   # #4C721D
        self.theme["off"] = rgb_to_hex(255, 255, 255)     # white
        self.apply_theme()

    def handle_enter(self, event=None):
        user_text = self.user_input.get()
        if user_text.strip():
            self.output_screen.insert(tk.END, f"> {user_text}\n")
            self.output_screen.see(tk.END)
            self.user_input.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a command.")

    def upload_file(self):
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            self.output_screen.insert(tk.END, f"[Uploaded file: {file_path}]\n")
            self.output_screen.see(tk.END)

    def reset_ui(self):
        # Clear the screen and reprint the starter hint; keep theme as-is
        self.output_screen.delete("1.0", tk.END)
        self.output_screen.insert(tk.END, "Click 'Upload' to upload a text file with BasicML commands to start.\n")
        self.output_screen.see(tk.END)
        self.user_input.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = UVSimGUI(root)
    root.mainloop()
