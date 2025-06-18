# animations/animation_handler_placeholder.py (FINAL - Mit QTimer zur Synchronisation)

from PySide6.QtCore import QObject, QPropertyAnimation, QEasingCurve, QAbstractAnimation, QTimer
from PySide6.QtWidgets import QWidget


class SidePanelAnimatorPlaceholder(QObject):
    """
    Realisiert eine sequentielle Animation mit der "Platzhalter"-Methode.
    FINALE, FUNKTIONIERENDE VERSION: Verwendet einen QTimer, um das Umschalten des
    Widgets mit dem Qt Event Loop zu synchronisieren und so Anzeigefehler zu beheben.
    """

    def __init__(self, parent_window, stacked_widget_name, animated_widget_name, toggle_button_name):
        super().__init__(parent_window)

        # --- Referenzen speichern ---
        self.parent_window = parent_window
        self.toggle_button = getattr(parent_window, toggle_button_name)
        self.stacked_widget = getattr(parent_window, stacked_widget_name)
        self.animated_widget = getattr(parent_window, animated_widget_name)

        # --- Platzhalter-Widget dynamisch erstellen und hinzufügen ---
        self.placeholder = QWidget()
        self.stacked_widget.insertWidget(0, self.placeholder)
        self.placeholder_index = 0
        self.animated_widget_index = 1

        # --- Animationseinstellungen ---
        self.animation_duration = 350
        self.easing_curve = QEasingCurve.Type.InOutCubic
        self.is_expanded = False

        self.panel_target_width = self.animated_widget.sizeHint().width()
        if self.panel_target_width <= 10:
            self.panel_target_width = 325

        # --- Nur EINE Animation, die die Größe des StackedWidgets steuert ---
        self.size_animation = QPropertyAnimation(self.stacked_widget, b"maximumWidth")
        self.size_animation.setDuration(self.animation_duration)
        self.size_animation.setEasingCurve(self.easing_curve)

        # Einmalige Verbindung des finished-Signals
        self.size_animation.finished.connect(self.on_animation_finished)

        self.toggle_button.clicked.connect(self.toggle_animation)

        # Initialen Zustand setzen
        self.stacked_widget.setMaximumWidth(0)
        self.stacked_widget.setCurrentIndex(self.placeholder_index)

    def toggle_animation(self):
        """ Startet die entsprechende Animationssequenz. """
        if self.size_animation.state() == QAbstractAnimation.State.Running:
            return

        current_width = self.stacked_widget.width()

        if self.is_expanded:
            # --- ZIEL: ZUKLAPPEN ---
            # Der Inhalt wird sofort unsichtbar, indem wir den Platzhalter zeigen.
            self.stacked_widget.setCurrentIndex(self.placeholder_index)
            self.size_animation.setStartValue(current_width)
            self.size_animation.setEndValue(0)
            self.is_expanded = False  # Zustand sofort aktualisieren
        else:
            # --- ZIEL: AUFKLAPPEN ---
            # Der Platzhalter ist bereits sichtbar oder wird es jetzt.
            self.size_animation.setStartValue(current_width)
            self.size_animation.setEndValue(self.panel_target_width)
            self.is_expanded = True  # Zustand sofort aktualisieren

        self.size_animation.start()

    def on_animation_finished(self):
        """
        Wird aufgerufen, wenn die Größen-Animation beendet ist.
        Setzt den finalen sichtbaren Zustand.
        """
        # Wenn der finale Zustand "aufgeklappt" sein soll...
        if self.is_expanded:
            # *** DIE ENTSCHEIDENDE LÖSUNG ***
            # Wir rufen das Umschalten nicht sofort auf, sondern geben den Befehl
            # an das Ende der Event-Warteschlange. Das gibt der GUI-Engine
            # Zeit, das Ende der Animation zu verarbeiten.
            QTimer.singleShot(0, lambda: self.stacked_widget.setCurrentIndex(self.animated_widget_index))