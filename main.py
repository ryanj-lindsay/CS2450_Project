import sys
from uvsim import *
from gui import *

def main():
    if len(sys.argv) >= 2:
        file = sys.argv[1]
        with open(file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        sim = UVSim()
        sim.load(lines)
        try:
            sim.run()
        except (ValueError, IndexError, ZeroDivisionError, RuntimeError) as e:
            print(f"Runtime error: {e}")
            sys.exit(1)
        return

    import threading, queue, tkinter as tk
    from tkinter import filedialog, messagebox

    class GUIRunner(UVSimGUI):
        def __init__(self, root):
            super().__init__(root)
            import threading, queue
            self._inbox = queue.Queue()
            self.sim = UVSim(input_function=self._gui_input, output_function=self._gui_output)

            self.enter_button.config(command=self._enter_click)
            self.upload_button.config(command=self._upload_and_run)

            self._runner_thread = None
            self._running = False
            
            self.reset_button.config(command=self._reset)


        def _gui_output(self, value):
            self.root.after(0, lambda: self._append(str(value)))

        def _gui_input(self) -> int:
            while True:
                self._gui_output("Enter a word (-9999 - 9999): ")
                raw = self._inbox.get()
                if not self._running:
                    raise RuntimeError("Input cancelled")
                try:
                    value = int(raw)
                    if -9999 <= value <= 9999:
                        return value
                    else:
                        self._gui_output("Invalid input: out of range. Please try again.")
                except ValueError:
                    self._gui_output("Invalid input: please enter an integer.")

                    
        def _set_running(self, is_running: bool):
            self._running = is_running
            state = ("disabled" if is_running else "normal")
            self.upload_button.config(state=state)
            self.user_input.config(state="normal")
            self.enter_button.config(state="normal")

        def _stop_if_running(self):
            if self._runner_thread and self._runner_thread.is_alive():
                self.sim.running = False
                try:
                    self._inbox.put_nowait(0)
                except Exception:
                    pass
                self._runner_thread.join(timeout=1.0)

        def _reset(self):  
            self._stop_if_running()
            import queue
            self._inbox = queue.Queue()
            self.sim = UVSim(input_function=self._gui_input, output_function=self._gui_output)
            self.output_screen.delete("1.0", tk.END)
            self.user_input.delete(0, tk.END)
            self.output_screen.insert(tk.END, "Click 'Upload' to upload a text file with BasicML commands to start.\n")
            self.output_screen.see(tk.END)
            self._set_running(False)

        def _append(self, text: str):
            self.output_screen.insert(tk.END, text + "\n")
            self.output_screen.see(tk.END)

        def handle_enter(self, event=None):
            user_text = self.user_input.get()
            if user_text.strip():
                self._append(f"> {user_text}")
                self._inbox.put(user_text.strip())
                self.user_input.delete(0, tk.END)
            else:
                messagebox.showwarning("Input Error", "Please enter a command.")

        def _enter_click(self):
            self.handle_enter()

        def _upload_and_run(self):
            from tkinter import filedialog, messagebox
            file_path = filedialog.askopenfilename(
                title="Select a BasicML program",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if not file_path:
                return

            self._stop_if_running()

            import queue
            self._inbox = queue.Queue()

            try:
                with open(file_path, "r") as f:
                    lines = [line.strip() for line in f if line.strip()]
                self.sim = UVSim( 
                    input_function=self._gui_input,
                    output_function=self._gui_output
                )
                self.sim.load(lines)
            except Exception as e:
                messagebox.showerror("Load Error", f"{e}")
                return

            self._append(f"[Program loaded: {file_path}]")
            self._append("[Running…]")
            self._set_running(True)

            import threading
            def _run():
                try:
                    self.sim.run()
                    self._gui_output("[Program halted]")
                except (ValueError, IndexError, ZeroDivisionError) as e:
                    self._gui_output(f"Runtime error: {e}")
                except RuntimeError as e:
                    self._gui_output(f"[Stopped] {e}")
                except Exception as e:
                    self._gui_output(f"Unexpected error: {e}")
                finally:
                    self.root.after(0, lambda: self._set_running(False))

            self._runner_thread = threading.Thread(target=_run, daemon=True)
            self._runner_thread.start()


    root = tk.Tk()
    app = GUIRunner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
