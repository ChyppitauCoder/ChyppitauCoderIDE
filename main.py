import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import subprocess

class IDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Code IDE")

        self.text_area = tk.Text(self, wrap="word")
        self.text_area.pack(fill="both", expand=True)
        self.text_area.bind("<BackSpace>", self.delete_char)
        self.text_area.bind("<Up>", self.move_up)
        self.text_area.bind("<Down>", self.move_down)

        self.save_button = tk.Button(self, text="Save", command=self.save_file)
        self.save_button.pack(side="left")
        self.run_button = tk.Button(self, text="Run(Alpha)", command=self.run_code)
        self.run_button.pack(side="left")

    def delete_char(self, event):
        current_pos = self.text_area.index(tk.INSERT)
        if current_pos != "1.0":
            prev_pos = self.text_area.index(f"{current_pos} - 1 chars")
            self.text_area.delete(prev_pos, current_pos)
        return "break"  # Отменяем стандартное действие Backspace

    def move_up(self, event):
        current_line = int(self.text_area.index(tk.INSERT).split(".")[0])
        if current_line > 1:
            prev_line = current_line - 1
            self.text_area.tag_remove("insert", "1.0", "end")
            self.text_area.mark_set("insert", f"{prev_line}.0")
        return "break"  # Отменяем стандартное действие стрелки вверх

    def move_down(self, event):
        current_line = int(self.text_area.index(tk.INSERT).split(".")[0])
        total_lines = int(self.text_area.index("end-1c").split(".")[0])
        if current_line < total_lines:
            next_line = current_line + 1
            self.text_area.tag_remove("insert", "1.0", "end")
            self.text_area.mark_set("insert", f"{next_line}.0")
        return "break"  # Отменяем стандартное действие стрелки вниз

    def save_file(self):
        content = self.text_area.get("1.0", "end-1c")
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(content)
            messagebox.showinfo("Saved", "File saved successfully.")

    def run_code(self):
        content = self.text_area.get("1.0", "end-1c")
        file_path = "temp_script.py"
        with open(file_path, "w") as file:
            file.write(content)
        try:
            result = subprocess.run(["python", file_path], capture_output=True, text=True)
            output = result.stdout.strip()
            error = result.stderr.strip()
            if error:
                messagebox.showerror("Error", error)
            else:
                messagebox.showinfo("Output", output)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            subprocess.run(["rm", file_path], capture_output=True)

if __name__ == "__main__":
    ide = IDE()
    ide.mainloop()
