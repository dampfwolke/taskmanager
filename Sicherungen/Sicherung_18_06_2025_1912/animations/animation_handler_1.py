# animations/animation_handler.py (JETZT WIRKLICH FINAL)

from PySide6.QtCore import (
    QObject,
    QPropertyAnimation,
    QEasingCurve,
    QParallelAnimationGroup,
    QAbstractAnimation,
    QRect,
    QSize  # <--- WICHTIGER IMPORT HINZUGEFÜGT
)
from PySide6.QtWidgets import QLayout


class SidePanelAnimator(QObject):
    """
    Verwaltet die Animation eines seitlichen Panels und die Größe des Hauptfensters.

    KERNFUNKTION: Deaktiviert temporär die automatische Größenanpassung des
    Layouts (`setSizeConstraint`), um einen Konflikt zwischen der Animation und dem
    Layout-Manager zu verhindern. Führt die Fenster- und Panel-Animation
    parallel für einen flüssigen Effekt aus.
    """

    def __init__(self, parent_window, animated_widget_name, toggle_button_name):
        super().__init__(parent_window)

        # --- Widgets und Layout referenzieren ---
        self.parent_window = parent_window
        self.animated_widget = getattr(parent_window, animated_widget_name)
        self.toggle_button = getattr(parent_window, toggle_button_name)

        self.main_layout = self.parent_window.centralWidget().layout()
        if not self.main_layout:
            raise RuntimeError("Das centralWidget hat keinen Layout-Manager. Animation nicht möglich.")

        self.original_size_constraint = self.main_layout.sizeConstraint()

        # --- Animationseinstellungen ---
        self.animation_duration = 1250
        self.easing_curve = QEasingCurve.Type.InOutCubic
        self.is_expanded = False

        # --- Breitenberechnung ---
        self.panel_target_width = self.animated_widget.maximumSize().width()
        self.collapsed_width = self.parent_window.width()
        self.expanded_width = self.collapsed_width + self.panel_target_width

        # --- Animationen erstellen ---
        self.panel_animation = QPropertyAnimation(self.animated_widget, b"maximumWidth")
        self.panel_animation.setDuration(self.animation_duration)
        self.panel_animation.setEasingCurve(self.easing_curve)

        self.window_animation = QPropertyAnimation(self.parent_window, b"geometry")
        self.window_animation.setDuration(self.animation_duration)
        self.window_animation.setEasingCurve(self.easing_curve)

        self.animation_group = QParallelAnimationGroup(self)
        self.animation_group.addAnimation(self.panel_animation)
        self.animation_group.addAnimation(self.window_animation)

        # --- Signale verbinden ---
        self.toggle_button.clicked.connect(self.toggle_animation)
        self.animation_group.finished.connect(self.on_animation_finished)

        # Initialen Zustand setzen
        self.animated_widget.setMaximumWidth(0)

    def toggle_animation(self):
        """
        Startet die Animation und deaktiviert vorher die Layout-Kontrolle.
        """
        if self.animation_group.state() == QAbstractAnimation.State.Running:
            return

        self.main_layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        current_geometry = self.parent_window.geometry()

        if self.is_expanded:
            # --- Ziel: ZUKLAPPEN ---
            target_panel_width = 0
            end_geometry = QRect(
                current_geometry.topLeft(),
                # *** KORREKTUR HIER: Explizit ein QSize-Objekt erstellen ***
                QSize(self.collapsed_width, current_geometry.height())
            )
        else:
            # --- Ziel: AUFKLAPPEN ---
            target_panel_width = self.panel_target_width
            end_geometry = QRect(
                current_geometry.topLeft(),
                # *** KORREKTUR HIER: Explizit ein QSize-Objekt erstellen ***
                QSize(self.expanded_width, current_geometry.height())
            )

        # Animationen mit Start- und Endwerten konfigurieren
        self.panel_animation.setStartValue(self.animated_widget.width())
        self.panel_animation.setEndValue(target_panel_width)

        self.window_animation.setStartValue(current_geometry)
        self.window_animation.setEndValue(end_geometry)

        # Zustand für den nächsten Klick umschalten
        self.is_expanded = not self.is_expanded

        # Animation starten
        self.animation_group.start()

    def on_animation_finished(self):
        """
        Wird aufgerufen, wenn die Animation beendet ist.
        Gibt dem Layout die Kontrolle über die Fenstergröße zurück.
        """
        self.main_layout.setSizeConstraint(self.original_size_constraint)

        if not self.is_expanded:
            self.parent_window.setMinimumSize(self.parent_window.sizeHint())