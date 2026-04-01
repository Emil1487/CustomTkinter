import customtkinter as ctk
from PIL import Image


def handler(i, j):
    global counter, matrix_lbls
    if counter % 2 != 1:
        lbl_ij = matrix_lbls[i][j]
        lbl_ij.configure(image=image_ctk_x)
    else:
        lbl_ij = matrix_lbls[i][j]
        lbl_ij.configure(image=image_ctk_O)
    counter += 1
    x = 0
    for i in range(3):
        for j in range(3):
            lbl_ij = matrix_lbls[i][j]
            if lbl_ij.image == image_ctk_x:
                x += 1
            elif lbl_ij.image == image_ctk_O:
                x -= 1
        if x == 3:
            print("X win")
        if x == -3:
            print("O win")

def handler_reset():
    global counter, matrix_lbls
    counter = 0
    for i in range(3):
        for j in range(3):
            lbl_ij = matrix_lbls[i][j]
            lbl_ij.configure(image=image_ctk_white)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Task_6")
root.geometry("500x600")
my_font = ctk.CTkFont(family="Roboto", size=20)

image_x = Image.open("images/image_x.png")
image_ctk_x = ctk.CTkImage(dark_image=image_x, size=(120, 120))
image_O = Image.open("images/image_O.png")
image_ctk_O = ctk.CTkImage(dark_image=image_O, size=(120, 120))
image_white = Image.open("images/image_white.png")
image_ctk_white = ctk.CTkImage(dark_image=image_white, size=(120, 120))

frame = ctk.CTkFrame(master=root)

counter = 0

rows, columns = 2, 1
for i in range(rows):
    root.rowconfigure(index=i, weight=1)
for i in range(columns):
    root.columnconfigure(index=i, weight=1)
frame.grid(row=0, column=0)

# внутри рамки frame будет плитка из labels 2x3:

# создание хендлеров для labels:
matrix_handlers = []
for i in range(3):
    tmp_lst = []
    for j in range(3):
        handler_ij = lambda x, i_actual=i, j_actual=j: handler(i_actual, j_actual)
        tmp_lst.append(handler_ij)
    matrix_handlers.append(tmp_lst)

# создание виджетов labels и привязка к ним изображений и хендлеров:
matrix_lbls = []
for i in range(3):
    tmp_lst = []
    for j in range(3):
        lbl_ij = ctk.CTkLabel(master=frame, text="", image=image_ctk_white)
        lbl_ij.bind("<Button-1>", matrix_handlers[i][j])
        lbl_ij.configure(cursor="hand2")
        tmp_lst.append(lbl_ij)
    matrix_lbls.append(tmp_lst)

# внутренняя сетка для рамки frame:
rows, columns = 3, 3
for i in range(rows):
    frame.rowconfigure(index=i, weight=1)
for i in range(columns):
    frame.columnconfigure(index=i, weight=1)
for i in range(3):
    for j in range(3):
        lbl_ij = matrix_lbls[i][j]
        lbl_ij.grid(row=i, column=j, padx=5, pady=5)  # сделаем небольшие отступы между картинками

button = ctk.CTkButton(master=root)
button.configure(
    text="reset",
    font=my_font,
    text_color="white",
    fg_color="#f19c28",
    hover_color="#b27420"
)
button.configure(command=handler_reset)

button.grid(row=1, column=0, pady=5)
root.mainloop()
