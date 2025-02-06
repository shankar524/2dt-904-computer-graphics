from celestialbody import Renderable
from attribute import Attribute

from OpenGL.GL import *

# Form a given point this should render a quad enclosing the point
class Quad(Renderable):
    def __init__(self, x, y, weight, length=0.1):
        self.x = x
        self.y = y
        # Prevent weight from being too small
        self.weight = max(weight, 0.025)
        self.length = length
        self.vao = glGenVertexArrays(1)

    def upload(self, program):
        glBindVertexArray(self.vao)

        half_length = (self.length / 2) * self.weight

        p1 = (self.x - half_length, self.y + half_length) # Top-left vertex
        p2 = (self.x + half_length, self.y + half_length) # Top-right vertex
        p3 = (self.x + half_length, self.y - half_length) # Bottom-right vertex
        p4 = (self.x - half_length, self.y - half_length) # Bottom-left vertex

        self.vertices = [p1, p2, p3, p3, p1, p4, p4, p2, p1, p2, p4, p3]
        vertexAttribute = Attribute("vec2", self.vertices)
        vertexAttribute.associateVariable(program, "position")

    def draw(self, program, dt, time):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices))

    def __str__(self):
        return f'Quad [{self.x}, {self.y}], weight: {self.weight}, length: {self.length}]'
