import customtkinter as ctk


def handle_button_press():
    text = input("Новый текст: ")
    entry.configure(state="normal")  # разблокируем поле
    entry.delete(0, "end")  # удалим оттуда старую строчку
    entry.insert(0, text)  # вставим новую
    entry.configure(state="readonly")  # снова заблокируем


def handle_button_press_1(btn_number):
    for n in range(10):
        lst_btns_1[n].configure(fg_color=color_fg, hover_color="#0D4C13")
    lst_btns_1[btn_number].configure(fg_color="#F54927", hover_color="#B5351B")
    number = str(btn_number)
    entry.configure(state="normal")  # разблокируем поле
    old_code = entry.get()
    new_code = number + old_code[1::]
    entry.delete(0, "end")  # удалим оттуда старую строчку
    entry.insert(0, new_code)  # вставим новую
    entry.configure(state="readonly")  # снова заблокируем


def handle_button_press_2(btn_number):
    for n in range(10):
        lst_btns_2[n].configure(fg_color=color_fg, hover_color="#0D4C13")
    lst_btns_2[btn_number].configure(fg_color="#F54927", hover_color="#B5351B")
    number = str(btn_number)
    entry.configure(state="normal")  # разблокируем поле
    old_code = entry.get()
    new_code = old_code[0:1] + number + old_code[2:]
    entry.delete(0, "end")  # удалим оттуда старую строчку
    entry.insert(0, new_code)  # вставим новую
    entry.configure(state="readonly")  # снова заблокируем


def handle_button_press_3(btn_number):
    for n in range(10):
        lst_btns_3[n].configure(fg_color=color_fg, hover_color="#0D4C13")
    lst_btns_3[btn_number].configure(fg_color="#F54927", hover_color="#B5351B")
    number = str(btn_number)
    entry.configure(state="normal")  # разблокируем поле
    old_code = entry.get()
    new_code = old_code[0:2:] + number
    entry.delete(0, "end")  # удалим оттуда старую строчку
    entry.insert(0, new_code)  # вставим новую
    entry.configure(state="readonly")  # снова заблокируем


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Task_5")
root.geometry("800x600")
my_font = ctk.CTkFont(family="Roboto", size=25)

scrollable_frame_1 = ctk.CTkScrollableFrame(master=root)
scrollable_frame_2 = ctk.CTkScrollableFrame(master=root)
scrollable_frame_3 = ctk.CTkScrollableFrame(master=root)
scrollable_frame_1.configure(height=325)
scrollable_frame_2.configure(height=325)
scrollable_frame_3.configure(height=325)

rows, columns = 3, 3
for i in range(rows):
    root.rowconfigure(index=i, weight=1)
for i in range(columns):
    root.columnconfigure(index=i, weight=1)
scrollable_frame_1.grid(row=1, column=0)
scrollable_frame_2.grid(row=1, column=1)
scrollable_frame_3.grid(row=1, column=2)

color_fg = "#178021"

label = ctk.CTkLabel(master=root)
label.configure(
    text="Выберите код:",
    font=my_font,
    text_color="white"
)

entry = ctk.CTkEntry(master=root)
entry.configure(
    justify="center",
    font=my_font,
    width=250
)
entry.insert(0, "***")  # вставили в поле текст
entry.configure(state="readonly")

lst_handlers_1 = []
for i in range(10):
    handler_i_1 = lambda i_actual=i: handle_button_press_1(i_actual)
    lst_handlers_1.append(handler_i_1)

lst_handlers_2 = []
for i in range(10):
    handler_i_2 = lambda i_actual=i: handle_button_press_2(i_actual)
    lst_handlers_2.append(handler_i_2)

lst_handlers_3 = []
for i in range(10):
    handler_i_3 = lambda i_actual=i: handle_button_press_3(i_actual)
    lst_handlers_3.append(handler_i_3)

# кнопки внутри scrollable_frame:
lst_btns_1 = []
for i in range(10):
    btn_i = ctk.CTkButton(master=scrollable_frame_1)
    btn_i.configure(text=f"{i}", font=my_font, width=200, height=50, fg_color=color_fg, hover_color="#0D4C13")
    btn_i.configure(command=lst_handlers_1[i])
    lst_btns_1.append(btn_i)

lst_btns_2 = []
for i in range(10):
    btn_i = ctk.CTkButton(master=scrollable_frame_2)
    btn_i.configure(text=f"{i}", font=my_font, width=200, height=50, fg_color=color_fg, hover_color="#0D4C13")
    btn_i.configure(command=lst_handlers_2[i])
    lst_btns_2.append(btn_i)

lst_btns_3 = []
for i in range(10):
    btn_i = ctk.CTkButton(master=scrollable_frame_3)
    btn_i.configure(text=f"{i}", font=my_font, width=200, height=50, fg_color=color_fg, hover_color="#0D4C13")
    btn_i.configure(command=lst_handlers_3[i])
    lst_btns_3.append(btn_i)


label.grid(row=0, column=1, pady=40)
entry.grid(row=3, column=1, pady=40)
rows, columns = 10, 1
for i in range(rows):
    scrollable_frame_1.rowconfigure(index=i, weight=1)
for i in range(columns):
    scrollable_frame_1.columnconfigure(index=i, weight=1)
for i in range(rows):
    scrollable_frame_2.rowconfigure(index=i, weight=1)
for i in range(columns):
    scrollable_frame_2.columnconfigure(index=i, weight=1)
for i in range(rows):
    scrollable_frame_3.rowconfigure(index=i, weight=1)
for i in range(columns):
    scrollable_frame_3.columnconfigure(index=i, weight=1)
for i in range(10):
    btn_i = lst_btns_1[i]
    btn_i.grid(row=i, column=0, padx=20, pady=20)
for i in range(10):
    btn_i = lst_btns_2[i]
    btn_i.grid(row=i, column=0, padx=20, pady=20)
for i in range(10):
    btn_i = lst_btns_3[i]
    btn_i.grid(row=i, column=0, padx=20, pady=20)

root.mainloop()
