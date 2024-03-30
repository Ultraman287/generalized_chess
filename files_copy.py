from tkinter import *
from tkinter import ttk
from tkinter import filedialog


class CopyRepository:
    filePaths = []

    def __init__(self, root):
        self.root = root

        root.title("Copy Repository")
        root.minsize(200, 200)  # Set the minimum size of the root window

        mainframe = ttk.Frame(root, padding="3 3 12 12", width=600, height=400)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        button = ttk.Button(mainframe, text="Select Source", command=self.select_source)
        button.grid(column=1, row=1, sticky=W)

        copy_button = ttk.Button(
            mainframe, text="Copy to Clipboard", command=self.copy_to_clipboard
        )
        copy_button.grid(column=1, row=2, sticky=W)

    def copy_to_clipboard(self):
        to_copy = ""

        for f in self.filePaths:
            to_copy += "This file is located at " + f + "\n\n"
            with open(f, "r") as file:
                to_copy += file.read() + "\n\n\n"
        self.root.clipboard_clear()
        self.root.clipboard_append(to_copy)

        print("Copied to clipboard")

    def select_source(self):
        files = filedialog.askopenfilename(multiple=True)
        var = root.tk.splitlist(files)
        for f in var:
            if f not in self.filePaths:
                self.filePaths.append(f)

        print(self.filePaths)


root = Tk()
CopyRepository(root)
root.mainloop()
