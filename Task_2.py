import customtkinter as ctk


def handle_button_press():
    global root, entry_1, entry_2, entry_frozen
    n1 = entry_1.get()
    n2 = entry_2.get()
    entry_1.delete(0, "end")
    entry_2.delete(0, "end")
    entry_frozen.configure(state="normal")
    entry_frozen.delete(0, "end")  # удалим оттуда старую строчку
    entry_frozen.configure(text=f"{n1 + n2}")
    entry_frozen.configure(state="readonly")

    entry_1._activate_placeholder()
    entry_2._activate_placeholder()
    root.focus_set()


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Виджет Entry")
root.geometry("500x500")
my_font = ctk.CTkFont(size=20)

entry_1 = ctk.CTkEntry(master=root)
entry_1.configure(
    placeholder_text="число №1",
    justify="center",
    font=my_font,
    width=250
)

entry_2 = ctk.CTkEntry(master=root)
entry_2.configure(
    placeholder_text="число №2",
    justify="center",
    font=my_font,
    width=250
)


answer = "ответ"

entry_frozen = ctk.CTkEntry(master=root)
entry_frozen.configure(
    placeholder_text="ответ",
    justify="center",
    font=my_font,
    width=250
)
entry_frozen.insert("0", f"{answer}")
entry_frozen.configure(state="readonly")

button = ctk.CTkButton(master=root, text="Готово", font=my_font, command=handle_button_press)

label_1 = ctk.CTkLabel(master=root)
label_1.configure(
    text="+",
    font=my_font,
    text_color="white"
)

label_2 = ctk.CTkLabel(master=root)
label_2.configure(
    text="=",
    font=my_font,
    text_color="white"
)

entry_1.pack(pady=50)
label_1.pack(pady=20)
entry_2.pack(pady=20)
label_2.pack(pady=20)
entry_frozen.pack(pady=20)
button.pack(pady=25)


root.mainloop()
