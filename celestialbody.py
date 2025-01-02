from OpenGL.GL import *
from sphere import generateSphere
from attribute import Attribute
from color import Color
from matrix import Matrix
from abc import ABC, abstractmethod

class Renderable(ABC):
    @abstractmethod
    def upload(self, program):
        pass

    @abstractmethod
    def draw(self, program, dt, time):
        pass

class CelestialBody(Renderable):
    def __init__(self, name, scaleFactor=1, translation=[0,0,0], rotationSpeed=0,revolutionSpeed = 0,color = Color(1, 1, 1)):
        self.name = name
        self.scaleFactor = scaleFactor
        self.translation = translation
        self.rotationSpeed = rotationSpeed
        self.revolutionSpeed = revolutionSpeed
        self.color = color
        self.vao = glGenVertexArrays(1)

    def upload(self, program):
        glBindVertexArray(self.vao)

        self.vertices = generateSphere()
        positionAttributeSquare = Attribute("vec3", self.vertices)
        positionAttributeSquare.associateVariable(program, "position" )

        colorAttributeSquare = Attribute("vec3", [self.color.asArray()]*len(self.vertices))
        colorAttributeSquare.associateVariable(program, "vertexColor" )

    def draw(self, program, dt, time):
        speed = time * 0.3
        glBindVertexArray(self.vao)

        tansl_x, tansl_y, tansl_z = self.translation
        program.setUniformMat4('mModel', Matrix.makeRotationZ(2*speed*self.rotationSpeed) @ Matrix.rotation_matrix(speed * self.revolutionSpeed, [0,0,1]) @ Matrix.makeScale(self.scaleFactor) @ Matrix.makeTranslation(tansl_x, tansl_y, tansl_z))

        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices))
