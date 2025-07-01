# --- START OF FILE task.py ---

from PySide6.QtCore import QDateTime, QTimeZone

from utils.timestamp import timestamp


class Task:

    # GEÄNDERT: __init__ korrigiert, um das Überschreiben des Erstellungsdatums zu verhindern
    def __init__(self, title: str, description: str, category: str, status: str="in Bearbeitung", due_date: str=None, creation_date: str=None):
        self.title = title
        self.description = description
        self.category = category
        self.status = status
        self.due_date = due_date
        # Wenn kein Erstellungsdatum übergeben wird (neue Aufgabe), erstelle ein neues.
        # Andernfalls (beim Laden aus JSON), verwende das übergebene Datum.
        self.creation_date = creation_date if creation_date is not None else timestamp(3)

    # NEU: Methode zur Überprüfung, ob eine Aufgabe überfällig ist
    def is_overdue(self) -> bool:
        """
        Prüft, ob das Fälligkeitsdatum der Aufgabe in der Vergangenheit liegt.
        Gibt True zurück, wenn überfällig, sonst False.
        """
        if not self.due_date:
            return False  # Aufgaben ohne Datum können nicht überfällig sein

        try:
            # Parse den Datums-String in ein QDateTime-Objekt
            due_datetime = QDateTime.fromString(self.due_date, "yyyy-MM-dd HH:mm:ss")
            # Hole die aktuelle Zeit
            now = QDateTime.currentDateTime()
            # Vergleiche: Ist das Fälligkeitsdatum kleiner als jetzt?
            return due_datetime < now
        except Exception:
            # Falls beim Parsen etwas schiefgeht, betrachte es als nicht überfällig
            return False

    def show_info(self) -> str:
        return f"{self.title}, {self.description}, {self.category}, {self.status}, {self.due_date}, {self.creation_date}"

    def update_status(self, status="Erledigt") -> None:
        self.status = status

    def update_category(self, category):
        self.category = category

    def create_task_dict(self) -> dict:
        """Returned ein dict mit allen Daten der Aufgabe."""
        task_dict = {"title": self.title, "description": self.description,
                     "category": self.category,
                     "status": self.status,
                     "due_date": self.due_date,
                     "creation_date": self.creation_date}
        return task_dict

    @classmethod
    def json_to_task(cls, json_data: dict) -> "Task":
        """Erstellt aus einem dict wieder ein Task-Objekt."""
        return cls(title=json_data["title"],
                   description=json_data["description"],
                   category=json_data["category"],
                   status=json_data.get("status"),
                   due_date=json_data.get("due_date"),
                   # NEU: Das Erstellungsdatum wird aus der JSON-Datei gelesen und übergeben
                   creation_date=json_data.get("creation_date")
                   )

    def __repr__(self):
        return f'Task("{self.title}")'

    def __str__(self):
        return f"Titel: {self.title}, Kategorie: {self.category}, Status: {self.status}"

if __name__ == "__main__":
    task1 = Task("Aufräumen", "Abwaschen dann Staubsaugen", "wichtig")
    task2 = Task("Wartung Dampfer", "Watte und Coil wechseln", "wichtig")