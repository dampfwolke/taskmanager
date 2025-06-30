import sys

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from UI.frm_main_window import Ui_frm_main_window
from animations.animation_handler import SidePanelAnimator
from animations.button_animator import ButtonAnimator

from new_task import NewTask

from utils.manage_tasks import ManageTasks

class MainWindow(qtw.QMainWindow, Ui_frm_main_window):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.frm_new_task = NewTask()
        self.resize(360, 500)
        self.ded_description.setDate(qtc.QDate.currentDate())
        self.ted_description.setTime(qtc.QTime.currentTime())
        self.pb_show_description.setDisabled(True)

        # ManageTasks Klasse aufrufen
        self.taskmanager = ManageTasks()
        self.taskmanager.load_from_json()
        self.categorize_tasks()


        # Initialisiere den Animator, nachdem das UI aufgebaut wurde.
        self.animator = SidePanelAnimator(parent_window=self, animated_widget_name="wg_main_description", toggle_button_name="pb_show_description")
        # BUTTON-ANIMATIONEN Liste hier alle Buttons auf, die den Effekt bekommen sollen.
        animated_buttons = ["pb_new_task", "pb_show_description", "pb_finish_task", "pb_edit_task"]
        self.button_animator = ButtonAnimator(self, animated_buttons)

        # Signale verbinden
        self.tb_tasks.currentChanged.connect(lambda: self.pb_show_description.setDisabled(True))

        self.lw_work.currentItemChanged.connect(lambda: self.pb_show_description.setDisabled(False))

        self.lw_home.currentItemChanged.connect(lambda: self.pb_show_description.setDisabled(False))
        self.lw_home.itemClicked.connect(self.show_details)

        self.lw_other.currentItemChanged.connect(lambda: self.pb_show_description.setDisabled(False))
        self.lw_finished.currentItemChanged.connect(lambda: self.pb_show_description.setDisabled(False))

        self.pb_new_task.clicked.connect(self.execute_new_task)
        self.pb_show_description.clicked.connect(self.show_details)


    def categorize_tasks(self):
        for task in self.taskmanager.task_list:
            if task.status.lower() == "Erledigt".lower():
                self.lw_finished.addItem(task.title)
            elif task.category == "zu Hause":
                self.lw_home.addItem(task.title)
            elif task.category == "Arbeit":
                self.lw_work.addItem(task.title)
            else:
                self.lw_other.addItem(task.title)

    @qtc.Slot()
    def show_details(self):
        for task in self.taskmanager.task_list:
            if task.title == self.lw_home.currentItem().text():
                self.te_description.setText(task.description)
                self.lb_task_title.setText(task.title)
                if task.due_date is None:
                    self.wg_description_time.setDisabled(True)


    @qtc.Slot()
    def execute_new_task(self):
        if self.frm_new_task:
            self.frm_new_task.close()
        self.frm_new_task = NewTask()
        self.frm_new_task.show()
        

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    with open("UI/Styles/Adapticnew.qss", "r") as stylesheet_file:
        app.setStyleSheet(stylesheet_file.read())
    sys.exit(app.exec())