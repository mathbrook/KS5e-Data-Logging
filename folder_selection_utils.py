import tkinter as tk
from tkinter import filedialog

def select_folder_and_get_path():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    folder_path = filedialog.askdirectory()
    
    if folder_path:
        print(f"Selected folder path: {folder_path}")
        return folder_path
    else:
        print("No folder selected")
        return None

# # Call the method to select a folder and get its path
# selected_folder_path = select_folder_and_get_path()

# if selected_folder_path:
#     # Use the selected folder path for further operations
#     pass