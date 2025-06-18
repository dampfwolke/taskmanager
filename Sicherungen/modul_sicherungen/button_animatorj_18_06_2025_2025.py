# animations/button_animator.py

from PySide6.QtCore import QObject, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtWidgets import QPushButton


class ButtonAnimator(QObject):
    """
    Fügt einer Liste von PushButtons einen 'Hineindrücken'-Animationseffekt hinzu.

    Verwendet die 'pressed' und 'released' Signale, um die Animation zu steuern.
    Jeder Button bekommt seinen eigenen kleinen Animations-Handler.
    """

    def __init__(self, parent_window, button_names: list):
        super().__init__(parent_window)
        self.parent = parent_window
        self.handlers = []

        for button_name in button_names:
            try:
                button = getattr(self.parent, button_name)
                if isinstance(button, QPushButton):
                    # Erstelle für jeden Button einen eigenen Handler, der sich
                    # um dessen Animation kümmert.
                    handler = _ButtonAnimationHandler(button)
                    self.handlers.append(handler)
                else:
                    print(f"Warnung: '{button_name}' ist kein QPushButton und wird ignoriert.")
            except AttributeError:
                print(f"Warnung: Button mit dem Namen '{button_name}' nicht gefunden.")


class _ButtonAnimationHandler(QObject):
    """
    Ein interner Helfer, der die Animation für einen einzelnen Button verwaltet.
    """

    def __init__(self, button: QPushButton):
        super().__init__(button)
        self.button = button

        # Speichere die ursprüngliche Geometrie, um immer dorthin zurückzukehren
        self.original_geometry = self.button.geometry()

        # --- Animationen erstellen ---

        # Animation für das Hineindrücken (sehr schnell)
        self.press_animation = QPropertyAnimation(self.button, b"geometry")
        self.press_animation.setDuration(150)  # Sehr kurze Dauer
        self.press_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Animation für das Loslassen (mit einem leichten "Bounce"-Effekt)
        self.release_animation = QPropertyAnimation(self.button, b"geometry")
        self.release_animation.setDuration(150)
        self.release_animation.setEasingCurve(QEasingCurve.Type.OutBack)  # Schöner Federeffekt

        # --- Signale verbinden ---
        self.button.pressed.connect(self.animate_press)
        self.button.released.connect(self.animate_release)

    def animate_press(self):
        """ Startet die Animation, die das Hineindrücken simuliert. """
        # Wir müssen die originale Geometrie bei jedem Klick neu abfragen,
        # falls sich das Fenster seit dem Start geändert hat.
        self.original_geometry = self.button.geometry()

        # Ziel: 1 Pixel nach rechts/unten, und 2 Pixel kleiner in Breite/Höhe
        pressed_geometry = QRect(
            self.original_geometry.x() + 1,
            self.original_geometry.y() + 1,
            self.original_geometry.width() - 2,
            self.original_geometry.height() - 2
        )

        self.press_animation.setStartValue(self.original_geometry)
        self.press_animation.setEndValue(pressed_geometry)
        self.press_animation.start()

    def animate_release(self):
        """ Startet die Animation, die das Zurückfedern simuliert. """
        # Start ist die aktuell "gedrückte" Position
        start_geometry = self.button.geometry()

        # Ziel ist immer die ursprüngliche, ungedrückte Position
        self.release_animation.setStartValue(start_geometry)
        self.release_animation.setEndValue(self.original_geometry)
        self.release_animation.start()