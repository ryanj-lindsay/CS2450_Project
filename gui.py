import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

class UVSimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UVsim")
        self.root.geometry("1200x900")
        
        # Output Screen
        self.output_screen = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 14))
        self.output_screen.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Bottom frame for user input
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.user_input = tk.Entry(bottom_frame, font=("Courier", 18))
        self.user_input.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10, pady=15)

        self.user_input.bind("<Return>", self.handle_enter)

        self.upload_button = tk.Button(bottom_frame, text="Upload", command=self.upload_file, height=2)
        self.upload_button.pack(side=tk.RIGHT, padx=2)
        
        self.enter_button = tk.Button(bottom_frame, text="Enter", command=self.handle_enter, height=2, width=8)
        self.enter_button.pack(side=tk.RIGHT, padx=2)
        
        # Menu Bar with "Close"
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Close", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

    def handle_enter(self, event=None):
        user_text = self.user_input.get()
        if user_text.strip():
            self.output_screen.insert(tk.END, f"> {user_text}\n")
            self.user_input.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a command.")

    def upload_file(self):
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            self.output_screen.insert(tk.END, f"[Uploaded file: {file_path}]\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = UVSimGUI(root)
    root.mainloop()
