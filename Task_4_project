import customtkinter as ctk
from yandex_music import Client
import threading
import requests
import os
import pygame
from mutagen.mp3 import MP3

#242424
class YandexMusicApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        my_font = ctk.CTkFont(size=15)

        self.title("Поиск музыки Яндекс.Музыка")
        self.geometry("950x520")

        self.music_folder = r"C:\Users\Py#1\PycharmProjects\pythonProject\music"
        os.makedirs(self.music_folder, exist_ok=True)

        self.client = Client("y0__xDwwOulBhje-AYg5PyN2xYwn7nz8Qe-0R7uTo3KMW4T-z3ixi8il2bgLg").init()
        self.search_results = []
        self.selected_song = None

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.downloaded_files = []
        self.current_track_index = -1
        self.current_track_length = 0
        self.is_paused = False
        self.user_dragging_slider = False

        pygame.mixer.init()

        rows, columns = 6, 4
        for i in range(rows):
            self.rowconfigure(index=i, weight=1)
        for i in range(columns):
            self.columnconfigure(index=i, weight=1, uniform="col")  # ← uniform!

        # Row 0
        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Введите название трека...",
            height=40,
            font=my_font
        )
        self.search_entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.search_entry.bind("<Return>", lambda e: self.search_music())

        self.search_button = ctk.CTkButton(
            self,
            text="Найти",
            command=self.search_music,
            font=my_font
        )
        self.search_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        # Row 1
        self.results_combobox = ctk.CTkComboBox(
            self,
            values=[],
            command=self.on_select,
            state="readonly",
            font=my_font
        )
        self.results_combobox.set("Результаты появятся здесь...")
        self.results_combobox.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # =============================================
        # TEXTBOX вместо LABEL — фиксированный размер
        # =============================================
        self.info_textbox = ctk.CTkTextbox(
            self,
            width=250,
            height=100,
            font=my_font,
            wrap="word",
            fg_color="transparent",  # фон как у окна
            border_width=0,  # без рамки
            corner_radius=0,
            activate_scrollbars=False  # скрыть скроллбар
        )
        self.info_textbox.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        self.info_textbox.configure(state="disabled")  # только для чтения

        self.info_textbox2 = ctk.CTkTextbox(
            self,
            width=250,
            height=100,
            font=my_font,
            wrap="word",
            activate_scrollbars=False,
            fg_color="transparent",  # фон как у окна
            border_width=0,  # без рамки
            corner_radius=0,
        )
        self.info_textbox2.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")
        self.info_textbox2.configure(state="disabled")

        # Row 2
        self.download_button = ctk.CTkButton(
            self,
            text="Скачать трек",
            command=self.download_track,
            state="disabled",
            font=my_font
        )
        self.download_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.progress = ctk.CTkProgressBar(self)
        self.progress.grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky="ew")
        self.progress.set(0)

        # Row 3
        self.downloaded_label = ctk.CTkLabel(
            self,
            text="Скачанные треки:",
            anchor="w",
            font=my_font
        )
        self.downloaded_label.grid(row=3, column=0, columnspan=4, padx=10, pady=(10, 0), sticky="ew")

        # Row 4
        self.downloaded_combobox = ctk.CTkComboBox(
            self,
            values=[],
            command=self.on_downloaded_select,
            state="readonly",
            font=my_font
        )
        self.downloaded_combobox.set("Нет скачанных треков")
        self.downloaded_combobox.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        # Row 5
        self.prev_button = ctk.CTkButton(self, text="⏮", command=self.play_previous)
        self.prev_button.grid(row=5, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.play_pause_button = ctk.CTkButton(self, text="⏯", command=self.toggle_pause)
        self.play_pause_button.grid(row=5, column=1, padx=10, pady=(10, 5), sticky="ew")

        self.next_button = ctk.CTkButton(self, text="⏭", command=self.play_next)
        self.next_button.grid(row=5, column=2, padx=10, pady=(10, 5), sticky="ew")

        self.time_label = ctk.CTkLabel(self, text="00:00 / 00:00")
        self.time_label.grid(row=5, column=3, padx=10, pady=(10, 5), sticky="ew")

        self.time_slider = ctk.CTkSlider(self, from_=0, to=100, command=self.seek_track)

        self.load_downloaded_tracks()
        self.after(500, self.update_playback_ui)

    # =============================================
    # Вспомогательный метод для записи текста в TextBox
    # =============================================
    def set_textbox_text(self, textbox, text):
        """Очищает textbox и вставляет новый текст (даже если он disabled)."""
        textbox.configure(state="normal")   # разрешаем редактирование
        textbox.delete("1.0", "end")        # очищаем
        textbox.insert("1.0", text)         # вставляем новый текст
        textbox.configure(state="disabled") # снова блокируем

    def format_time(self, seconds):
        seconds = max(0, int(seconds))
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    def is_valid_mp3(self, filepath):
        try:
            audio = MP3(filepath)
            return audio.info.length > 0
        except Exception:
            return False

    def search_music(self):
        query = self.search_entry.get().strip()
        if not query:
            self.set_textbox_text(self.info_textbox, "⚠️ Введите название трека")
            return

        self.search_button.configure(state="disabled", text="Ищу...")
        self.set_textbox_text(self.info_textbox, "🔍 Поиск...")
        self.progress.set(0.3)

        def search_thread():
            try:
                search_result = self.client.search(query, type_='track')

                if not search_result or not search_result.tracks or not search_result.tracks.results:
                    self.results_combobox.configure(values=["Ничего не найдено"])
                    self.set_textbox_text(self.info_textbox, "❌ Ничего не найдено")
                    return

                self.search_results = search_result.tracks.results[:20]

                display_values = []
                for track in self.search_results:
                    artists = ", ".join([a.name for a in track.artists])
                    display_values.append(f"{artists} - {track.title}")

                self.results_combobox.configure(values=display_values)
                self.results_combobox.set(display_values[0])
                self.on_select(display_values[0])
                self.download_button.configure(state="normal")
                self.progress.set(1)

            except Exception as e:
                self.set_textbox_text(self.info_textbox, f"❌ Ошибка поиска: {e}")
                self.progress.set(0)
            finally:
                self.search_button.configure(state="normal", text="Найти")

        threading.Thread(target=search_thread, daemon=True).start()

    def on_select(self, choice):
        try:
            index = self.results_combobox.cget("values").index(choice)
            self.selected_song = self.search_results[index]

            artists = ", ".join([a.name for a in self.selected_song.artists])
            duration_sec = self.selected_song.duration_ms // 1000 if self.selected_song.duration_ms else 0
            album = self.selected_song.albums[0].title if self.selected_song.albums else "Сингл"

            self.set_textbox_text(
                self.info_textbox,
                f"🎵 {self.selected_song.title}\n"
                f"👤 {artists}\n"
                f"💿 {album}\n"
                f"⏱️ {self.format_time(duration_sec)}"
            )
        except Exception as e:
            self.set_textbox_text(self.info_textbox, f"Ошибка выбора: {e}")

    def download_track(self):
        if not self.selected_song:
            self.set_textbox_text(self.info_textbox, "⚠️ Выберите трек")
            return

        self.download_button.configure(state="disabled", text="Скачиваю...")
        self.progress.set(0.1)

        def download_thread():
            try:
                artist = self.selected_song.artists[0].name
                title = self.selected_song.title
                filename = f"{artist} - {title}.mp3"
                filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.', '(', ')')).rstrip()
                filepath = os.path.join(self.music_folder, filename)

                if self.client.token:
                    self.selected_song.download(filepath)
                else:
                    track_id = str(self.selected_song.id)
                    preview_url = f"https://storage.yandexcloud.net/music-previews/{track_id[:2]}/{track_id}.mp3"

                    response = requests.get(preview_url, stream=True, timeout=30)
                    if response.status_code != 200:
                        raise Exception("Не удалось скачать файл")

                    total_size = int(response.headers.get('content-length', 0))
                    downloaded = 0

                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                if total_size:
                                    self.progress.set(downloaded / total_size)

                if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
                    raise Exception("Файл не был сохранён")

                if not self.is_valid_mp3(filepath):
                    os.remove(filepath)
                    raise Exception("Скачанный файл поврежден или не является MP3")

                self.set_textbox_text(self.info_textbox, "✅ Скачано")
                self.progress.set(1)
                self.load_downloaded_tracks()

            except Exception as e:
                self.set_textbox_text(self.info_textbox, f"❌ Ошибка скачивания: {e}")
                self.progress.set(0)
            finally:
                self.download_button.configure(state="normal", text="Скачать трек")

        threading.Thread(target=download_thread, daemon=True).start()

    def load_downloaded_tracks(self):
        files = []
        for f in os.listdir(self.music_folder):
            if f.lower().endswith(".mp3"):
                full_path = os.path.join(self.music_folder, f)
                if self.is_valid_mp3(full_path):
                    files.append(f)

        files.sort()
        self.downloaded_files = files

        if files:
            self.downloaded_combobox.configure(values=files)
            if self.current_track_index == -1:
                self.downloaded_combobox.set("Выбор трека")
            elif 0 <= self.current_track_index < len(files):
                self.downloaded_combobox.set(files[self.current_track_index])
        else:
            self.downloaded_combobox.configure(values=["Нет скачанных треков"])
            self.downloaded_combobox.set("Нет скачанных треков")
            self.current_track_index = -1

    def on_downloaded_select(self, choice):
        if choice == "Нет скачанных треков":
            return

        try:
            self.current_track_index = self.downloaded_files.index(choice)
            self.play_selected_track()
        except Exception as e:
            self.set_textbox_text(self.info_textbox, f"Ошибка выбора файла: {e}")

    def play_selected_track(self):
        if self.current_track_index < 0 or self.current_track_index >= len(self.downloaded_files):
            return

        filepath = os.path.join(self.music_folder, self.downloaded_files[self.current_track_index])

        if not self.is_valid_mp3(filepath):
            self.set_textbox_text(
                self.info_textbox,
                f"❌ Поврежденный файл:\n{self.downloaded_files[self.current_track_index]}"
            )
            return

        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            self.is_paused = False
            self.play_pause_button.configure(text="⏸")

            audio = MP3(filepath)
            self.current_track_length = int(audio.info.length)

            self.time_slider.configure(to=max(1, self.current_track_length))
            self.time_slider.set(0)
            self.time_label.configure(text=f"00:00 / {self.format_time(self.current_track_length)}")
            self.downloaded_combobox.set(self.downloaded_files[self.current_track_index])

            self.set_textbox_text(
                self.info_textbox2,
                f"▶ Сейчас играет:\n{self.downloaded_files[self.current_track_index]}"
            )

        except Exception as e:
            self.set_textbox_text(self.info_textbox2, f"Ошибка воспроизведения: {e}")

    def play_previous(self):
        if not self.downloaded_files:
            return

        if self.current_track_index == -1:
            self.current_track_index = 0
        else:
            self.current_track_index = (self.current_track_index - 1) % len(self.downloaded_files)

        self.play_selected_track()

    def play_next(self):
        if not self.downloaded_files:
            return

        if self.current_track_index == -1:
            self.current_track_index = 0
        else:
            self.current_track_index = (self.current_track_index + 1) % len(self.downloaded_files)

        self.play_selected_track()

    def toggle_pause(self):
        if self.current_track_index == -1:
            return

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.play_pause_button.configure(text="⏸")
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.is_paused = True
                self.play_pause_button.configure(text="▶")
            else:
                self.play_selected_track()

    def seek_track(self):
        if self.current_track_index == -1 or self.current_track_length == 0:
            return

        if self.user_dragging_slider:
            return

    def update_playback_ui(self):
        try:
            if self.current_track_index != -1 and self.current_track_length > 0:
                pos_ms = pygame.mixer.music.get_pos()

                if pos_ms >= 0 and not self.is_paused:
                    current_sec = pos_ms // 1000
                    if current_sec <= self.current_track_length:
                        self.time_slider.set(current_sec)
                        self.time_label.configure(
                            text=f"{self.format_time(current_sec)} / {self.format_time(self.current_track_length)}"
                        )

                if not pygame.mixer.music.get_busy() and not self.is_paused:
                    if self.current_track_index != -1 and self.downloaded_files:
                        current_pos = pygame.mixer.music.get_pos()
                        if current_pos == -1:
                            self.play_next()

        except Exception:
            pass

        self.after(500, self.update_playback_ui)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = YandexMusicApp()
    app.mainloop()
