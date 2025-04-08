import tkinter as tk
import random as rnd

root = tk.Tk()
root.title("Опитувальник/Казіно")
root.geometry("650x650+350+0")

DATA = ["apple", "banana", "cherry"]

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

# Label ---------------------------------------------------------------
label = tk.Label(bg="white", font=("Arial", 14, "bold"), width=50, height=3)
label.pack()

def get_values():
    max_units = 7
    values = [0, 1, 2, 3, 4, 5]

    while True:
        comp_values = {
            "apple": rnd.choice(values),
            "banana": rnd.choice(values),
            "cherry": rnd.choice(values)
        }
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

# Кнопка
button = tk.Button(
    text="Крутим 🎰",
    command=get_values,
    font=("Arial", 14, "bold"),
    bg="blue",
    fg="white"
)
button.pack()

root.mainloop()