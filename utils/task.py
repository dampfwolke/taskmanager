from timestamp import timestamp

class Task:

    def __init__(self, title: str, 	description: str, category: str, status: str="in Bearbeitung", due_date: str=None):
        self.title = title
        self.description = description
        self.category = category
        self.status = status
        self.due_date = due_date
        self.creation_date = timestamp(3)

    def show_info(self) -> str:
        return f"{self.title}, {self.description}, {self.category}, {self.status}, {self.due_date}, {self.creation_date}"

    def update_status(self, status="Erledigt") -> None:
        self.status = status

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
                   due_date=json_data.get("due_date")
                   )

    def __repr__(self):
        return f'Task("{self.title}", "{self.description}", "{self.category}")'


if __name__ == "__main__":
    task1 = Task("Aufräumen", "Abwaschen dann Staubsaugen", "wichtig")
    task2 = Task("Wartung Dampfer", "Watte und Coil wechseln", "wichtig")

