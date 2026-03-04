import customtkinter as ctk


def handle_button_press():
    global root, entry, label
    text = entry.get()
    entry.delete(0, "end")
    label.configure(text=f"Привет, {text}!")

    entry._activate_placeholder()
    root.focus_set()


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Виджет Entry")
root.geometry("500x500")
my_font = ctk.CTkFont(size=20)

label = ctk.CTkLabel(master=root)
label.configure(
    text="Привет, Аноним!",
    font=my_font,
    text_color="white"
)

entry = ctk.CTkEntry(master=root)
entry.configure(
    placeholder_text="Введите своё имя",
    justify="center",
    font=my_font,
    width=250
)

button = ctk.CTkButton(master=root, text="Готово", font=my_font, command=handle_button_press)

label.pack(pady=50)
entry.pack(pady=50)
button.pack(pady=50)

root.mainloop()
