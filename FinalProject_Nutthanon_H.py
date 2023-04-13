# Import libraries that require 
import os
import shutil
import tkinter as tk
from tkinter import filedialog

#Todo: Define file categories dictionary
file_categories = {
    ".txt" : "Text",
    ".jpg" : "Images",
    ".jpeg": "Images",
    ".png" : "Images",
    ".pdf" : "Documents",
    ".xlsx": "Excel",
    ".py"  : "Python",
    ".docx": "Microsoft Word",
    
}

#Todo: Function to organize files by moving them into categorized folders
def organize_files(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)

        if os.path.isfile(file_path):
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in file_categories:
                category = file_categories[file_extension]
                category_folder = os.path.join(path, category)

                if not os.path.exists(category_folder):
                    os.makedirs(category_folder)

                destination = os.path.join(category_folder, file)
                shutil.move(file_path, destination)

#Todo: Function to open a directory browsing dialog and organize the chosen directory
def browse_directory():
    directory_to_organize = filedialog.askdirectory()
    organize_files(directory_to_organize)
    result_label.config(text="Files have been organized!")

#Todo: Function to initiate the organization process
def start_organization():
    main.update()
    browse_directory()

main = tk.Tk()
main.title("File Organizer")
main.geometry("300x200")
main.config(bg="#1DB954")

#Todo: Create and display the title label
title_label = tk.Label(main, text="File Organizer Program", font=("Arial", 18), fg="#1DB954", bg="#191414")
title_label.pack(pady=20)

#Todo: Create and display the browse button
browse_button = tk.Button(main, text="Select Folder", command=start_organization, fg="#1DB954", bg="#191414", font=("Arial", 12))
browse_button.pack(pady=10)

#Todo: Create and display the result label
result_label = tk.Label(main, text="", font=("Arial", 12), fg="#1DB954", bg="#191414")
result_label.pack(pady=10)

main.mainloop()