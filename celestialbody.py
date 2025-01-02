from OpenGL.GL import *
from sphere import generateSphere
from attribute import Attribute
from color import Color

class CelestialBody:
    def __init__(self, name, radius=32, height=32, color = Color(1, 1, 1)):
        self.name = name
        self.radius = radius
        self.height = height
        self.color = color

    def setMoon(self, moon):
        self.moon = moon

    def upload(self, program):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vertices = generateSphere(self.radius, self.height)
        positionAttributeSquare = Attribute("vec3", self.vertices)
        positionAttributeSquare.associateVariable(program, "position" )

        colorAttributeSquare = Attribute("vec3", [self.color.asArray()]*len(self.vertices))
        colorAttributeSquare.associateVariable(program, "vertexColor" )

    def vertexCount(self):
        return len(self.vertices)