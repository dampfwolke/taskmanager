import sys
import ctypes
import datetime
import struct
from pathlib import Path
from collections import defaultdict

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel, QTextEdit, QSizePolicy
)
from PySide6.QtCore import Qt, Slot

# -----------------------------------------------------------------------------
# WICHTIG: Pfad zur Everything SDK DLL anpassen!
# -----------------------------------------------------------------------------
try:
    # Versuchen Sie, den Pfad relativ zum Skriptverzeichnis zu finden,
    # falls das SDK-Verzeichnis neben dem Skript liegt.
    # Ansonsten den absoluten Pfad verwenden.
    SCRIPT_DIR = Path(__file__).parent.resolve()
    DLL_DIR = SCRIPT_DIR / "Everything-SDK" / "dll"  # Beispielhafter relativer Pfad
    if not DLL_DIR.exists():  # Fallback auf Ihren angegebenen Pfad
        DLL_DIR = Path("C:\\Users\\hasanovic\\Desktop\\Everything API\\dll\\").resolve()

    # Automatisch 64-bit oder 32-bit DLL wählen (basierend auf Python-Architektur)
    if ctypes.sizeof(ctypes.c_void_p) == 8:  # 64-bit Python
        DLL_PATH = DLL_DIR / "Everything64.dll"
    else:  # 32-bit Python
        DLL_PATH = DLL_DIR / "Everything32.dll"

    if not DLL_PATH.exists():
        raise FileNotFoundError(f"Everything DLL nicht gefunden unter: {DLL_PATH}")

except NameError:  # Tritt auf, wenn __file__ nicht definiert ist (z.B. in manchen IDEs/REPLs)
    DLL_DIR = Path("C:\\Users\\Ismail\\Desktop\\Zielordner\\Everything-SDK\\dll\\").resolve()
    if ctypes.sizeof(ctypes.c_void_p) == 8:
        DLL_PATH = DLL_DIR / "Everything64.dll"
    else:
        DLL_PATH = DLL_DIR / "Everything32.dll"
    if not DLL_PATH.exists():
        # Kritischer Fehler, hier könnten wir nicht weitermachen
        print(f"KRITISCH: Everything DLL nicht gefunden unter: {DLL_PATH}")
        sys.exit(1)
# -----------------------------------------------------------------------------

# Everything API Konstanten
EVERYTHING_REQUEST_FILE_NAME = 0x00000001
EVERYTHING_REQUEST_PATH = 0x00000002
EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME = 0x00000004
EVERYTHING_REQUEST_EXTENSION = 0x00000008
EVERYTHING_REQUEST_SIZE = 0x00000010
EVERYTHING_REQUEST_DATE_CREATED = 0x00000020
EVERYTHING_REQUEST_DATE_MODIFIED = 0x00000040
# ... (weitere Konstanten aus dem SDK-Beispiel bei Bedarf)

