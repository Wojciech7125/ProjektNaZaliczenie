from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class BackgroundWidget(Widget):
    """Widget do rysowania tła"""

    def __init__(self, bg_color="#022831", **kwargs):
        super().__init__(**kwargs)

        # Konwertuj hex na RGB
        self.bg_color = self.hex_to_rgb(bg_color)

        # Narysuj tło
        self.bind(size=self.update_bg, pos=self.update_bg)

        with self.canvas:  # Zmienione z canvas.before na canvas
            Color(*self.bg_color, 1)  # RGBA
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def hex_to_rgb(self, hex_color):
        """Konwertuj hex na RGB (0-1)"""
        hex_color = hex_color.lstrip('#')
        return [int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]

    def update_bg(self, *args):
        """Aktualizuj rozmiar tła"""
        self.rect.pos = self.pos
        self.rect.size = self.size