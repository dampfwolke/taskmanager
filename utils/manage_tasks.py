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

    def append_task(self, *tasks: Task):
        for task in tasks:
            task_dict = task.create_task_dict()
            self.current_task_list.append(task_dict)

    def save_to_json(self) -> None:
        """Kombiniert den Inhalt der self.current_task_list und self.loaded_task_list und speichert die neue list von dictionaries
         in die JSON Datei 'taskmanager/data/save_file.json'"""
        combined_task_list = self.current_task_list + self.loaded_task_list
        try:
            with open(self.SAVE_PATH_FILE, "w", encoding="utf-8") as f:
                json.dump(combined_task_list, f, indent=4)
                print(f"JSON Datei erfolgreich gespeichert. {timestamp(1)}")
        except FileNotFoundError as e:
            print(f"Datei {self.SAVE_PATH_FILE} konnte nicht gefunden werden. {e}")
        except TypeError as e:
            print(f"Daten konnten nicht in JSON umgewandelt werden. {e}")
        except Exception as e:
            print(f"Unbekannter Fehler bei 'Task.save_to_json'. {e}")

    def load_from_json(self) -> None:
        """Lädt Task()-Objekte als dictionary von einer JSON Datei.
        Der Pfad ist 'taskmanager/data/save_file.json'
        Speichert das dictionary in eine list (self.loaded_task_list)."""
        try:
            with open(self.SAVE_PATH_FILE, "r", encoding="utf-8") as f:
                reader = json.load(f)
                print(f"JSON Datei erfolgreich geladen. {timestamp(1)}")
                for task_dict in reader:
                    self.loaded_task_list.append(task_dict)
        except FileNotFoundError as e:
            print(f"Datei {self.SAVE_PATH_FILE} konnte nicht gefunden werden. {e}")
            return None
        except Exception as e:
            print(f"Unbekannter Fehler beim Laden der JSON Datei. {e}")
            return None


if __name__ == "__main__":
    taskmanager_1 = ManageTasks()
    # task1 = Task("Nacharbeit", "NA-Pgm Gtech erstellen", "wichtig")
    # task2 = Task("Pgm-Änderung", "Kulisse Pgm anpassen", "niedrig")

    task1 = Task.json_to_task(taskmanager_1.SAVE_PATH_FILE)






