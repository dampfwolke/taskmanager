# animation_handler.py

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QObject


class SidePanelAnimator(QObject):
    """
    Manages the slide animation for a side panel widget in a Qt application.

    This class handles the animation of a widget's maximumWidth property to create
    a smooth expand/collapse effect. It's designed to be used with a main window
    loaded from a .ui file.
    """

    def __init__(self, parent_window, animated_widget_name, toggle_button_name):
        """
        Initializes the animator.

        Args:
            parent_window: The main window instance containing the UI elements.
            animated_widget_name (str): The objectName of the widget to be animated.
            toggle_button_name (str): The objectName of the button that triggers the animation.
        """
        super().__init__(parent_window)

        # UI-Elemente aus dem übergeordneten Fenster holen
        self.animated_widget = getattr(parent_window.ui, animated_widget_name)
        self.toggle_button = getattr(parent_window.ui, toggle_button_name)

        if not all([self.animated_widget, self.toggle_button]):
            raise ValueError("Eines oder mehrere Widgets konnten nicht im UI gefunden werden.")

        # Animationseinstellungen
        self.animation_duration = 350  # in Millisekunden
        self.is_expanded = False  # Das Panel startet eingeklappt

        # Speichere die ursprüngliche Breite, die für die Expansion benötigt wird.
        # Wir nehmen die sizeHint, da sie oft eine gute "Wunschgröße" darstellt.
        self.expanded_width = self.animated_widget.sizeHint().width()

        # Erstelle das Animations-Objekt
        # Wir animieren die 'maximumWidth'-Eigenschaft
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
        if self.is_expanded:
            # --- Einklappen ---
            self.animation.setStartValue(self.expanded_width)
            self.animation.setEndValue(0)
            self.animation.start()
            self.is_expanded = False
        else:
            # --- Ausklappen ---
            self.animation.setStartValue(0)
            self.animation.setEndValue(self.expanded_width)
            self.animation.start()
            self.is_expanded = True