# Hilfsfunktion zur Konvertierung von Windows FILETIME zu Python datetime
# (Aus dem SDK-Beispiel übernommen und leicht angepasst)
WINDOWS_TICKS = int(1 / 10 ** -7)
WINDOWS_EPOCH = datetime.datetime.strptime('1601-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
POSIX_EPOCH = datetime.datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
EPOCH_DIFF_SECONDS = (POSIX_EPOCH - WINDOWS_EPOCH).total_seconds()
WINDOWS_TICKS_TO_POSIX_EPOCH = EPOCH_DIFF_SECONDS * WINDOWS_TICKS


def filetime_to_datetime(filetime_qword):
    """Konvertiert eine Windows FILETIME (als QWORD/ctypes.c_ulonglong) zu datetime."""
    winticks = filetime_qword.value
    if winticks == 0:  # Ungültiges Datum oder nicht gesetzt
        return datetime.datetime.min  # Oder None, je nach gewünschtem Verhalten
    microsecs = (winticks - WINDOWS_TICKS_TO_POSIX_EPOCH) / WINDOWS_TICKS
    try:
        return datetime.datetime.fromtimestamp(microsecs)
    except ValueError:  # Kann bei sehr alten oder ungültigen Daten auftreten
        return datetime.datetime.min


class EverythingSearchGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.everything_dll = None
        self.init_dll()
        self.init_ui()

    def init_dll(self):
        try:
            self.everything_dll = ctypes.WinDLL(str(DLL_PATH))
            # Überprüfen, ob die DLL geladen wurde und Everything läuft
            # Everything_GetMajorVersion gibt 0 zurück, wenn die IPC nicht verfügbar ist
            if self.everything_dll.Everything_GetMajorVersion() == 0:
                print("Everything Dienst scheint nicht zu laufen oder IPC ist nicht verfügbar.")
                # Hier könnte man eine Fehlermeldung in der GUI anzeigen
                self.everything_dll = None  # Verhindert weitere Aufrufe
        except FileNotFoundError:
            print(f"FEHLER: Everything DLL nicht gefunden unter '{DLL_PATH}'.")
            print("Bitte laden Sie das Everything SDK herunter und passen Sie den Pfad im Skript an.")
        except Exception as e:
            print(f"Fehler beim Laden der Everything DLL: {e}")

    def init_ui(self):
        self.setWindowTitle("Everything Datei Suche")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)

        # Eingabebereich
        input_layout = QHBoxLayout()
        self.filename_label = QLabel("Dateiname:")
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Teil des Dateinamens...")
        self.filename_input.editingFinished.connect(self.search_triggered)

        self.extension_label = QLabel("Endung (z.B. .txt):")
        self.extension_input = QLineEdit()
        self.extension_input.setPlaceholderText(".log, .docx, etc.")
        # self.extension_input.textEdited.connect(self.search_triggered)
        self.extension_input.setMaximumWidth(150)

        input_layout.addWidget(self.filename_label)
        input_layout.addWidget(self.filename_input)
        input_layout.addWidget(self.extension_label)
        input_layout.addWidget(self.extension_input)
        layout.addLayout(input_layout)

        # Ergebnisanzahl
        self.results_count_label = QLabel("Dateien gefunden: 0")
        layout.addWidget(self.results_count_label)

        # Ergebnisbereich
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setFontFamily("Consolas")  # Monospace für bessere Lesbarkeit
        layout.addWidget(self.results_display)

        self.setLayout(layout)

    @Slot()
    def search_triggered(self):
        if not self.everything_dll:
            self.results_display.setText("Everything DLL nicht geladen oder Dienst nicht verfügbar.")
            self.results_count_label.setText("Dateien gefunden: 0")
            return

        search_term = self.filename_input.text().strip()
        extension_filter = self.extension_input.text().strip()

        if not search_term and not extension_filter:
            self.results_display.clear()
            self.results_count_label.setText("Dateien gefunden: 0")
            return

        # Suchanfrage für Everything zusammenbauen
        query_parts = []
        if search_term:
            query_parts.append(search_term)
        if extension_filter:
            if not extension_filter.startswith("."):
                extension_filter = "." + extension_filter
            query_parts.append(f"ext:{extension_filter.lstrip('.')}")  # Everything erwartet ext:txt, nicht ext:.txt

        full_query = " ".join(query_parts)

        # Debug-Ausgabe der Query
        # print(f"Everything Query: '{full_query}'")

        results = self._find_files_backend(full_query)
        self._format_and_display_results(results)

    def _find_files_backend(self, query):
        if not self.everything_dll:
            return []

        # 1. Suchbegriff setzen
        self.everything_dll.Everything_SetSearchW(query)

        # 2. Angeforderte Informationen (Pfad und Änderungsdatum)
        request_flags = EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME | EVERYTHING_REQUEST_DATE_MODIFIED
        self.everything_dll.Everything_SetRequestFlags(request_flags)

        # Sortierung direkt in Everything festlegen (optional, aber effizienter)
        # 1 = Ascending, 2 = Descending
        # EVERYTHING_SORT_DATE_MODIFIED = 6
        # self.everything_dll.Everything_SetSort(EVERYTHING_SORT_DATE_MODIFIED)
        # self.everything_dll.Everything_SetSortDirection(2) # Neueste zuerst

        # 3. Suche ausführen
        if not self.everything_dll.Everything_QueryW(True):  # True = warten
            print("Everything_QueryW fehlgeschlagen.")
            return []

        num_results = self.everything_dll.Everything_GetNumResults()
        found_files = []

        if num_results > 0:
            path_buffer = ctypes.create_unicode_buffer(1024)  # Erhöhter Puffer
            date_modified_filetime = ctypes.c_ulonglong()

            for i in range(num_results):
                # Vollständigen Pfad abrufen
                self.everything_dll.Everything_GetResultFullPathNameW(i, path_buffer, 1024)
                full_path = Path(path_buffer.value)

                # Änderungsdatum abrufen
                self.everything_dll.Everything_GetResultDateModified(i, ctypes.byref(date_modified_filetime))
                mod_datetime = filetime_to_datetime(date_modified_filetime)

                found_files.append({"path": full_path, "date_modified": mod_datetime})

        return found_files

    def _format_and_display_results(self, results):
        # self.results_count_label.setText(f"Dateien gefunden: {len(results)}")
        self.results_count_label.setText(f"Programm vorhanden! Stehend fräsen??? Anzahl Programme: {len(results)}")
        if not results:
            self.results_display.clear()
            return

        # Sortieren: Zuerst nach Laufwerksbuchstabe, dann nach Änderungsdatum (neueste zuerst)
        results.sort(
            key=lambda x: (x["path"].drive.lower(), -x["date_modified"].timestamp() if x["date_modified"] else 0))

        output_text = []
        current_drive = None
        for item in results:
            path_obj = item["path"]
            mod_date = item["date_modified"]

            if path_obj.drive != current_drive:
                current_drive = path_obj.drive
                output_text.append(f"\n--- Laufwerk {current_drive.upper()} ---")

            date_str = mod_date.strftime('%Y-%m-%d %H:%M:%S') if mod_date != datetime.datetime.min else "N/A"
            output_text.append(f"{date_str} - {path_obj}")

        self.results_display.setText("\n".join(output_text))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Sicherstellen, dass Everything läuft, bevor die GUI gestartet wird
    # Dies ist eine einfache Prüfung; eine robustere Prüfung wäre besser.
    try:
        temp_dll = ctypes.WinDLL(str(DLL_PATH))
        if temp_dll.Everything_GetMajorVersion() == 0:
            print("WARNUNG: Everything scheint nicht zu laufen. Die Suche wird nicht funktionieren.")
            # Hier könnte man dem Benutzer eine Nachricht anzeigen und die App beenden oder
            # die GUI trotzdem starten, aber mit einer Fehlermeldung.
    except Exception as e:
        print(f"FEHLER beim Prüfen von Everything: {e}. Stellen Sie sicher, dass das SDK korrekt eingerichtet ist.")
        # sys.exit(1) # Beenden, wenn DLL nicht geladen werden kann

    main_window = EverythingSearchGUI()
    main_window.show()
    sys.exit(app.exec())