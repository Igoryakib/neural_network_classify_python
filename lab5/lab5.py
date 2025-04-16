import tkinter as tk
import tkinter.ttk as ttk
import os
import csv
import numpy as np
import pandas as pd

root = tk.Tk()
root.title("Dialog window")
root.geometry("570x400+350+0")

toplevel = None

entry_varW = tk.StringVar(value="50")
entry_varH = tk.StringVar(value="30")
bitmap_var = tk.StringVar(value="info")
bg_var = tk.StringVar(value="white")
fg_var = tk.StringVar(value="black")
cursor_var = tk.StringVar(value="arrow")


labelBitmap = tk.Label(
    root,
    bg=bg_var.get(),
    fg=fg_var.get(),
    bitmap=bitmap_var.get(),
    width=int(entry_varW.get()),
    height=int(entry_varH.get()),
    cursor=cursor_var.get(),
    anchor="center"
)
labelBitmap.pack(pady=10)


def close_toplevel():
    global toplevel
    if toplevel is not None:
        toplevel.grab_release()
        toplevel.destroy()
        toplevel = None


def handle_ok():
    labelBitmap.config(
        width=int(entry_varW.get()),
        height=int(entry_varH.get()),
        bg=bg_var.get(),
        fg=fg_var.get(),
        bitmap=bitmap_var.get(),
        cursor=cursor_var.get()
    )
    save_data()
    close_toplevel()

def handle_cancel():
    close_toplevel()
    
def save_data():
    data = [bitmap_var.get(), bg_var.get(), fg_var.get(), cursor_var.get()]
    file_exists = os.path.isfile("dataset.csv")

    with open("dataset.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["bitmap", "bg", "fg", "cursor"])
        writer.writerow(data)
        
def read_data():
    line = pd.read_csv("dataset.csv")   
    intermediateData = line[["bitmap", "bg", "fg", "cursor"]].values
    result = [[item[0], list(item[1:len(item)])] for item in intermediateData]
    return result    

def suggestBestChoice(event):
    arrayData = read_data()
    def changeData(bg, fg, cursor):
        bg_var.set(bg)
        fg_var.set(fg)
        cursor_var.set(cursor)
    list(map(lambda item: changeData(*item[1]) if bitmap_var.get() in item else -1, arrayData))

def handle_adjust():
    global toplevel
    if toplevel is not None:
        return

    toplevel = tk.Toplevel()
    toplevel.title("Налаштування Label")
    toplevel.resizable(False, False)
    toplevel.protocol("WM_DELETE_WINDOW", close_toplevel)


    ttk.Label(toplevel, text="Width:").pack(anchor="w", padx=5)
    ttk.Entry(toplevel, textvariable=entry_varW).pack(fill="x", padx=5, pady=2)

    ttk.Label(toplevel, text="Height:").pack(anchor="w", padx=5)
    ttk.Entry(toplevel, textvariable=entry_varH).pack(fill="x", padx=5, pady=2)

    ttk.Label(toplevel, text="Bitmap:").pack(anchor="w", padx=5)
    bitmap_combo = ttk.Combobox(toplevel, textvariable=bitmap_var, values=[
        "error", "gray75", "gray50", "gray25", "gray12",
        "hourglass", "info", "questhead", "question", "warning"
    ])
    bitmap_combo.bind("<<ComboboxSelected>>", suggestBestChoice)
    bitmap_combo.pack(fill="x", padx=5, pady=2)

    ttk.Label(toplevel, text="Background color:").pack(anchor="w", padx=5)
    ttk.Entry(toplevel, textvariable=bg_var).pack(fill="x", padx=5, pady=2)

    ttk.Label(toplevel, text="Foreground color:").pack(anchor="w", padx=5)
    ttk.Entry(toplevel, textvariable=fg_var).pack(fill="x", padx=5, pady=2)

    ttk.Label(toplevel, text="Cursor:").pack(anchor="w", padx=5)
    cursor_combo = ttk.Combobox(toplevel, textvariable=cursor_var, values=[
        "arrow", "circle", "cross", "hand2", "heart", "plus", "watch", "xterm"
    ])
    cursor_combo.pack(fill="x", padx=5, pady=2)

    tk.Button(toplevel, text="OK", command=handle_ok, width=10).pack(pady=5)
    tk.Button(toplevel, text="Cancel", command=handle_cancel, width=10).pack()

    toplevel.grab_set()

tk.Button(root, text="Adjust", command=handle_adjust).pack(pady=10)

root.mainloop()
