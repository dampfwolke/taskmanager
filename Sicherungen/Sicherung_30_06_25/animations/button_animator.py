# animations/button_animator.py (Version 6 - FINAL, mit QGraphicsColorizeEffect)

from PySide6.QtCore import QObject, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtWidgets import QPushButton, QGraphicsColorizeEffect
from PySide6.QtGui import QColor


class ButtonAnimator(QObject):
    """
    Fügt einer Liste von PushButtons einen dynamischen Animations-Effekt hinzu.
    Kombiniert eine Größen- und Farb-Animation für einen auffälligen Effekt.
    """

    def __init__(self, parent_window, button_names: list):
        super().__init__(parent_window)
        self.parent = parent_window
        self.handlers = []

        for button_name in button_names:
            try:
                button = getattr(self.parent, button_name)
                if isinstance(button, QPushButton):
                    # Erstelle für jeden Button einen eigenen Handler
                    handler = _ButtonAnimationHandler(button)
                    self.handlers.append(handler)
                else:
                    print(f"Warnung: '{button_name}' ist kein QPushButton.")
            except AttributeError:
                print(f"Warnung: Button '{button_name}' nicht gefunden.")


class _ButtonAnimationHandler(QObject):
    """
    Verwaltet die Animation für einen einzelnen Button.
    LÖSUNG: Verwendet einen QGraphicsColorizeEffect direkt auf dem Button,
    um Farbänderungen zu animieren, anstatt fehleranfällige Overlays zu verwenden.
    """

    def __init__(self, button: QPushButton):
        super().__init__(button)
        self.button = button

        # --- Der Colorize-Effekt ---
        # Dieser eine Effekt wird für das Abdunkeln UND das Aufhellen verwendet.
        self.colorize_effect = QGraphicsColorizeEffect(self)
        self.button.setGraphicsEffect(self.colorize_effect)
        # Initial ist der Effekt komplett deaktiviert (Stärke 0.0)
        self.colorize_effect.setStrength(0.0)

        # --- Animationen erstellen ---
        # Eine Animation für die Größe des Buttons
        self.geometry_animation = QPropertyAnimation(self.button, b"geometry")

        # Eine Animation für die Stärke des Farbeffekts
        self.color_animation = QPropertyAnimation(self.colorize_effect, b"strength")

        # --- Signale verbinden ---
        self.button.pressed.connect(self.animate_press)
        self.button.released.connect(self.animate_release)

    def animate_press(self):
        """ Drücken: Button wird kleiner und dunkler. """
        # Stoppe laufende Animationen, um Konflikte zu vermeiden
        self.geometry_animation.stop()
        self.color_animation.stop()

        # 1. Geometrie-Animation (hineindrücken)
        original_geo = self.button.geometry()
        offset = 3
        shrink = offset * 3

        pressed_geo = QRect(
            original_geo.x() + offset,
            original_geo.y() + offset,
            original_geo.width() - shrink,
            original_geo.height() - shrink
        )
        self.geometry_animation.setDuration(80)
        self.geometry_animation.setStartValue(original_geo)
        self.geometry_animation.setEndValue(pressed_geo)

        # 2. Farb-Animation (abdunkeln)
        self.colorize_effect.setColor(QColor("black"))  # Effektfarbe auf Schwarz setzen
        self.color_animation.setDuration(80)
        self.color_animation.setStartValue(0.0)
        self.color_animation.setEndValue(0.25)  # 25% Abdunkelung

        # Beide Animationen starten
        self.geometry_animation.start()
        self.color_animation.start()

    def animate_release(self):
        """ Loslassen: Federt zurück und leuchtet kurz auf. """
        # Stoppe laufende Animationen
        self.geometry_animation.stop()
        self.color_animation.stop()

        # 1. Geometrie-Animation (zurückfedern)
        offset = 2
        shrink = offset * 2
        original_geo = QRect(
            self.button.x() - offset,
            self.button.y() - offset,
            self.button.width() + shrink,
            self.button.height() + shrink
        )
        self.geometry_animation.setDuration(350)
        self.geometry_animation.setEasingCurve(QEasingCurve.Type.OutBack)
        self.geometry_animation.setStartValue(self.button.geometry())
        self.geometry_animation.setEndValue(original_geo)

        # 2. Farb-Animation (aufblitzen)
        self.colorize_effect.setColor(QColor("white"))  # Effektfarbe auf Weiß setzen
        self.color_animation.setDuration(400)
        self.color_animation.setStartValue(0.0)
        self.color_animation.setKeyValueAt(0.25, 0.3)  # Kurzer heller Blitz
        self.color_animation.setKeyValueAt(1.0, 0.0)  # Vollständiges Ausblenden

        # Beide Animationen starten
        self.geometry_animation.start()
        self.color_animation.start()