# animations/animation_handler.py (FINAL - mit robuster Zustandslogik)

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QObject, QParallelAnimationGroup


class SidePanelAnimator(QObject):
    """
    Manages the slide animation for a side panel widget and resizes the main window accordingly.
    Uses fixed target widths for the window to prevent cumulative resizing errors.
    """

    def __init__(self, parent_window, animated_widget_name, toggle_button_name):
        super().__init__(parent_window)

        self.animated_widget = getattr(parent_window, animated_widget_name)
        self.toggle_button = getattr(parent_window, toggle_button_name)

        # Animationseinstellungen
        self.animation_duration = 1250
        self.easing_curve = QEasingCurve.Type.InOutCubic
        self.is_expanded = False

        # Breite des Panels, um das wir erweitern wollen
        self.panel_width_delta = self.animated_widget.sizeHint().width()
        if self.panel_width_delta == 0:
            self.panel_width_delta = 300

        # --- NEUE, ROBUSTE LOGIK: Feste Zielgrößen speichern ---
        # Speichere die Startbreite des Fensters als "eingeklappten" Zustand
        self.collapsed_window_width = parent_window.width()
        # Berechne die Zielbreite für den "ausgeklappten" Zustand
        self.expanded_window_width = self.collapsed_window_width + self.panel_width_delta

        # Animationen erstellen
        self.panel_animation = QPropertyAnimation(self.animated_widget, b"maximumWidth")
        # self.window_animation = QPropertyAnimation(parent_window, b"minimumWidth")

        self.window_animation = QPropertyAnimation(parent_window, b"windowWidth")

        self.panel_animation.setDuration(self.animation_duration)
        self.panel_animation.setEasingCurve(self.easing_curve)
        self.window_animation.setDuration(self.animation_duration)
        self.window_animation.setEasingCurve(self.easing_curve)

        # Gruppe für parallele Animationen erstellen
        self.animation_group = QParallelAnimationGroup(self)
        self.animation_group.addAnimation(self.panel_animation)
        self.animation_group.addAnimation(self.window_animation)

        # Signal verbinden
        self.toggle_button.clicked.connect(self.toggle_animation)

        # Initialen Zustand setzen
        self.animated_widget.setMaximumWidth(0)

    def toggle_animation(self):
        """
        Toggles the panel's visibility by animating between fixed window and panel sizes.
        """
        # Aktuelle Breiten zum Start der Animation holen
        current_panel_width = self.animated_widget.width()
        current_window_width = self.parent().width()

        if self.is_expanded:
            # --- Ziel: Einklappen ---
            # Setze die Zielbreiten auf die gespeicherten "eingeklappten" Werte
            target_panel_width = 0
            target_window_width = self.collapsed_window_width
        else:
            # --- Ziel: Ausklappen ---
            # Setze die Zielbreiten auf die gespeicherten "ausgeklappten" Werte
            target_panel_width = self.panel_width_delta
            target_window_width = self.expanded_window_width

        # Setze die Start- und Endwerte für die Animationen
        self.panel_animation.setStartValue(current_panel_width)
        self.panel_animation.setEndValue(target_panel_width)

        self.window_animation.setStartValue(current_window_width)
        self.window_animation.setEndValue(target_window_width)

        # Zustand für den nächsten Klick umschalten
        self.is_expanded = not self.is_expanded

        self.animation_group.start()