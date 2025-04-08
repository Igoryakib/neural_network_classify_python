#root
import tkinter as tk
root = tk.Tk()
root.title("Кодовий замок")
root.geometry("450x450+350+0")
root.configure(bg="#1b1c1c")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

VALIDE_CODE="9971"
LIST_CODE=list(range(95, 106))

label_var = tk.StringVar()


#specialFunc
def changeColor():
    label.config(fg="#34ebe8")
    label_var.set("") 

def on_key(event):
    if event.keycode in LIST_CODE:
        label_var.set(label_var.get() + event.char)
    if event.keycode == 13:
        onClickVerify()
    if event.keycode == 8:
        onClickDel()

#onClickfn
def onClickNum(num):
    label_var.set(label_var.get() + str(num))

def onClickDel():
    label_var.set(label_var.get()[:-1])

def onClickVerify():
    if(VALIDE_CODE==label_var.get()):
        label.config(fg="green")
        label_var.set("Approved")
    else:
        label.config(fg="red")
        label_var.set("Disaprovved")
    label.after(1000, changeColor) 
    
#label
label = tk.Label(
    root,
    textvariable=label_var,
    bg="black",
    fg="#34ebe8",
    font=("Arial", 14, "normal"),
    width=20,
    height=10,
    anchor="center"
    )
label.grid(row=0, column=0, padx=10, pady=10)

#frame for btns
frame = tk.Frame(
    root,
    bg="black",
    )
frame.grid(column=1,row=0)

#buttons
for i in range(1, 10):
    button = tk.Button(
    frame,
    bg="#34ebe8",
    font=("Arial", 14, "normal"),
    text=str(i),
    width=4,
    height=2,
    command=lambda num=i: onClickNum(num),
    )
    button.grid(row=(i-1)//3, column=(i-1)%3,padx=1, pady=1)
    
button_0 = tk.Button(
    frame,
    text=0,
    bg="#34ebe8",
    fg="black",
    font=("Arial", 14, "normal"),
    width=4, height=2,
    command= lambda num=0 : onClickNum(num)
)
button_0.grid(row=3, column=1,padx=1, pady=1)

button_back = tk.Button(
    frame,
    text="Back",
    bg="#34ebe8",
    fg="black",
    font=("Arial", 14, "normal"),
    width=4, height=2,
    command=onClickDel
)
button_back.grid(row=3, column=0,padx=1, pady=1)


button_enter = tk.Button(
    frame,
    text="Enter",
    bg="#34ebe8",
    fg="black",
    font=("Arial", 14, "normal"),
    width=4, height=2,
    command=onClickVerify
)
button_enter.grid(row=3, column=2, padx=1, pady=1)
root.bind("<KeyPress>", on_key)
root.mainloop()
