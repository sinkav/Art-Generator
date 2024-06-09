import tkinter as tk
from tkinter import colorchooser, filedialog
import random

class ArtGenerator:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw_rectangle(self, x1, y1, x2, y2, color):
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

    def draw_circle(self, x, y, r, color):
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline=color)

    def draw_triangle(self, x1, y1, x2, y2, x3, y3, color):
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline=color)

    def draw_polygon(self, points, color):
        self.canvas.create_polygon(points, fill=color, outline=color)
    
    def draw_ellipse(self, x1, y1, x2, y2, color):
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

    def draw_line(self, x1, y1, x2, y2, color):
        self.canvas.create_line(x1, y1, x2, y2, fill=color)

    def generate_art(self, num_shapes, shape_types, colors):
        self.canvas.delete("all")
        for _ in range(num_shapes):
            shape_type = random.choice(shape_types)
            color = random.choice(colors)
            if shape_type == "rectangle":
                x1 = random.randint(0, 400)
                y1 = random.randint(0, 400)
                x2 = x1 + random.randint(20, 100)
                y2 = y1 + random.randint(20, 100)
                self.draw_rectangle(x1, y1, x2, y2, color)
            elif shape_type == "circle":
                x = random.randint(0, 400)
                y = random.randint(0, 400)
                r = random.randint(10, 50)
                self.draw_circle(x, y, r, color)
            elif shape_type == "triangle":
                x1 = random.randint(0, 400)
                y1 = random.randint(0, 400)
                x2 = x1 + random.randint(20, 100)
                y2 = y1
                x3 = x1 + (x2 - x1) // 2
                y3 = y1 - random.randint(20, 100)
                self.draw_triangle(x1, y1, x2, y2, x3, y3, color)
            elif shape_type == "polygon":
                points = [(random.randint(0, 400), random.randint(0, 400)) for _ in range(random.randint(3, 6))]
                self.draw_polygon(points, color)
            elif shape_type == "ellipse":
                x1 = random.randint(0, 400)
                y1 = random.randint(0, 400)
                x2 = x1 + random.randint(20, 100)
                y2 = y1 + random.randint(20, 100)
                self.draw_ellipse(x1, y1, x2, y2, color)
            elif shape_type == "line":
                x1 = random.randint(0, 400)
                y1 = random.randint(0, 400)
                x2 = random.randint(0, 400)
                y2 = random.randint(0, 400)
                self.draw_line(x1, y1, x2, y2, color)

def on_generate(num_shapes_entry, color_vars, shape_type_vars, art_gen):
    num_shapes = int(num_shapes_entry.get())
    selected_colors = [color for color, var in color_vars.items() if var.get()]
    shape_types = [shape for shape, var in shape_type_vars.items() if var.get()]
    art_gen.generate_art(num_shapes, shape_types, selected_colors)

def on_color_pick(color_vars, colors_frame):
    color_code = colorchooser.askcolor(title="Choose color")[1]
    if color_code:
        color_vars[color_code] = tk.BooleanVar(value=True)
        color_check = tk.Checkbutton(colors_frame, text=color_code, variable=color_vars[color_code], bg=color_code)
        color_check.pack(side=tk.LEFT, padx=5, pady=5)

def save_art(canvas):
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        canvas.postscript(file=file_path + '.eps')
        import os
        os.system(f"convert {file_path + '.eps'} {file_path}")

def load_settings(file_path, num_shapes_entry, color_vars, color_checks, shape_type_vars, shape_checks):
    with open(file_path, "r") as file:
        settings = file.read().split("\n")
        num_shapes_entry.delete(0, tk.END)
        num_shapes_entry.insert(0, settings[0])
        for color_check in color_checks:
            color_check.deselect()
        for color in settings[1].split(","):
            if color in color_vars:
                color_vars[color].set(True)
        for shape_check in shape_checks:
            shape_check.deselect()
        for shape in settings[2].split(","):
            if shape in shape_type_vars:
                shape_type_vars[shape].set(True)

def save_settings(file_path, num_shapes, color_vars, shape_type_vars):
    selected_colors = ",".join([color for color, var in color_vars.items() if var.get()])
    selected_shapes = ",".join([shape for shape, var in shape_type_vars.items() if var.get()])
    with open(file_path, "w") as file:
        file.write(f"{num_shapes}\n{selected_colors}\n{selected_shapes}")

def create_gui():
    root = tk.Tk()
    root.title("Art Generator")

    canvas = tk.Canvas(root, width=500, height=500, bg="white")
    canvas.pack()

    controls_frame = tk.Frame(root)
    controls_frame.pack()

    num_shapes_label = tk.Label(controls_frame, text="Number of Shapes:")
    num_shapes_label.grid(row=0, column=0)
    num_shapes_entry = tk.Entry(controls_frame)
    num_shapes_entry.grid(row=0, column=1)

    color_button = tk.Button(controls_frame, text="Pick Color", command=lambda: on_color_pick(color_vars, colors_frame))
    color_button.grid(row=1, column=0, columnspan=2)

    colors_frame = tk.Frame(controls_frame)
    colors_frame.grid(row=2, column=0, columnspan=2)

    shape_types = ["rectangle", "circle", "triangle", "polygon", "ellipse", "line"]
    shape_type_vars = {shape: tk.BooleanVar(value=True) for shape in shape_types}
    shape_checks = []
    color_vars = {}
    color_checks = []

    for i, shape in enumerate(shape_types):
        chk = tk.Checkbutton(controls_frame, text=shape, variable=shape_type_vars[shape])
        chk.grid(row=3+i, column=0, columnspan=2)
        shape_checks.append(chk)

    generate_button = tk.Button(root, text="Generate Art", command=lambda: on_generate(num_shapes_entry, color_vars, shape_type_vars, art_gen))
    generate_button.pack()

    save_button = tk.Button(root, text="Save Art", command=lambda: save_art(canvas))
    save_button.pack()

    save_settings_button = tk.Button(root, text="Save Settings", command=lambda: save_settings(filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")]), num_shapes_entry.get(), color_vars, shape_type_vars))
    save_settings_button.pack()

    load_settings_button = tk.Button(root, text="Load Settings", command=lambda: load_settings(filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")]), num_shapes_entry, color_vars, color_checks, shape_type_vars, shape_checks))
    load_settings_button.pack()

    art_gen = ArtGenerator(canvas)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
