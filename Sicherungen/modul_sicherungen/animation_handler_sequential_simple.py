# animations/animation_handler_sequential_simple.py

from PySide6.QtCore import QObject, QPropertyAnimation, QEasingCurve, QAbstractAnimation


class SidePanelAnimatorSequentialSimple(QObject):
    """
    Führt eine EINFACHE SEQUENTIELLE Animation aus.
    - Animiert NUR das Panel (gleitet sanft auf/zu).
    - Das Fenster wird vom Layout-Manager automatisch und sofort angepasst.
    Diese Methode ist sehr stabil und vermeidet Konflikte.
    """

    def __init__(self, parent_window, animated_widget_name, toggle_button_name):
        super().__init__(parent_window)
        self.parent_window = parent_window
        self.animated_widget = getattr(parent_window, animated_widget_name)
        self.toggle_button = getattr(parent_window, toggle_button_name)

        self.animation_duration = 1600
        self.easing_curve = QEasingCurve.Type.InOutCubic
        self.is_expanded = False
        self.panel_target_width = self.animated_widget.maximumSize().width()

        self.panel_animation = QPropertyAnimation(self.animated_widget, b"maximumWidth")
        self.panel_animation.setDuration(self.animation_duration)
        self.panel_animation.setEasingCurve(self.easing_curve)

        self.toggle_button.clicked.connect(self.toggle_animation)
        self.animated_widget.setMaximumWidth(0)

    def toggle_animation(self):
        if self.panel_animation.state() == QAbstractAnimation.State.Running:
            return

        start_width = self.animated_widget.width()
        if self.is_expanded:
            end_width = 0
        else:
            end_width = self.panel_target_width

        self.panel_animation.setStartValue(start_width)
        self.panel_animation.setEndValue(end_width)

        self.is_expanded = not self.is_expanded
        self.panel_animation.start()