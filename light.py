from color import Color
from position import Position

class Light:
    def __init__(self, position = Position(), color = Color(1,1,1)):
        self.position = position
        self.color = color

    def __str__(self):
        return f'Light({self.position}, {self.color})'
