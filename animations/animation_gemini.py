import sys
from functools import partial
from PySide6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QRect,
    QParallelAnimationGroup, QSequentialAnimationGroup, QSize
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QListWidgetItem, QStackedWidget,
    QFrame, QTextEdit, QButtonGroup, QSizePolicy
)

# ===================================================================
#  STYLESHEET (um den Look Ihrer App nachzubauen)
# ===================================================================
STYLESHEET = """
QWidget {
    background-color: #2b2b2b;
    color: #f0f0f0;
    font-family: Segoe UI;
    font-size: 10pt;
}

/* Die Tab-Buttons für die Aufgaben */
#AccordionButton {
    text-align: left;
    padding: 8px;
    border: 1px solid #444;
    border-radius: 4px;
    background-color: #3c3c3c;
}
#AccordionButton:hover {
    background-color: #4a4a4a;
}
#AccordionButton:checked {
    background-color: #555555;
    border-bottom: 2px solid #007acc; /* Blauer Indikator für aktiven Tab */
}

/* Der Container für die Listen */
#TaskStackedWidget {
    border: none;
}

QListWidget {
    border: 1px solid #444;
    border-radius: 4px;
    padding: 5px;
    background-color: #333333;
}
QListWidget::item {
    padding: 5px;
}
QListWidget::item:hover {
    background-color: #4a4a4a;
}
QListWidget::item:selected {
    background-color: #007acc;
    color: white;
}

/* Das rechte Slide-in Panel */
#SidePanel {
    background-color: #252526;
    border-left: 1px solid #444;
}

QLabel#HeaderLabel {
    font-size: 12pt;
    font-weight: bold;
    padding: 5px;
    color: #cccccc;
}

QPushButton {
    background-color: #4a4a4a;
    border: 1px solid #555;
    padding: 8px;
    border-radius: 4px;
}
QPushButton:hover {
    background-color: #5a5a5a;
}
QPushButton:pressed {
    background-color: #6a6a6a;
}
"""


