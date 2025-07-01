# --- START OF FILE manage_tasks.py ---

from pathlib import Path
import json

from utils.task import Task
from utils.timestamp import timestamp

class ManageTasks:

    SAVE_PATH_DIR = Path(__file__).parent.parent.resolve() / "data"
    SAVE_PATH_FILE  = SAVE_PATH_DIR / "save_file.json"

    def __init__(self):
        self.task_list = []
        # GEÄNDERT: task_dict wird nicht benötigt, wenn wir setData verwenden
        # self.task_dict = {}

    def append_task(self, *tasks: Task):
        for task_ in tasks:
            self.task_list.append(task_)

    # GEÄNDERT: to_task_dict entfernt, da ungenutzt.

    def save_to_json(self) -> None:
        """Speichert die komplette self.task_list in die JSON-Datei."""
        # GEÄNDERT: Korrekte Verwendung von self.task_list
        list_of_dicts = [task_.create_task_dict() for task_ in self.task_list]
        try:
            # Stellt sicher, dass das Verzeichnis existiert
            self.SAVE_PATH_DIR.mkdir(parents=True, exist_ok=True)
            with open(self.SAVE_PATH_FILE, "w", encoding="utf-8") as f:
                json.dump(list_of_dicts, f, indent=4, ensure_ascii=False) # NEU: ensure_ascii=False für Umlaute
                print(f"JSON Datei erfolgreich gespeichert. {timestamp(1)}")
        except FileNotFoundError as e:
            print(f"Datei {self.SAVE_PATH_FILE} konnte nicht gefunden werden. {e}")
        except TypeError as e:
            print(f"Daten konnten nicht in JSON umgewandelt werden. {e}")
        except Exception as e:
            print(f"Unbekannter Fehler bei 'Task.save_to_json'. {e}")

    def load_from_json(self) -> None:
        """Lädt Task-Objekte aus einer JSON-Datei."""
        if not self.SAVE_PATH_FILE.exists():
            print("Keine Speicherdatei gefunden. Starte mit leerer Aufgabenliste.")
            return

        try:
            with open(self.SAVE_PATH_FILE, "r", encoding="utf-8") as f:
                reader = json.load(f)
                print(f"JSON Datei erfolgreich geladen. {timestamp(1)}")
                self.task_list.clear() # Sicherstellen, dass die Liste vor dem Laden leer ist
                for task_dict in reader:
                    task_object = Task.json_to_task(task_dict)
                    self.task_list.append(task_object)
        except json.decoder.JSONDecodeError:
            print(f"Die JSON-Datei '{self.SAVE_PATH_FILE}' ist leer oder beschädigt.")
        except Exception as e:
            print(f"Unbekannter Fehler beim Laden der JSON Datei: {e}")


if __name__ == "__main__":
    tm = ManageTasks()