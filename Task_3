import customtkinter as ctk


def handle_combobox_choice(chosen_elem):
    global text
    text = chosen_elem


def handle_button_press():
    global root, entry, text
    entry.delete(0, "end")
    color = var_radiobuttons.get()
    
    text = combobox.get()

    if color == 1:
        entry.configure(text_color="white")
    elif color == 2:
        entry.configure(text_color="red")
    elif color == 3:
        entry.configure(text_color="yellow")

    if var_checkbox_1.get():
        text = text + "!"
    if var_checkbox_2.get():
        text = text + "?"

    entry.insert(0, text)

    root.focus_set()


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Task_3")
root.geometry("500x500")
my_font = ctk.CTkFont(size=15)

text = ""

entry = ctk.CTkEntry(master=root)
entry.configure(
    justify="center",
    font=my_font,
    width=250
)


elems = ["Привет", "Hello", "Hi"]
combobox = ctk.CTkComboBox(master=root)
combobox.configure(
    font=my_font,
    values=elems,
    state="readonly"
)
combobox.set("Выберите фразу:")
combobox.configure(command=handle_combobox_choice)

combobox.get()

button = ctk.CTkButton(master=root, text="Готово", font=my_font, command=handle_button_press)

var_radiobuttons = ctk.IntVar()

radiobutton_1 = ctk.CTkRadioButton(
    master=root,
    variable=var_radiobuttons,
    value=1
)

radiobutton_1.configure(text="Белый цвет текста", font=my_font)

radiobutton_2 = ctk.CTkRadioButton(master=root, variable=var_radiobuttons, value=2)
radiobutton_2.configure(text="Красный цвет текста", font=my_font)

radiobutton_3 = ctk.CTkRadioButton(master=root, variable=var_radiobuttons, value=3)
radiobutton_3.configure(text="Желтый цвет текста", font=my_font)

var_radiobuttons.set(1)

var_radiobuttons.get()


var_checkbox_1 = ctk.BooleanVar()

checkbox_1 = ctk.CTkCheckBox(
    master=root,
    variable=var_checkbox_1,
    onvalue=True,
    offvalue=False
)
checkbox_1.configure(text="добавить в конец '!'", font=my_font)

var_checkbox_1.set(False)

var_checkbox_2 = ctk.BooleanVar()
checkbox_2 = ctk.CTkCheckBox(master=root, variable=var_checkbox_2, onvalue=True, offvalue=False)
checkbox_2.configure(text="добавить в конец'?'", font=my_font)
var_checkbox_2.set(False)

var_checkbox_1.get()
var_checkbox_2.get()



entry.pack(pady=25)
radiobutton_1.pack(pady=10)
radiobutton_2.pack(pady=10)
radiobutton_3.pack(pady=10)
combobox.pack(pady=25)
checkbox_1.pack(pady=10)
checkbox_2.pack(pady=10)
button.pack(pady=25)


root.mainloop()
