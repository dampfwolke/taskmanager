from timestamp import timestamp

class Task:

    def __init__(self, title: str, 	description: str, category: str, status: str="in Bearbeitung", due_date: str=None):
        self.title = title
        self.description = description
        self.category = category
        self.status = status
        self.due_date = due_date
        self.creation_date = timestamp(3)

        self.task_dict = self.create_task_dict()

    def create_task_dict(self) -> dict:
        task_dict = {"title": self.title, "description": self.description,
                     "category": self.category,
                     "status": self.status,
                     "due_date": self.due_date,
                     "creation_date": self.creation_date}
        return task_dict

    def __repr__(self):
        return f'ManageTask("{self.title}", "{self.description}", "{self.category}")'


if __name__ == "__main__":
    task1 = Task("Aufräumen", "Abwaschen dann Staubsaugen", "wichtig")
    task2 = Task("Wartung Dampfer", "Watte und Coil wechseln", "wichtig")
    print(task2.task_dict)