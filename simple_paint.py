import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk

root = tk.Tk(className=' Simple Paint')
root.geometry("1280x1000")

def open_file(event=None):
    file_path = filedialog.askopenfilename(initialdir='/', title='Open File', filetypes=[('PNG files', '*.png')])
    if file_path:
        canvas.delete('all')
        image = Image.open(file_path)
        canvas.image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=canvas.image, anchor='nw')

def save_to_png(event=None):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[('PNG files', '*.png')])
    if file_path:
        canvas.postscript(file='temp.eps')
        im = Image.open('temp.eps')
        fig = im.convert('RGBA')
        image_png= file_path
        fig.save(image_png, lossless = True)

def quit(event=None):
    root.quit()

def activate_pencil():
    canvas.bind('<B1-Motion>', draw_pencil)

def draw_pencil(event):
    x, y = event.x, event.y
    canvas.create_line(x, y, x+1, y+1, fill=color, width=pencil_size.get(), capstyle='round', smooth='true')

def deactivate_pencil(event):
    canvas.unbind('<B1-Motion>')

def activate_eraser():
    canvas.bind('<B1-Motion>', erase)

def erase(event):
    x, y = event.x, event.y
    canvas.create_rectangle(x-eraser_size.get(), y-eraser_size.get(), x+eraser_size.get(), y+eraser_size.get(), fill='white', outline='white')
    size = eraser_size.get()
    canvas.create_oval(x-size, y-size, x+size, y+size, fill='white', outline='white')

def deactivate_eraser(event):
    canvas.unbind('<B1-Motion>')

def set_color(new_color):
    global color
    color = new_color

def create_color_palette():
    colors = ['#000000', '#3F48CC', '#55D1D0', '#ffffff', '#B5E61D', '#FF7F27', '#FFAEC9', '#ED1C24', '#FFF200']
    for i, color in enumerate(colors):
        color_button = tk.Button(palette_frame, bg=color, width=2, command=lambda new_color=color: set_color(new_color))
        color_button.grid(row=i//3, column=i%3, padx=2, pady=2)

# Create a canvas
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill=tk.BOTH, expand=1)

# Create a tools frame
tools_frame = tk.Frame(root)
tools_frame.pack(side=tk.LEFT, padx=5, pady=5)

palette_frame = tk.Frame(tools_frame)
palette_frame.pack(side=tk.BOTTOM)

# Create a button
pencil_button = tk.Button(tools_frame, text='Pencil', command=activate_pencil)
pencil_button.pack(side=tk.TOP, pady=5)

eraser_button = tk.Button(tools_frame, text='Eraser', command=activate_eraser)
eraser_button.pack(side=tk.TOP, pady=5)

clear_button = tk.Button(tools_frame, text='Clear Canvas', command=lambda: canvas.delete('all'))
clear_button.pack(side=tk.TOP, pady=5)

# Create a size customize scale
pencil_size = tk.Scale(tools_frame, from_=9, to=50, orient=tk.HORIZONTAL, label='Pencil Size')
pencil_size.pack(side=tk.TOP, pady=5)

eraser_size = tk.Scale(tools_frame, from_=9, to=50, orient=tk.HORIZONTAL, label='Eraser Size')
eraser_size.pack(side=tk.TOP, pady=5)

create_color_palette()

# Default
color = 'black'

menu_bar = tk.Menu(root)

# Create a file menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open (Ctrl-o)', command=open_file)
file_menu.add_command(label='Save to png (Ctrl-s)', command=save_to_png)
file_menu.add_command(label='Quit (Ctrl-q)', command=quit)
menu_bar.add_cascade(label='File', menu=file_menu)
root.config(menu=menu_bar)

activate_pencil()
root.bind('<Control-o>', open_file)
root.bind('<Control-s>', save_to_png)
root.bind('<Control-q>', quit)
root.mainloop()
