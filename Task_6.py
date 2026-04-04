import customtkinter as ctk
from PIL import Image


def handler(i, j):
    global counter, game_state
    if game_state[i][j] != 0 or game_state[i][j] != 0:
        return
    if counter % 2 == 0:
        matrix_lbls[i][j].configure(image=image_ctk_x)
        game_state[i][j] = 1
    else:
        matrix_lbls[i][j].configure(image=image_ctk_O)
        game_state[i][j] = -1
    counter += 1
    winner = check_winner(game_state)
    if winner == 1:
        label.configure(text="Последняя победа: \n победа X")
        handler_reset()
    elif winner == -1:
        label.configure(text="Последняя победа: \n победа 0")
        handler_reset()


def check_winner(state):
    for i in range(3):
        if abs(sum(state[i])) == 3:
            return state[i][0]
        if abs(state[0][i] + state[1][i] + state[2][i]) == 3:
            return state[0][i]
    if abs(state[0][0] + state[1][1] + state[2][2]) == 3:
        return state[0][0]
    if abs(state[0][2] + state[1][1] + state[2][0]) == 3:
        return state[0][2]
    return 0

def handler_reset():
    global counter, game_state
    counter = 0
    game_state = [[0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            matrix_lbls[i][j].configure(image=image_ctk_white)


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

rows, columns = 2, 3
for i in range(rows):
    root.rowconfigure(index=i, weight=1)
for i in range(columns):
    root.columnconfigure(index=i, weight=1)
frame.grid(row=0, column=1)

matrix_handlers = []
for i in range(3):
    tmp_lst = []
    for j in range(3):
        handler_ij = lambda x, i_actual=i, j_actual=j: handler(i_actual, j_actual)
        tmp_lst.append(handler_ij)
    matrix_handlers.append(tmp_lst)

game_state = [[0 for _ in range(3)] for _ in range(3)]

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

label = ctk.CTkLabel(master=root)
label.configure(
    text="Последняя победа: \n",
    font=my_font,
    text_color="white"
)

button.grid(row=1, column=1, pady=5)
label.grid(rows=1, columns=3)
root.mainloop()

)
button.configure(command=handler_reset)

button.grid(row=1, column=0, pady=5)
root.mainloop()