# ===================================================================
#  ANIMATOR-KLASSE FÜR DAS AKKORDION (Aufgaben-Bereich)
# ===================================================================
class AccordionAnimator:
    def __init__(self, buttons: list[QPushButton], stacked_widget: QStackedWidget, duration=1800):
        self.stacked_widget = stacked_widget
        self.buttons = buttons
        self.duration = duration
        self.page_heights = [stacked_widget.widget(i).sizeHint().height() for i in range(stacked_widget.count())]

        # Button-Gruppe sorgt dafür, dass nur ein Button gleichzeitig "checked" sein kann
        self.button_group = QButtonGroup()
        for i, button in enumerate(self.buttons):
            button.setCheckable(True)
            self.button_group.addButton(button, i)

        # Signal verbinden
        self.button_group.idClicked.connect(self.animate_to_page)

        # Initialzustand
        self.buttons[0].setChecked(True)
        self.stacked_widget.setCurrentIndex(0)
        self.stacked_widget.setMaximumHeight(self.page_heights[0])

    def animate_to_page(self, target_index: int):
        current_index = self.stacked_widget.currentIndex()
        if current_index == target_index:
            return

        target_height = self.page_heights[target_index]
        current_widget = self.stacked_widget.widget(current_index)

        # Wir erstellen eine Sequenz: 1. Zuklappen, 2. Seite wechseln, 3. Aufklappen

        # Animation zum Zuklappen (auf Höhe 0)
        collapse_anim = QPropertyAnimation(self.stacked_widget, b"maximumHeight")
        collapse_anim.setDuration(self.duration // 2)
        collapse_anim.setStartValue(self.stacked_widget.height())
        collapse_anim.setEndValue(0)
        collapse_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Animation zum Aufklappen (auf Zielhöhe)
        expand_anim = QPropertyAnimation(self.stacked_widget, b"maximumHeight")
        expand_anim.setDuration(self.duration)
        expand_anim.setStartValue(0)
        expand_anim.setEndValue(target_height)
        expand_anim.setEasingCurve(QEasingCurve.Type.OutCubic)  # Out fühlt sich "federnder" an

        # Sequenz zusammenbauen
        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(collapse_anim)
        self.animation_group.addPause(10)  # Kleine Pause
        self.animation_group.addAnimation(expand_anim)

        # Wenn die Zuklapp-Animation fertig ist, wechseln wir die Seite
        collapse_anim.finished.connect(lambda: self.stacked_widget.setCurrentIndex(target_index))

        self.animation_group.start()


# ===================================================================
#  ANIMATOR-KLASSE FÜR DAS SEITEN-PANEL (Beschreibung)
# ===================================================================
class SidePanelAnimator:
    def __init__(self, parent: QWidget, panel: QWidget, duration=350):
        self.parent = parent
        self.panel = panel
        self.duration = duration
        self.is_open = False

        # Die Breite des Panels, die wir aufklappen wollen
        self.panel_width = 325
        # Start- und Endbreite des Hauptfensters
        self.closed_width = 325
        self.open_width = self.closed_width + self.panel_width

        self.animation_group = QParallelAnimationGroup(parent)

    def toggle_panel(self):
        # Animation für die Position des Panels
        panel_anim = QPropertyAnimation(self.panel, b"geometry")
        panel_anim.setDuration(self.duration)
        panel_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Animation für die Breite des Hauptfensters
        window_anim = QPropertyAnimation(self.parent, b"minimumWidth")
        window_anim.setDuration(self.duration)
        window_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        if self.is_open:
            # --- Panel SCHLIESSEN ---
            start_geo = self.panel.geometry()
            end_geo = QRect(self.open_width, start_geo.y(), self.panel_width, start_geo.height())

            panel_anim.setStartValue(start_geo)
            panel_anim.setEndValue(end_geo)

            window_anim.setStartValue(self.open_width)
            window_anim.setEndValue(self.closed_width)

            # Panel nach der Animation verstecken
            self.animation_group.finished.connect(self.panel.hide)
        else:
            # --- Panel ÖFFNEN ---
            self.panel.show()
            # Startposition des Panels ist außerhalb des sichtbaren Bereichs
            start_geo = QRect(self.closed_width, self.panel.y(), self.panel_width, self.panel.height())
            # Endposition ist am rechten Rand des neuen, breiteren Fensters
            end_geo = QRect(self.closed_width, self.panel.y(), self.panel_width, self.panel.height())

            panel_anim.setStartValue(start_geo)
            panel_anim.setEndValue(end_geo)

            window_anim.setStartValue(self.closed_width)
            window_anim.setEndValue(self.open_width)

            # Sicherstellen, dass die Verbindung zu hide() getrennt wird
            try:
                self.animation_group.finished.disconnect(self.panel.hide)
            except (TypeError, RuntimeError):
                pass

        self.animation_group.clear()  # Alte Animationen entfernen
        self.animation_group.addAnimation(panel_anim)
        self.animation_group.addAnimation(window_anim)
        self.animation_group.start()

        self.is_open = not self.is_open


# ===================================================================
#  HAUPTFENSTER
# ===================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager Beta")
        self.setMinimumSize(325, 550)

        # --- Widgets erstellen ---
        self._create_widgets()
        # --- Layout aufbauen ---
        self._setup_layout()
        # --- Animationen und Verbindungen einrichten ---
        self._setup_animations_and_connections()

        self.setStyleSheet(STYLESHEET)

    def _create_widgets(self):
        # --- Linker Bereich: Aufgaben ---
        self.btn_high = QPushButton("Hoch")
        self.btn_high.setObjectName("AccordionButton")
        self.btn_medium = QPushButton("Mittel")
        self.btn_medium.setObjectName("AccordionButton")
        self.btn_low = QPushButton("Niedrig")
        self.btn_low.setObjectName("AccordionButton")

        self.list_high = QListWidget()
        self.list_high.addItems([f"Wichtige Aufgabe #{i}" for i in range(1, 6)])
        self.list_medium = QListWidget()
        self.list_medium.addItems([f"Normale Aufgabe #{i}" for i in range(1, 10)])
        self.list_low = QListWidget()
        self.list_low.addItems([f"Optionale Aufgabe #{i}" for i in range(1, 4)])

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("TaskStackedWidget")
        self.stacked_widget.addWidget(self.list_high)
        self.stacked_widget.addWidget(self.list_medium)
        self.stacked_widget.addWidget(self.list_low)
        # Wichtig, damit die Höhe korrekt berechnet werden kann
        self.stacked_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        self.btn_details = QPushButton("Detailansicht")

        # --- Rechter Bereich: Beschreibung (das Slide-Panel) ---
        self.right_panel = QFrame(self)  # WICHTIG: parent ist self (QMainWindow)
        self.right_panel.setObjectName("SidePanel")
        self.right_panel.setFrameShape(QFrame.Shape.NoFrame)
        # Position wird durch Animation gesteuert, aber wir brauchen eine Anfangsgröße
        self.right_panel.setGeometry(325, 0, 325, self.height())
        self.right_panel.hide()

    def _setup_layout(self):
        # --- Layout für den linken Bereich ---
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Aufgaben", objectName="HeaderLabel"))
        left_layout.addWidget(self.btn_high)
        left_layout.addWidget(self.btn_medium)
        left_layout.addWidget(self.btn_low)
        left_layout.addWidget(self.stacked_widget)
        left_layout.addStretch()  # Drückt alles nach oben
        left_layout.addWidget(self.btn_details)

        left_container = QWidget()
        left_container.setLayout(left_layout)

        # --- Haupt-Layout (hat nur den linken Container) ---
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # --- Layout für das rechte Panel (intern) ---
        right_panel_layout = QVBoxLayout()
        right_panel_layout.addWidget(QLabel("Beschreibung", objectName="HeaderLabel"))
        right_panel_layout.addWidget(QLabel("Überschrift Aufgabe"))
        right_panel_layout.addWidget(QTextEdit())
        right_panel_layout.addStretch()
        self.right_panel.setLayout(right_panel_layout)

    def _setup_animations_and_connections(self):
        # Accordion Animator für den Aufgaben-Bereich
        self.accordion_animator = AccordionAnimator(
            [self.btn_high, self.btn_medium, self.btn_low],
            self.stacked_widget
        )

        # Side Panel Animator für den Beschreibungs-Bereich
        self.side_panel_animator = SidePanelAnimator(self, self.right_panel)
        self.btn_details.clicked.connect(self.side_panel_animator.toggle_panel)

    # Das Panel muss bei Größenänderung des Fensters neu positioniert werden
    def resizeEvent(self, event: "QResizeEvent"):
        super().resizeEvent(event)
        if not self.side_panel_animator.is_open:
            # Das versteckte Panel an den rechten Rand schieben
            self.right_panel.setGeometry(self.width(), 0, self.side_panel_animator.panel_width, self.height())
        else:
            # Das offene Panel an seiner Position halten
            self.right_panel.setGeometry(self.width() - self.side_panel_animator.panel_width, 0,
                                         self.side_panel_animator.panel_width, self.height())


# ===================================================================
#  ANWENDUNG STARTEN
# ===================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())