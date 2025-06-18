# animations/animation_handler_2.py (FINAL - mit Stretch-Faktor)

from PySide6.QtCore import (
    QObject,
    QPropertyAnimation,
    QEasingCurve,
    QSequentialAnimationGroup,
    QAbstractAnimation,
    QRect,
    QSize
)
from PySide6.QtWidgets import QLayout


class SidePanelAnimatorSequential(QObject):
    """
    Verwaltet eine SEQUENZIELLE, zweistufige Animation für ein seitliches Panel.

    FINALE VERSION: Kombiniert drei Techniken für eine robuste Funktion:
    1. Lazy Initialization: Berechnet Breiten erst bei Bedarf.
    2. setSizeConstraint: Deaktiviert Layout-Kontrolle während der Animation.
    3. setStretch: Weist dem animierten Widget den Expansionsraum zu.
    """

    def __init__(self, parent_window, animated_widget_name, toggle_button_name):
        super().__init__(parent_window)

        # --- Referenzen speichern ---
        self.parent_window = parent_window
        self.animated_widget = getattr(parent_window, animated_widget_name)
        self.toggle_button = getattr(parent_window, toggle_button_name)

        self.main_layout = self.parent_window.centralWidget().layout()
        if not self.main_layout:
            raise RuntimeError("Das centralWidget hat keinen Layout-Manager. Animation nicht möglich.")

        # *** DER ENTSCHEIDENDE NEUE TEIL ***
        # Wir weisen dem Layout Anweisungen für die Größenverteilung zu.
        # Das linke Widget (Index 0) soll seine Größe behalten (Stretch 0).
        # Das rechte, animierte Widget (Index 1) soll allen neuen Platz bekommen (Stretch 1).
        self.main_layout.setStretch(0, 0)
        self.main_layout.setStretch(1, 1)

        self.original_size_constraint = self.main_layout.sizeConstraint()

        # --- Animationseinstellungen ---
        self.animation_duration_part = 1250
        self.easing_curve = QEasingCurve.Type.InOutCubic
        self.is_expanded = False

        # --- Breitenberechnung (Lazy Initialization) ---
        self.panel_target_width = self.animated_widget.maximumSize().width()
        self.collapsed_width = None
        self.expanded_width = None

        # --- Einzelne Animationen erstellen ---
        self.panel_animation = QPropertyAnimation(self.animated_widget, b"maximumWidth")
        self.panel_animation.setDuration(self.animation_duration_part)
        self.panel_animation.setEasingCurve(self.easing_curve)

        self.window_animation = QPropertyAnimation(self.parent_window, b"geometry")
        self.window_animation.setDuration(self.animation_duration_part)
        self.window_animation.setEasingCurve(self.easing_curve)

        # --- SEQUENZIELLE Animationsgruppen ---
        self.expand_group = QSequentialAnimationGroup(self)
        self.expand_group.addAnimation(self.window_animation)
        self.expand_group.addAnimation(self.panel_animation)

        self.collapse_group = QSequentialAnimationGroup(self)
        self.collapse_group.addAnimation(self.panel_animation)
        self.collapse_group.addAnimation(self.window_animation)

        # --- Signale verbinden ---
        self.toggle_button.clicked.connect(self.toggle_animation)
        self.expand_group.finished.connect(self.on_animation_finished)
        self.collapse_group.finished.connect(self.on_animation_finished)

        # Initialen Zustand setzen
        self.animated_widget.setMaximumWidth(0)

    def toggle_animation(self):
        """ Startet die entsprechende Animationssequenz. """
        if self.collapsed_width is None:
            self.collapsed_width = self.parent_window.width()
            self.expanded_width = self.collapsed_width + self.panel_target_width

        if self.expand_group.state() == QAbstractAnimation.State.Running or \
                self.collapse_group.state() == QAbstractAnimation.State.Running:
            return

        self.main_layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        current_geometry = self.parent_window.geometry()

        if self.is_expanded:
            self.panel_animation.setStartValue(self.animated_widget.width())
            self.panel_animation.setEndValue(0)
            end_geometry = QRect(current_geometry.topLeft(), QSize(self.collapsed_width, current_geometry.height()))
            self.window_animation.setStartValue(current_geometry)
            self.window_animation.setEndValue(end_geometry)
            self.collapse_group.start()
        else:
            end_geometry = QRect(current_geometry.topLeft(), QSize(self.expanded_width, current_geometry.height()))
            self.window_animation.setStartValue(current_geometry)
            self.window_animation.setEndValue(end_geometry)
            self.panel_animation.setStartValue(0)
            self.panel_animation.setEndValue(self.panel_target_width)
            self.expand_group.start()

        self.is_expanded = not self.is_expanded

    def on_animation_finished(self):
        """ Wird aufgerufen, wenn eine der Animationssequenzen beendet ist. """
        self.main_layout.setSizeConstraint(self.original_size_constraint)
        if not self.is_expanded:
            self.parent_window.setMinimumSize(self.parent_window.sizeHint())