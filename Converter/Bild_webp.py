import os
import sys
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Prüfen, ob PIL (Pillow) installiert ist
try:
    from PIL import Image

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class WebPConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("WebP Konverter")
        self.root.geometry("700x550")

        # Standardwerte
        self.jpg_quality = tk.IntVar(value=90)
        self.png_quality = tk.IntVar(value=95)
        self.use_lossless_for_png = tk.BooleanVar(value=True)
        self.selected_files = []
        self.output_dir = None
        self.conversion_stats = []

        # Wenn PIL nicht verfügbar ist, zeige Installationshinweis
        if not PIL_AVAILABLE:
            self._show_pil_missing()
            return

        self._create_widgets()

    def _show_pil_missing(self):
        """Zeigt Hinweis an, wenn PIL nicht installiert ist"""
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame,
            text="Pillow (PIL) ist nicht installiert!",
            font=("", 14, "bold")
        ).pack(pady=10)

        message = (
            "Dieses Programm benötigt die Pillow-Bibliothek zum Konvertieren von Bildern.\n\n"
            "Bitte installiere Pillow mit dem folgenden Befehl:\n"
            "pip install Pillow\n\n"
            "Nach der Installation starte das Programm neu."
        )

        ttk.Label(
            frame,
            text=message,
            wraplength=500,
            justify="center"
        ).pack(pady=20)

        ttk.Button(
            frame,
            text="Programm beenden",
            command=self.root.destroy
        ).pack(pady=10)

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Oberer Bereich - Datei/Ordner-Auswahl
        file_frame = ttk.LabelFrame(main_frame, text="Bildauswahl", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 15))

        # Buttons zur Dateiauswahl
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            btn_frame,
            text="Bilder auswählen",
            command=self.select_files
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Ordner auswählen",
            command=self.select_folder
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Ausgabeordner festlegen",
            command=self.set_output_dir
        ).pack(side=tk.LEFT, padx=5)

        # Ausgewählte Dateien anzeigen
        self.file_info_label = ttk.Label(file_frame, text="Keine Dateien ausgewählt")
        self.file_info_label.pack(fill=tk.X, pady=5)

        self.output_dir_label = ttk.Label(file_frame, text="Ausgabeordner: Standard")
        self.output_dir_label.pack(fill=tk.X, pady=5)

        # Mittlerer Bereich - Konversionsoptionen
        options_frame = ttk.LabelFrame(main_frame, text="Konversionsoptionen", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 15))

        # JPG-Qualität
        ttk.Label(
            options_frame,
            text="JPG-zu-WebP Qualität:"
        ).grid(row=0, column=0, sticky=tk.W, pady=5)

        ttk.Scale(
            options_frame,
            from_=60,
            to=100,
            variable=self.jpg_quality,
            orient=tk.HORIZONTAL,
            length=300
        ).grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(
            options_frame,
            textvariable=self.jpg_quality
        ).grid(row=0, column=2, padx=5)

        # PNG-Qualität
        ttk.Label(
            options_frame,
            text="PNG-zu-WebP Qualität:"
        ).grid(row=1, column=0, sticky=tk.W, pady=5)

        ttk.Scale(
            options_frame,
            from_=75,
            to=100,
            variable=self.png_quality,
            orient=tk.HORIZONTAL,
            length=300
        ).grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Label(
            options_frame,
            textvariable=self.png_quality
        ).grid(row=1, column=2, padx=5)

        # Verlustfreie Kompression für PNG
        ttk.Checkbutton(
            options_frame,
            text="Verlustfreie Kompression für PNG (empfohlen)",
            variable=self.use_lossless_for_png
        ).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=5)

        # Info-Text
        info_text = (
            "Empfohlene Einstellungen für minimalen Qualitätsverlust:\n"
            "• JPG: 85-95 (höher = bessere Qualität, größere Dateien)\n"
            "• PNG: Verlustfreie Kompression aktiviert oder Qualität 90-100"
        )

        ttk.Label(
            options_frame,
            text=info_text,
            wraplength=600,
            justify=tk.LEFT
        ).grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=10)

        # Konvertierungsbutton
        self.convert_btn = ttk.Button(
            main_frame,
            text="Konvertieren starten",
            command=self.start_conversion
        )
        self.convert_btn.pack(pady=10)

        # Fortschrittsanzeige
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress.pack(fill=tk.X, pady=5)

        # Status-Label
        self.status_label = ttk.Label(main_frame, text="Bereit")
        self.status_label.pack(pady=5)

        # Ergebnisbereich
        result_frame = ttk.LabelFrame(main_frame, text="Konvertierungsergebnisse")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Scrollbare Textbox für Ergebnisse
        self.result_text = tk.Text(result_frame, height=10, wrap=tk.WORD)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(result_frame, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)

    def select_files(self):
        filetypes = [
            ("Bilddateien", "*.jpg *.jpeg *.png"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("Alle Dateien", "*.*")
        ]

        files = filedialog.askopenfilenames(
            title="Bilder zum Konvertieren auswählen",
            filetypes=filetypes
        )

        if files:
            self.selected_files = list(files)
            if len(self.selected_files) > 1:
                self.file_info_label.config(text=f"{len(self.selected_files)} Bilder ausgewählt")
            else:
                self.file_info_label.config(
                    text=f"1 Bild ausgewählt: {os.path.basename(self.selected_files[0])}"
                )

    def select_folder(self):
        folder = filedialog.askdirectory(title="Ordner mit Bildern auswählen")
        if folder:
            # Dateien im Ordner und Unterordnern suchen
            image_files = []
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        image_files.append(os.path.join(root, file))

            self.selected_files = image_files

            if self.selected_files:
                self.file_info_label.config(text=f"{len(self.selected_files)} Bilder in Ordner gefunden")
            else:
                self.file_info_label.config(text="Keine Bilder im ausgewählten Ordner gefunden")

    def set_output_dir(self):
        folder = filedialog.askdirectory(title="Ausgabeordner auswählen")
        if folder:
            self.output_dir = folder
            self.output_dir_label.config(text=f"Ausgabeordner: {folder}")

    def start_conversion(self):
        if not self.selected_files:
            messagebox.showwarning("Keine Dateien", "Bitte wähle zuerst Bilder aus.")
            return

        # Wenn kein Ausgabeordner festgelegt, automatisch einen im Ordner der ersten Datei erstellen
        if not self.output_dir:
            first_file_dir = os.path.dirname(self.selected_files[0])
            self.output_dir = os.path.join(first_file_dir, "webp_konvertiert")
            self.output_dir_label.config(text=f"Ausgabeordner: {self.output_dir}")

        # Ausgabeordner erstellen, wenn er nicht existiert
        os.makedirs(self.output_dir, exist_ok=True)

        # UI zurücksetzen
        self.result_text.delete(1.0, tk.END)
        self.conversion_stats = []
        self.progress_var.set(0)

        # Konvertierung starten
        self.convert_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Konvertierung läuft...")

        total_files = len(self.selected_files)
        processed = 0
        failed = 0

        start_time = time.time()

        for idx, file_path in enumerate(self.selected_files):
            try:
                file_name = os.path.basename(file_path)
                file_ext = os.path.splitext(file_name)[1].lower()

                # Status Update
                self.status_label.config(text=f"Konvertiere {file_name}...")
                self.root.update()  # UI aktualisieren

                # Qualität und Kompressionseinstellungen basierend auf Dateityp
                lossless = False
                quality = self.jpg_quality.get()

                if file_ext in ('.png', '.PNG'):
                    if self.use_lossless_for_png.get():
                        lossless = True
                    else:
                        quality = self.png_quality.get()

                # Datei konvertieren
                result = self._convert_to_webp(
                    file_path,
                    quality=quality,
                    lossless=lossless
                )

                # In GUI anzeigen
                if result:
                    self._append_result(result)
                    processed += 1
                else:
                    failed += 1
            except Exception as e:
                self._append_result(f"FEHLER bei {file_name}: {str(e)}")
                failed += 1

            # Fortschritt aktualisieren
            progress = ((idx + 1) / total_files) * 100
            self.progress_var.set(progress)
            self.root.update()  # UI aktualisieren

        # Abschluss
        duration = time.time() - start_time

        # Zusammenfassung berechnen
        if self.conversion_stats:
            total_original = sum(stat['original_size'] for stat in self.conversion_stats)
            total_webp = sum(stat['webp_size'] for stat in self.conversion_stats)

            if total_original > 0:
                savings_percent = ((total_original - total_webp) / total_original) * 100
                total_saved = total_original - total_webp

                summary = (
                    f"\n--- ZUSAMMENFASSUNG ---\n"
                    f"Erfolgreich konvertiert: {processed} Dateien\n"
                    f"Fehlgeschlagen: {failed} Dateien\n"
                    f"Ursprüngliche Größe gesamt: {self._format_size(total_original)}\n"
                    f"WebP Größe gesamt: {self._format_size(total_webp)}\n"
                    f"Ersparnis: {self._format_size(total_saved)} ({savings_percent:.1f}%)\n"
                    f"Dauer: {duration:.1f} Sekunden"
                )

                self._append_result(summary)

        self.status_label.config(text=f"Fertig! {processed} Bilder konvertiert, {failed} fehlgeschlagen.")
        self.convert_btn.config(state=tk.NORMAL)

        # Erfolgsbenachrichtigung
        messagebox.showinfo(
            "Konvertierung abgeschlossen",
            f"{processed} von {total_files} Bildern erfolgreich konvertiert.\n"
            f"Ergebnisse wurden im Ordner gespeichert:\n{self.output_dir}"
        )

    def _convert_to_webp(self, input_path, quality=90, lossless=False):
        try:
            # Bild öffnen
            img = Image.open(input_path)

            # Ausgabepfad bestimmen
            filename = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(self.output_dir, f"{filename}.webp")

            # Optimierte Speicheroptionen
            save_options = {
                'format': 'WEBP',
                'method': 6,  # 0-6, 6 ist die höchste Kompression (langsamer)
            }

            # Lossless oder Qualität je nach Einstellung
            if lossless:
                save_options['lossless'] = True
            else:
                save_options['quality'] = quality

            # Speichern
            img.save(output_path, **save_options)

            # Größenvergleich
            original_size = os.path.getsize(input_path)
            webp_size = os.path.getsize(output_path)

            # Prozentuale Einsparung berechnen
            if original_size > 0:
                savings_percent = ((original_size - webp_size) / original_size) * 100
            else:
                savings_percent = 0

            # Größensparung für positive oder negative Werte
            if webp_size < original_size:
                size_change = f"Ersparnis: {self._format_size(original_size - webp_size)} ({savings_percent:.1f}%)"
            else:
                size_change = f"Zunahme: {self._format_size(webp_size - original_size)} ({-savings_percent:.1f}%)"

            # Statistik speichern
            stat = {
                'filename': os.path.basename(input_path),
                'original_size': original_size,
                'webp_size': webp_size,
                'savings_percent': savings_percent
            }
            self.conversion_stats.append(stat)

            # Ergebnistext formatieren
            result = (
                f"{os.path.basename(input_path)}: "
                f"{self._format_size(original_size)} → {self._format_size(webp_size)} "
                f"({size_change})"
            )

            return result

        except Exception as e:
            return None

    def _format_size(self, size_bytes):
        """Formatiert Bytes in lesbare Größe (KB, MB)"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.2f} MB"

    def _append_result(self, text):
        """Text zum Ergebnisbereich hinzufügen und scrollen"""
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.see(tk.END)
        self.root.update_idletasks()  # GUI aktualisieren


if __name__ == "__main__":
    # Wenn Pillow nicht installiert ist, zeige klare Fehlermeldung
    if not PIL_AVAILABLE:
        print("\nFEHLER: Die Pillow-Bibliothek (PIL) ist nicht installiert.")
        print("Dieses Programm benötigt Pillow zur Bildkonvertierung.")
        print("\nBitte installiere Pillow mit dem folgenden Befehl:")
        print("pip install Pillow\n")

        # Falls GUI nicht funktioniert, zeige Konsolenmeldung
        try:
            root = tk.Tk()
            app = WebPConverter(root)
            root.mainloop()
        except Exception:
            sys.exit(1)
    else:
        # Normale Ausführung
        root = tk.Tk()
        app = WebPConverter(root)
        root.mainloop()