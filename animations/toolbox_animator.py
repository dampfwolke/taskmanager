from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QAbstractAnimation
from PySide6.QtWidgets import QToolBox


class ToolBoxAnimator:
    """
    Eine robuste Klasse zur Animation einer QToolBox, die versucht,
    Größenprobleme zu umgehen.
    """

    def __init__(self, toolbox: QToolBox, duration: int = 350):
        self.toolbox = toolbox
        self.duration = duration
        self.page_heights = {}

        print("--- Initializing ToolBoxAnimator ---")

        # Höhe jeder Seite beim Start ermitteln und speichern
        for i in range(self.toolbox.count()):
            page = self.toolbox.widget(i)
            height = 0

            # Versuch 1: sizeHint() der Seite
            hint_height = page.sizeHint().height()

            # Versuch 2 (oft besser): Höhe des Layouts der Seite abfragen
            layout_height = 0
            if page.layout() is not None:
                layout_height = page.layout().sizeHint().height()

            # Wir nehmen den größeren der beiden Werte
            height = max(hint_height, layout_height)

            if height == 0:
                print(
                    f"[WARNUNG] Seite {i} ('{self.toolbox.itemText(i)}'): Konnte keine Höhe > 0 ermitteln. Animation wird nicht funktionieren.")
                # Fallback auf einen festen Wert, damit wir überhaupt etwas sehen
                height = 150

            self.page_heights[i] = height
            print(
                f"Seite {i} ('{self.toolbox.itemText(i)}'): Hint={hint_height}, LayoutHint={layout_height}. Gespeicherte Höhe = {height}px")

        self.toolbox.currentChanged.connect(self.animate_to_page)
        self.set_initial_state()
        print("--- ToolBoxAnimator Initialized ---")

    def set_initial_state(self):
        """Setzt die Höhen beim Start, ohne Animation."""
        current_index = self.toolbox.currentIndex()
        for i in range(self.toolbox.count()):
            page = self.toolbox.widget(i)
            if i == current_index:
                page.setMaximumHeight(self.page_heights.get(i, 500))
            else:
                page.setMaximumHeight(0)

    def animate_to_page(self, index: int):
        """Animiert beim Klick auf einen neuen Tab."""
        print(f"\nAnimating to page {index} ('{self.toolbox.itemText(index)}')")

        # Zuerst alle anderen Panels schließen
        for i in range(self.toolbox.count()):
            if i != index:
                page_to_close = self.toolbox.widget(i)
                # Nur schließen, wenn es nicht schon geschlossen ist
                if page_to_close.height() > 0:
                    # Hier könnten wir auch eine Schließ-Animation einbauen,
                    # aber ein sofortiges Schließen ist oft klarer.
                    page_to_close.setMaximumHeight(0)

        # Dann das Ziel-Panel öffnen
        page_to_open = self.toolbox.widget(index)
        target_height = self.page_heights.get(index, 150)

        animation = QPropertyAnimation(page_to_open, b"maximumHeight")
        animation.setDuration(self.duration)
        animation.setStartValue(page_to_open.height())  # Aktuelle Höhe (0)
        animation.setEndValue(target_height)  # Gespeicherte Zielhöhe
        animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        print(f"  -> Animating '{page_to_open.objectName()}' from {page_to_open.height()}px to {target_height}px")

        animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)