# animations/animation_handler.py

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QObject


class SidePanelAnimator(QObject):
    """
    Manages the slide animation for a side panel widget in a Qt application.

    This class handles the animation of a widget's maximumWidth property to create
    a smooth expand/collapse effect. It's designed to be used with a main window
    where the UI has been set up via a compiled .ui file (setupUi).
    """

    def __init__(self, parent_window, animated_widget_name, toggle_button_name):
        """
        Initializes the animator.

        Args:
            parent_window: The main window instance (self) after setupUi() has been called.
            animated_widget_name (str): The objectName of the widget to be animated.
            toggle_button_name (str): The objectName of the button that triggers the animation.
        """
        super().__init__(parent_window)

        # UI-Elemente direkt aus dem übergeordneten Fenster holen (da setupUi verwendet wird)
        # --- HIER IST DIE ANPASSUNG ---
        self.animated_widget = getattr(parent_window, animated_widget_name)
        self.toggle_button = getattr(parent_window, toggle_button_name)

        if not all([self.animated_widget, self.toggle_button]):
            raise ValueError("Eines oder mehrere Widgets konnten nicht im UI gefunden werden.")

        # Animationseinstellungen
        self.animation_duration = 2500 # in Millisekunden
        self.is_expanded = False  # Das Panel startet eingeklappt

        # Speichere die ursprüngliche Breite. Wir nehmen die sizeHint.
        self.expanded_width = self.animated_widget.sizeHint().width()

        # Stelle sicher, dass die Breite sinnvoll ist, falls sie 0 ist
        if self.expanded_width == 0:
            self.expanded_width = 650  # Setze einen Standardwert, falls sizeHint nicht ausreicht

        # Erstelle das Animations-Objekt
        self.animation = QPropertyAnimation(self.animated_widget, b"maximumWidth")
        self.animation.setDuration(self.animation_duration)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Signal des Buttons mit unserer Toggle-Funktion verbinden
        self.toggle_button.clicked.connect(self.toggle_animation)

        # Initialen Zustand setzen: Das rechte Widget ist "versteckt" (Breite 0)
        self.animated_widget.setMaximumWidth(0)

    def toggle_animation(self):
        """
        Starts the animation to either expand or collapse the panel.
        """
        start_value = self.animated_widget.width()

        if self.is_expanded:
            # --- Einklappen ---
            self.animation.setStartValue(start_value)
            self.animation.setEndValue(0)
            self.is_expanded = False
        else:
            # --- Ausklappen ---
            self.animation.setStartValue(start_value)
            self.animation.setEndValue(self.expanded_width)
            self.is_expanded = True

        self.animation.start()