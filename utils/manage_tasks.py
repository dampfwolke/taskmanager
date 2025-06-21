from pathlib import Path
import json

from task import Task
from timestamp import timestamp

class ManageTasks:

    SAVE_PATH_DIR = Path(__file__).parent.parent.resolve() / "data"
    SAVE_PATH_FILE  = SAVE_PATH_DIR / "save_file.json"

    def __init__(self):
        self.task_list = []

    def append_task(self, *tasks: Task):
        for tasks in tasks:
            self.task_list.append(tasks)

    def save_to_json(self) -> None:
        """Kombiniert den Inhalt der self.current_task_list und self.loaded_task_list und speichert die neue list von dictionaries
         in die JSON Datei 'taskmanager/data/save_file.json'"""
        list_of_dicts = [task_.create_task_dict() for task_ in self.task_list]
        try:
            with open(self.SAVE_PATH_FILE, "w", encoding="utf-8") as f:
                json.dump(list_of_dicts, f, indent=4)
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
                    task_object = Task.json_to_task(task_dict)
                    self.task_list.append(task_object)
        except FileNotFoundError as e:
            print(f"Datei {self.SAVE_PATH_FILE} konnte nicht gefunden werden. {e}")
        except json.decoder.JSONDecodeError as e:
            print(f"Die JSON-Datei ist leer oder ungültig. {e}")
        except Exception as e:
            print(f"Unbekannter Fehler beim Laden der JSON Datei. {e}")


if __name__ == "__main__":
    tm = ManageTasks()
    # task1 = Task("Nacharbeit", "NA-Pgm Gtech erstellen", "wichtig")
    # task2 = Task("Pgm-Änderung IFW", "Kulisse Pgm anpassen", "niedrig")






