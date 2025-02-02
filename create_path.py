import tkinter as tk
from tkinter import filedialog


def pixel_to_logical(x_pixel, y_pixel):
    x = (x_pixel - 300) / 300
    y = (300 - y_pixel) / 300
    return (x, y)


def start_draw(event):
    global drawing, points
    drawing = True
    canvas.delete("all")
    points = [(event.x, event.y)]


def draw(event):
    global drawing, points
    if drawing:
        x, y = event.x, event.y
        points.append((x, y))
        if len(points) >= 2:
            last_x, last_y = points[-2]
            canvas.create_line(last_x, last_y, x, y, fill='black')


def end_draw(event):
    """鼠标释放事件处理"""
    global drawing
    drawing = False


def save_points():
    global points
    if not points:
        return
    points.append(points[0])

    filepath = filedialog.asksaveasfilename(defaultextension="",
                                            filetypes=[("All files", "*.*")])

    if not filepath:
        return

    with open(filepath, 'w') as f:
        for x_pixel, y_pixel in points:
            x, y = pixel_to_logical(x_pixel, y_pixel)
            f.write(f"{x:.4f} {y:.4f}\n")


root = tk.Tk()
root.title("Create a Path")

canvas = tk.Canvas(root, width=600, height=600, bg='white')
canvas.pack()

drawing = False
points = []

canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", end_draw)

save_btn = tk.Button(root, text="save", command=save_points)
save_btn.pack(pady=10)

root.mainloop()
