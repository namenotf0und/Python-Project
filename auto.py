import os
import glob
import tkinter as tk
from tkinter import filedialog, messagebox

def delete_files_by_extension(folder_path, file_extension):
    """
    Deletes files with a specified extension in the given folder.

    Args:
        folder_path (str): The path to the folder where files should be deleted.
        file_extension (str): The extension of the files to delete (e.g., ".txt", ".log").
    """
    try:
        # Ensure the extension starts with a dot
        if not file_extension.startswith("."):
            file_extension = "." + file_extension

        # Construct the search pattern
        search_pattern = os.path.join(folder_path, f"*{file_extension}")

        # Find all files matching the pattern
        files_to_delete = glob.glob(search_pattern)

        if not files_to_delete:
            messagebox.showinfo("Result", f"No files with extension '{file_extension}' found in {folder_path}.")
            return

        deleted_files = []

        # Iterate and delete files
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                deleted_files.append(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

        if deleted_files:
            history_textbox.config(state=tk.NORMAL)
            for file in deleted_files:
                history_textbox.insert(tk.END, f"Deleted: {file}\n")
            history_textbox.config(state=tk.DISABLED)

        messagebox.showinfo("Result", f"Deleted {len(deleted_files)} file(s) with extension '{file_extension}'.")

    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)

def start_deletion():
    folder = folder_entry.get().strip()
    extension = extension_entry.get().strip()

    if not os.path.exists(folder):
        messagebox.showerror("Error", "The specified folder does not exist.")
        return

    if not extension:
        messagebox.showerror("Error", "Please enter a file extension.")
        return

    delete_files_by_extension(folder, extension)

# Create the GUI window
app = tk.Tk()
app.title("File Deletion Tool")
app.geometry("500x400")

# Folder selection
tk.Label(app, text="Folder Path:").pack(pady=5)
folder_entry = tk.Entry(app, width=50)
folder_entry.pack(pady=5)

tk.Button(app, text="Browse", command=browse_folder).pack(pady=5)

# File extension input
tk.Label(app, text="File Extension (e.g., .txt):").pack(pady=5)
extension_entry = tk.Entry(app, width=20)
extension_entry.pack(pady=5)

# Delete button
tk.Button(app, text="Delete Files", command=start_deletion).pack(pady=20)

# History log
tk.Label(app, text="Deletion History:").pack(pady=5)
history_textbox = tk.Text(app, width=60, height=10, state=tk.DISABLED)
history_textbox.pack(pady=5)

# Run the GUI event loop
app.mainloop()
