import tkinter as tk
import random as rnd
from PIL import Image, ImageTk
import time

root = tk.Tk()
root.title("Опитувальник/Казіно")
root.geometry("650x700+350+0")

DATA = ["apple", "banana", "cherry"]
IMAGES = {fruit: ImageTk.PhotoImage(Image.open(f"D:/КросДодатки/lab2/{fruit}.png").resize((100, 100))) for fruit in DATA}

# Entry ---------------------------------------------------------------
entry_var = tk.StringVar()
entry = tk.Entry(
    bg="white",
    font=("Arial", 14, "normal"),
    textvariable=entry_var,
    width=13
)
entry.pack()

# Radiobutton  --------------------------------------------------------
radio_var = tk.StringVar(value="apple")
radioFrame = tk.LabelFrame(
    text="Radiobutton",
    font=("Arial", 14, "normal"),
)
radioFrame.pack(padx=5, pady=5)

for item in DATA:
    radioButton = tk.Radiobutton(
        radioFrame,
        variable=radio_var,
        text=item.capitalize(),
        value=item,
        font=("Arial", 14, "normal"),
    )
    radioButton.pack(anchor="w")

# Checkbutton  --------------------------------------------------------
check_vars = {}
checkFrame = tk.LabelFrame(
    text="CheckButton",
    font=("Arial", 14, "normal"),
)
checkFrame.pack(padx=5, pady=5)

for item in DATA:
    var = tk.BooleanVar(value=False)
    check_vars[item] = var
    checkButton = tk.Checkbutton(
        checkFrame,
        text=item.capitalize(),
        variable=var,
        onvalue=True,
        offvalue=False,
        font=("Arial", 14, "normal"),
    )
    checkButton.pack(anchor="w")

# Spinbox -------------------------------------------------------------
spin_var = tk.StringVar(value="apple")
spinbox = tk.Spinbox(
    textvariable=spin_var,
    values=DATA,
    state="readonly",
)
spinbox.pack(padx=5, pady=5)

# OptionMenu ----------------------------------------------------------
option_var = tk.StringVar(value="apple")
optionmenu = tk.OptionMenu(
    root, option_var, *DATA)
optionmenu.pack(padx=5, pady=5)

# Label для результату ------------------------------------------------
label = tk.Label(bg="white", font=("Arial", 14, "bold"), width=50, height=3)
label.pack()

# Фрейм для зображень слотів ------------------------------------------
slot_frame = tk.Frame(root)
slot_frame.pack()
slot_labels = [tk.Label(slot_frame, image=IMAGES["apple"]) for _ in range(3)]
for lbl in slot_labels:
    lbl.pack(side="left", padx=10)

def animate_slots():
    """Анімація обертання слота"""
    for _ in range(10):
        for lbl in slot_labels:
            lbl.config(image=IMAGES[rnd.choice(DATA)])
        root.update()
        time.sleep(0.1)

def get_values():
    animate_slots()  # Анімація обертання

    max_units = 7
    values = [0, 1, 2, 3, 4, 5]

    while True:
        comp_values = {fruit: rnd.choice(values) for fruit in DATA}
        if sum(comp_values.values()) <= max_units:
            break

    counters = {fruit: 0 for fruit in DATA}
    variables = [entry_var, radio_var, spin_var, option_var]

    for var in variables:
        value = var.get()
        if value in counters:
            counters[value] += 1

    for fruit, check_var in check_vars.items():
        if check_var.get():
            counters[fruit] += 1

    match_count = sum(1 for fruit in DATA if counters[fruit] == comp_values[fruit])

    # *** Оновлення зображень слотів відповідно до числових значень комп'ютера ***
    sorted_fruits = sorted(comp_values.items(), key=lambda x: x[1], reverse=True)  # Сортуємо за спаданням значень
    final_fruits = [fruit for fruit, _ in sorted_fruits[:3]]  # Беремо 3 фрукти з найвищими значеннями

    for i in range(3):
        slot_labels[i].config(image=IMAGES[final_fruits[i]])

    # Відображення результату
    if match_count == 3:
        result_text = "🎉💎 🎰 МЕГА ВИГРАШ! Вгадав усе! 🎰💎 🎉"
        result_color = "purple"
    elif match_count == 2:
        result_text = "💎 Дуже близько! 2 фрукти вгадано!"
        result_color = "yellow"
    elif match_count == 1:
        result_text = "✅ Перемога! Вгадав хоча б один фрукт!"
        result_color = "green"
    else:
        result_text = "❌ Поразка! Спробуй ще раз."
        result_color = "red"

    label.config(text=f"{result_text}\n"
                      f"User -> Apple: {counters['apple']}, "
                      f"Banana: {counters['banana']}, "
                      f"Cherry: {counters['cherry']}\n"
                      f"Computer -> Apple: {comp_values['apple']}, "
                      f"Banana: {comp_values['banana']}, "
                      f"Cherry: {comp_values['cherry']}",
                 bg=result_color)

# Кнопка запуску
button = tk.Button(
    text="Крутим 🎰",
    command=get_values,
    font=("Arial", 14, "bold"),
    bg="blue",
    fg="white"
)
button.pack()

root.mainloop()
