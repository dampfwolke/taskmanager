from pathlib import Path
import json

from task import Task
from timestamp import timestamp

class ManageTasks:

    SAVE_PATH_DIR = Path(__file__).parent.parent.resolve() / "data"
    SAVE_PATH_FILE  = SAVE_PATH_DIR / "save_file.json"

    def __init__(self):
        self.current_task_list = []
        self.loaded_task_list = []

    def append_tasks_to_list(self):
        pass

    def save_to_json(self) -> None:
        """Speichert den Inhalt der current_task_list als list von dictionaries in eine JSON Datei.
        Der Pfad ist 'taskmanager/data/save_file.json'"""
        try:
            with open(self.SAVE_PATH_FILE, "w", encoding="utf-8") as f:
                json.dump(self.current_task_list, f, indent=4)
                print(f"JSON Datei erfolgreich gespeichert. {timestamp(1)}")
        except FileNotFoundError as e:
            print(f"Datei {self.SAVE_PATH_FILE} konnte nicht gefunden werden. {e}")
        except TypeError as e:
            print(f"Daten konnten nicht in JSON umgewandelt werden. {e}")
        except Exception as e:
            print(f"Unbekannter Fehler bei 'Task.save_to_json'. {e}")

    def load_from_json(self) -> list[dict] | None:
        """Lädt ein Task()-Objekt als dictionary von einer JSON Datei.
        Der Pfad ist 'taskmanager/data/save_file.json'
        Speichert das dictionary in eine list (self.loaded_tasks)."""
        try:
            with open(self.SAVE_PATH_FILE, "r", encoding="utf-8") as f:
                reader = json.load(f)
                print(f"JSON Datei erfolgreich geladen. {timestamp(1)}")
                return reader
        except FileNotFoundError as e:
            print(f"Datei {self.SAVE_PATH_FILE} konnte nicht gefunden werden. {e}")
            return None
        except Exception as e:
            print(f"Unbekannter Fehler beim Laden der JSON Datei. {e}")
            return None


if __name__ == "__main__":
    taskmanager_1 = ManageTasks()
    # task1 = Task("Aufräumen", "Abwaschen dann Staubsaugen", "wichtig")
    task2 = Task("Wartung Dampfer", "Watte und Coil wechseln", "wichtig")
    taskmanager_1.save_to_json()


