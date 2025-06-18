from PySide6.QtCore import (QPropertyAnimation, QEasingCurve, QRect,
                            QParallelAnimationGroup)
from PySide6.QtWidgets import QWidget


class SidePanelAnimator:
    """
    Animiert ein Panel zum Herein-/Herausgleiten und passt die Größe des
    Hauptfensters an, ohne das linke Layout zu verzerren.
    """

    def __init__(self, parent: QWidget, panel: QWidget, left_container: QWidget,
                 closed_width: int, open_width: int, duration: int = 350):
        self.parent = parent
        self.panel = panel
        self.left_container = left_container  # Das neue Widget für den linken Bereich
        self.is_open = False

        self.closed_width = closed_width
        self.open_width = open_width

        # ... (der Rest des __init__ bleibt exakt gleich) ...
        self.animation_group = QParallelAnimationGroup(parent)
        self.panel_animation = QPropertyAnimation(self.panel, b"geometry")
        self.panel_animation.setEasingCurve(QEasingCurve.Type.OutBack)  # Standardmäßig auf eine gute Kurve gesetzt
        self.panel_animation.setDuration(duration)
        self.window_animation = QPropertyAnimation(self.parent, b"minimumWidth")
        self.window_animation.setEasingCurve(QEasingCurve.Type.OutBack)
        self.window_animation.setDuration(duration)
        self.animation_group.addAnimation(self.panel_animation)
        self.animation_group.addAnimation(self.window_animation)
        self.animation_group.finished.connect(self._on_animation_finished)

    def toggle_panel(self):
        panel_width = self.panel.width()
        panel_height = self.panel.height()
        panel_y = self.panel.y()

        if self.is_open:
            # --- Panel SCHLIESSEN ---
            # Der linke Container behält seine feste Breite während des Schließens
            self.left_container.setFixedWidth(self.closed_width)

            start_geo = self.panel.geometry()
            end_geo = QRect(self.closed_width, start_geo.y(), panel_width, start_geo.height())

            self.window_animation.setStartValue(self.open_width)
            self.window_animation.setEndValue(self.closed_width)
        else:
            # --- Panel ÖFFNEN ---
            # HIER IST DER TRICK: Fixiere die Breite des linken Teils, bevor die Animation startet
            self.left_container.setFixedWidth(self.closed_width)

            self.panel.show()
            self.parent.setMinimumWidth(self.closed_width)

            start_geo = QRect(self.closed_width, panel_y, panel_width, panel_height)
            end_geo = QRect(self.open_width - panel_width, panel_y, panel_width, panel_height)

            self.window_animation.setStartValue(self.closed_width)
            self.window_animation.setEndValue(self.open_width)

        self.panel_animation.setStartValue(start_geo)
        self.panel_animation.setEndValue(end_geo)

        self.is_open = not self.is_open
        self.animation_group.start()

    def _on_animation_finished(self):
        final_width = self.open_width if self.is_open else self.closed_width

        # WICHTIG: Die Breitenbeschränkung wieder aufheben, damit das Fenster anpassungsfähig bleibt
        self.left_container.setMinimumSize(0, 0)
        self.left_container.setMaximumSize(16777215, 16777215)
        # Bessere Alternative, falls die obigen nicht funktionieren:
        # self.left_container.setFixedWidth(final_width) # Setzt es auf die finale Größe des linken Teils

        if not self.is_open:
            self.panel.hide()
            # Der linke Container sollte die volle Fensterbreite einnehmen
            self.left_container.setFixedWidth(final_width)

        self.parent.setFixedWidth(final_width)
        self.parent.setMinimumWidth(0)