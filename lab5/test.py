import tkinter as tk
import tkinter.ttk as ttk
from tkinter import colorchooser

top_level = None

root = tk.Tk()
root.title("Налаштування Label - Варіант 19")

text_var = tk.StringVar(value="tk.Label")
size_var = tk.IntVar()
bg_var = tk.StringVar(value="white")
bd_var = tk.IntVar()
relief_var = tk.StringVar()

def handle_close():
    global top_level
    if top_level:
        top_level.destroy()
        top_level = None

def handle_ok():
    size = int(size_var.get())
    label.config(
        text=text_var.get(),
        width=size,
        height=size,
        bg=bg_var.get(),
        bd=bd_var.get(),
        relief=relief_var.get()
    )
    handle_close()

def handle_cancel():
    handle_close()

def choose_color():
    try:
        color = colorchooser.askcolor(initialcolor=bg_var.get())[1]
        if color:
            bg_var.set(color)
            color_button.config(bg=color)
    except:
        print("Color chooser failed")

def handle_adjust():
    global top_level
    if top_level is not None:
        return

    top_level = tk.Toplevel(root)
    top_level.title("Налаштування параметрів")
    top_level.resizable(False, False)
    top_level.protocol("WM_DELETE_WINDOW", handle_close)

    # Mac-friendly window handling
    top_level.lift()
    top_level.focus_force()
    top_level.after(100, lambda: top_level.focus_force())

    text_var.set(label.cget("text"))
    size_var.set(label.cget("width"))
    bg_var.set(label.cget("bg"))
    bd_var.set(label.cget("bd"))
    relief_var.set(label.cget("relief"))

    frame_text = tk.LabelFrame(top_level, text="Текст:")
    frame_text.pack(padx=10, pady=5, fill=tk.X)
    entry_text = tk.Entry(frame_text, textvariable=text_var, width=20)
    entry_text.pack(padx=5, pady=5)
    entry_text.focus_set()  # 👈 дає фокус на введення одразу

    frame_size = tk.LabelFrame(top_level, text="Ширина=Висота:")
    frame_size.pack(padx=10, pady=5, fill=tk.X)
    spin_size = tk.Spinbox(frame_size, textvariable=size_var, from_=1, to=20, width=15)
    spin_size.pack(padx=5, pady=5)

    frame_bg = tk.LabelFrame(top_level, text="Колір фону:")
    frame_bg.pack(padx=10, pady=5, fill=tk.X)

    global color_button
    color_button = tk.Button(frame_bg, text="Вибрати колір", bg=bg_var.get(), width=15, command=choose_color)
    color_button.pack(padx=5, pady=5)

    frame_bd = tk.LabelFrame(top_level, text="Товщина межі:")
    frame_bd.pack(padx=10, pady=5, fill=tk.X)
    spin_bd = tk.Spinbox(frame_bd, textvariable=bd_var, from_=0, to=10, width=15)
    spin_bd.pack(padx=5, pady=5)

    frame_relief = tk.LabelFrame(top_level, text="Стиль межі:")
    frame_relief.pack(padx=10, pady=5, fill=tk.X)
    relief_options = ["flat", "raised", "sunken", "ridge", "solid", "groove"]
    combo_relief = ttk.Combobox(frame_relief, textvariable=relief_var, values=relief_options, width=15, state="readonly")
    combo_relief.pack(padx=5, pady=5)

    buttons_frame = tk.Frame(top_level)
    buttons_frame.pack(padx=10, pady=10, fill=tk.X)
    button_ok = tk.Button(buttons_frame, text="Ok", width=15, command=handle_ok)
    button_ok.pack(side=tk.LEFT, padx=5)
    button_cancel = tk.Button(buttons_frame, text="Cancel", width=15, command=handle_cancel)
    button_cancel.pack(side=tk.RIGHT, padx=5)

label = tk.Label(
    root,
    text="tk.Label",
    width=10,
    height=10,
    bg="white",
    bd=2,
    relief="raised"
)
label.pack(padx=20, pady=20)

button_adjust = tk.Button(
    root,
    text="Adjust",
    width=10,
    command=handle_adjust
)
button_adjust.pack(pady=10)

root.mainloop()