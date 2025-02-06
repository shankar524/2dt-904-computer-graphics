from position import Position

class Camera:
    def __init__(self, position = Position(0, 0, -25), angleOfView=60, aspectRatio=1, near=0.1, far=1000):
        self.position = position
        self.angleOfView = angleOfView
        self.aspectRatio = aspectRatio
        self.near = near
        self.far = far

    def __str__(self):
        return f'Camera({self.position}, {self.angleOfView}, {self.aspectRatio}, {self.near}, {self.far})'
