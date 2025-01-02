from color import Color;

class Light:
    def __init__(self, position = [0,0,0], color = Color(1,1,1)):
        self.position = position
        self.color = color

    def __str__(self):
        return f'Light({self.position}, {self.color})'
