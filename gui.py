import os
import platform
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess

class FileExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("File Explorer")
       
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(expand=True, fill='both')
       
        self.tree.bind("<Double-1>", self.on_double_click)
       
        self.populate_tree()
   
    def populate_tree(self, starting_dir="."):
        self.tree.delete(*self.tree.get_children())
        self.populate_tree_recursively(starting_dir, '')
   
    def populate_tree_recursively(self, folder_path, parent):
        folders = []
        files = []
        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path):
                    folders.append(item)
                else:
                    files.append(item)
        except PermissionError:
            messagebox.showerror("Permission Error", f"Permission denied: {folder_path}")
            return

        for folder in sorted(folders):
            folder_id = self.tree.insert(parent, 'end', text=folder, open=False)
            self.populate_tree_recursively(os.path.join(folder_path, folder), folder_id)

        for file in sorted(files):
            self.tree.insert(parent, 'end', text=file)
   
    def on_double_click(self, event):
        item = self.tree.selection()[0]
        item_text = self.tree.item(item, "text")
        item_path = self.get_item_path(item)
       
        if os.path.isdir(item_path):
            self.populate_tree(item_path)
        else:
            if platform.system() == 'Windows':
                os.startfile(item_path)
            else:
                subprocess.Popen(['xdg-open', item_path])
   
    def get_item_path(self, item):
        item_path = self.tree.item(item, "text")
        parent = item
        while parent:
            parent = self.tree.parent(parent)
            if parent:
                item_path = os.path.join(self.tree.item(parent, "text"), item_path)
        return item_path

if __name__ == "__main__":
    root = tk.Tk()
    file_explorer = FileExplorer(root)
    root.mainloop()
