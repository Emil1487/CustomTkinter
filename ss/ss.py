import customtkinter as ctk
from yandex_music import Client
import threading
import requests
import os
from pathlib import Path

root = ctk.CTk()
root.title("Task_3")
root.geometry("600x450")
my_font = ctk.CTkFont(size=15)

rows, columns = 3, 4
for i in range(rows):
    root.rowconfigure(index=i, weight=1)
for i in range(columns):
    root.columnconfigure(index=i, weight=1)


class YandexMusicApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Путь к папке "Музыка"
        self.music_folder = r'C:\Users\Py#1\PycharmProjects\pythonProject\music'  # Windows: C:\Users\ИМЯ\Music
        # Если нужна другая папка:
        # self.music_folder = "D:\\Музыка"  # или любой путь

        # Создаём папку, если её нет
        os.makedirs(self.music_folder, exist_ok=True)

        # Инициализация БЕЗ токена (публичный поиск)
        # self.client = Client()
        # Или с токеном для скачивания:
        self.client = Client("y0__xDwwOulBhje-AYg5PyN2xYwn7nz8Qe-0R7uTo3KMW4T-z3ixi8il2bgLg").init()

        self.search_results = []
        self.selected_song = None

        # Показываем путь сохранения
        self.folder_label = ctk.CTkLabel(
            self,
            text=f"📁 Папка для сохранения: {self.music_folder}",
            font=("Arial", 10),
            text_color="gray"
        )
        self.folder_label.grid(row=0, column=0, columnspan=3)

        # UI
        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Введите название трека...",
            width=400,
            height=40
        )
        self.search_entry.grid(raw=1, columns=0)
        self.search_entry.bind("<Return>", lambda e: self.search_music())

        self.search_button = ctk.CTkButton(
            self,
            text="Найти",
            command=self.search_music,
            width=150
        )
        self.search_button.grid(raw=2, columns=0)

        self.results_combobox = ctk.CTkComboBox(
            self,
            values=[],
            width=500,
            height=40,
            command=self.on_select,
            state="readonly"
        )
        self.results_combobox.set("Результаты появятся здесь...")
        self.results_combobox.grid(raw=1, columns=1, rowspan=2, columnspan=2)

        self.info_label = ctk.CTkLabel(
            self,
            text="",
            wraplength=500,
            justify="left"
        )
        self.info_label.pack(pady=10, padx=20)

        self.download_button = ctk.CTkButton(
            self,
            text="Скачать трек",
            command=self.download_track,
            state="disabled",
            width=200
        )
        self.download_button.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self, width=500)
        self.progress.pack(pady=10, padx=20)
        self.progress.set(0)

    def search_music(self):
        """Поиск треков"""
        query = self.search_entry.get().strip()

        if not query:
            self.info_label.configure(text="⚠️ Введите название трека!")
            return

        self.search_button.configure(state="disabled", text="Ищу...")
        self.info_label.configure(text="🔍 Поиск...")
        self.progress.set(0.5)

        def search_thread():
            try:
                # Поиск через Яндекс.Музыку
                search_result = self.client.search(query, type_='track')

                if not search_result.tracks:
                    self.info_label.configure(text="❌ Ничего не найдено")
                    self.results_combobox.configure(values=["Ничего не найдено"])
                    return

                self.search_results = search_result.tracks.results[:20]

                # Формируем список
                display_values = []
                for track in self.search_results:
                    artists = ", ".join([artist.name for artist in track.artists])
                    display_values.append(
                        f"{artists} - {track.title} ({track.albums[0].title if track.albums else 'Сингл'})"
                    )

                self.results_combobox.configure(values=display_values)
                self.results_combobox.set(display_values[0])

                self.info_label.configure(
                    text=f"✅ Найдено {len(self.search_results)} треков"
                )
                self.download_button.configure(state="normal")

            except Exception as e:
                self.info_label.configure(text=f"❌ Ошибка: {str(e)}")

            finally:
                self.search_button.configure(state="normal", text="Найти")
                self.progress.set(0)

        thread = threading.Thread(target=search_thread, daemon=True)
        thread.start()

    def on_select(self, choice):
        """Выбор трека"""
        try:
            index = self.results_combobox.cget("values").index(choice)
            self.selected_song = self.search_results[index]

            artists = ", ".join([artist.name for artist in self.selected_song.artists])
            duration_sec = self.selected_song.duration_ms // 1000

            info_text = f"""
🎵 Трек: {self.selected_song.title}
👤 Исполнитель: {artists}
💿 Альбом: {self.selected_song.albums[0].title if self.selected_song.albums else 'Сингл'}
⏱️ Длительность: {duration_sec // 60}:{duration_sec % 60:02d}
📅 Год: {self.selected_song.albums[0].year if self.selected_song.albums else 'Неизвестно'}
            """
            self.info_label.configure(text=info_text.strip())

        except Exception as e:
            self.info_label.configure(text=f"Ошибка: {e}")

    def download_track(self):
        """Скачивание трека в папку Музыка"""
        if not self.selected_song:
            self.info_label.configure(text="⚠️ Выберите трек!")
            return

        self.download_button.configure(state="disabled", text="Скачиваю...")
        self.progress.set(0.3)

        def download_thread():
            try:
                # Имя файла
                artist = self.selected_song.artists[0].name
                title = self.selected_song.title
                filename = f"{artist} - {title}.mp3"
                filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()

                # Полный путь
                filepath = os.path.join(self.music_folder, filename)

                # Пытаемся скачать полный трек (если есть токен)
                if self.client.token:
                    self.selected_song.download(filepath)
                    self.info_label.configure(
                        text=f"✅ Скачан полный трек: {filename}\n📂 В папку: {self.music_folder}"
                    )
                else:
                    # Скачиваем превью (30 сек) если нет токена
                    preview_url = f"https://storage.yandexcloud.net/music-previews/{self.selected_song.id[:2]}/{self.selected_song.id}.mp3"

                    response = requests.get(preview_url, stream=True, timeout=30)
                    total_size = int(response.headers.get('content-length', 0))

                    with open(filepath, 'wb') as f:
                        downloaded = 0
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                if total_size:
                                    self.progress.set(downloaded / total_size)

                    self.info_label.configure(
                        text=f"✅ Скачано (превью 30 сек): {filename}\n📂 В папку: {self.music_folder}"
                    )

                self.progress.set(1.0)

            except Exception as e:
                self.info_label.configure(text=f"❌ Ошибка: {e}")
                self.progress.set(0)

            finally:
                self.download_button.configure(state="normal", text="Скачать трек")

        threading.Thread(target=download_thread, daemon=True).start()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = YandexMusicApp()
    app.mainloop()
