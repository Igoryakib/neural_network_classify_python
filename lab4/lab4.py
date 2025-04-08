import tkinter as tk
from tkinter import ttk
import math
import numpy as np
import os
import csv
from classify import predict
import joblib

scaler = joblib.load("scaler.pkl")

root = tk.Tk()
root.title("Shape classify")
root.geometry("670x750+350+0")

# Variables
dash_var = tk.StringVar()
x1_var = tk.IntVar()
y1_var = tk.IntVar()
x2_var = tk.IntVar()
y2_var = tk.IntVar()
width_var = tk.IntVar()
fill_var = tk.StringVar(value="black")
outline_var = tk.StringVar(value="black")  
shape_type_var = tk.StringVar(value="line")
# label_var = tk.StringVar(value="triangle")  

frame = tk.Frame(root)
frame.pack()

# Coordinate Inputs
for label_text, var in [("x1", x1_var), ("y1", y1_var), ("x2", x2_var), ("y2", y2_var)]:
    frame_coord = tk.LabelFrame(frame, text=label_text, bd=1, relief="solid")
    frame_coord.pack()
    spin = tk.Spinbox(frame_coord, textvariable=var, from_=0, to=500, width=5)
    spin.pack(fill="x", padx=2, pady=2)

# Width Input
frame_width = tk.LabelFrame(frame, text="Width:", bd=1, relief="solid")
frame_width.pack()
scale_width = tk.Scale(frame_width, variable=width_var, from_=1, to=9, resolution=1,
                        tickinterval=2, orient="horizontal", length=100, sliderlength=16)
scale_width.pack()

# Dash Style
frame_dash = tk.LabelFrame(frame, text="Dash:", bd=1, relief="solid")
frame_dash.pack()
combo_dash = ttk.Combobox(frame_dash, textvariable=dash_var, height=5,
                        values=("solid", "dashed", "dashdotted", "dotted"), width=10)
combo_dash.pack()

# Outline Color for Oval
frame_outline = tk.LabelFrame(frame, text="Outline Color:", bd=1, relief="solid")
frame_outline.pack()
combo_outline = ttk.Combobox(frame_outline, textvariable=outline_var,
                              values=("black", "red", "green", "blue", "yellow"), width=10)
combo_outline.pack()

# Shape Selection (Line or Oval)
frame_shape = tk.LabelFrame(frame, text="Shape Type:", bd=1, relief="solid")
frame_shape.pack()
combo_shape = ttk.Combobox(frame_shape, textvariable=shape_type_var,
                            values=("line", "oval"), width=10)
combo_shape.pack()

dashes = {"solid": None, "dashed": (20, 20), "dashdotted": (20, 5, 5, 5), "dotted": (5, 5)}
current_shape_lines = []
shapes_dataset = []

# Canvas
frame_canvas = tk.LabelFrame(root, text="Canvas area", bd=1, relief="solid")
frame_canvas.pack(fill="both", expand=True)
canvas = tk.Canvas(frame_canvas, bg="white", width=500, height=500)
canvas.pack(fill="both", expand=True)


# Drawing functions for Line and Oval
def handle_draw():
    x1, y1, x2, y2 = x1_var.get(), y1_var.get(), x2_var.get(), y2_var.get()
    shape_type = shape_type_var.get()

    if shape_type == "line":
        canvas.create_line(x1, y1, x2, y2,
                           width=width_var.get(), fill=fill_var.get(),
                           dash=dashes.get(dash_var.get()))
        current_shape_lines.append((x1, y1, x2, y2))
    elif shape_type == "oval":
        canvas.create_oval(x1, y1, x2, y2,
                           outline=outline_var.get(), width=width_var.get(),
                           fill=fill_var.get(), dash=dashes.get(dash_var.get()))
        current_shape_lines.append((x1, y1, x2, y2))


def clear_canvas():
    canvas.delete("all")
    current_shape_lines.clear()
    shapes_dataset.clear()

def end_shape():
    if not current_shape_lines:
        return

    def shape_to_features(lines):
        lengths = [math.hypot(x2 - x1, y2 - y1) for x1, y1, x2, y2 in lines]
        avg_length = sum(lengths) / len(lengths)
        perimeter = sum(lengths)
        return [len(lines), avg_length, perimeter, max(lengths)]

    features = shape_to_features(current_shape_lines)
    x = np.array([features])
    x_scaled = scaler.transform(x)
    probs = predict(x_scaled)
    pred_class = np.argmax(probs)
    class_names = ['triangle', 'square', 'rectangle']
    label = class_names[pred_class]
    shapes_dataset.append({
        "label": label,
        "lines": current_shape_lines.copy()
    })

    current_shape_lines.clear()
    prediction_result.set(f"You painted: {label}")
    
# def save_dataset():
#     def shape_to_features(lines):
#         lengths = [math.hypot(x2 - x1, y2 - y1) for x1, y1, x2, y2 in lines]
#         avg_length = sum(lengths) / len(lengths)
#         perimeter = sum(lengths)
#         return [len(lines), avg_length, perimeter, max(lengths)]

#     file_exists = os.path.isfile("shapes_dataset.csv")

#     with open("shapes_dataset.csv", "a", newline="") as f:
#         writer = csv.writer(f)
#         if not file_exists:
#             writer.writerow(["num_lines", "avg_length", "perimeter", "max_length", "label"])
#         for shape in shapes_dataset:
#             features = shape_to_features(shape["lines"])
#             writer.writerow(features + [shape["label"]])

# Prediction Result
prediction_result = tk.StringVar()
prediction_result.set("Painted figure: ...")
result_label = tk.Label(frame, textvariable=prediction_result, fg="blue", font=("Arial", 12, "bold"))
result_label.pack(pady=4)

# Mouse drawing
start_x, start_y = None, None

def start_draw(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def stop_draw(event):
    global start_x, start_y
    shape_type = shape_type_var.get()

    if shape_type == "line":
        canvas.create_line(start_x, start_y, event.x, event.y,
                           width=width_var.get(), fill=fill_var.get(),
                           dash=dashes.get(dash_var.get()))
        current_shape_lines.append((start_x, start_y, event.x, event.y))
    elif shape_type == "oval":
        canvas.create_oval(start_x, start_y, event.x, event.y,
                           outline=outline_var.get(), width=width_var.get(),
                           fill=fill_var.get(), dash=dashes.get(dash_var.get()))
        current_shape_lines.append((start_x, start_y, event.x, event.y))


canvas.bind("<ButtonPress-1>", start_draw)
canvas.bind("<ButtonRelease-1>", stop_draw)

# Buttons
button_draw = tk.Button(frame, text="Draw Shape", bg="orange", command=handle_draw)
button_draw.pack()

button_end = tk.Button(frame, text="End Shape", bg="lightblue", command=end_shape)
button_end.pack(fill="x", padx=2, pady=2)

button_clear = tk.Button(frame, text="Clear Canvas", command=clear_canvas)
button_clear.pack(fill="x", padx=2, pady=2)

# button_save = tk.Button(frame, text="Save Dataset", command=save_dataset)
# button_save.pack(fill="x", padx=2, pady=2)

# Defaults
x1_var.set(0)
y1_var.set(0)
x2_var.set(100)
y2_var.set(100)
width_var.set(1)
dash_var.set("solid")

root.mainloop()
