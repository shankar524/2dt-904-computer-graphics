from OpenGL.GL import *
from sphere import generateSphere
from attribute import Attribute
from color import Color
from matrix import Matrix
from abc import ABC, abstractmethod
import numpy as np

class Renderable(ABC):
    @abstractmethod
    def upload(self, program):
        pass

    @abstractmethod
    def draw(self, program, dt, time):
        pass

class CelestialBody(Renderable):
    def __init__(self, name, scaleFactor=1, translation=[0,0,0], rotationSpeed=0, revolutionSpeed = 0, color = Color(1, 1, 1), revolvesAround=None):
        self.name = name
        self.scaleFactor = scaleFactor
        self.translation = translation
        self.rotationSpeed = rotationSpeed
        self.revolutionSpeed = revolutionSpeed
        self.color = color
        self.vao = glGenVertexArrays(1)
        self.revolvesAround = revolvesAround
        self.translationMatrix = np.identity(4, dtype=np.float32)

    def upload(self, program):
        glBindVertexArray(self.vao)

        self.vertices = generateSphere()
        positionAttributeSquare = Attribute("vec3", self.vertices)
        positionAttributeSquare.associateVariable(program, "position" )

        colorAttributeSquare = Attribute("vec3", [self.color.asArray()]*len(self.vertices))
        colorAttributeSquare.associateVariable(program, "vertexColor" )

    def draw2(self, program, dt, time):
        glBindVertexArray(self.vao)

        tansl_x, tansl_y, tansl_z = self.translation
        if self.revolvesAround is not None:
            parent_matrix = self.revolvesAround.translationMatrix
        else:
            parent_matrix = np.identity(4, dtype=np.float32)

        self.translationMatrix = (
            parent_matrix @
            Matrix.makeRotationZ(time * self.rotationSpeed) @
            Matrix.rotation_matrix(time * self.revolutionSpeed, [0, 0, 1]) @
            Matrix.makeTranslation(tansl_x, tansl_y, tansl_z)
        )

        program.setUniformMat4('mModel',  Matrix.makeScale(self.scaleFactor) @ self.translationMatrix)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices))

    def draw(self, program, dt, time):
        glBindVertexArray(self.vao)

        tansl_x, tansl_y, tansl_z = self.translation
        if self.revolvesAround is None:
            # Calculate the model matrix for celestial bodies that do not revolve around another body
            self.translationMatrix = (
                Matrix.makeRotationZ(time * self.rotationSpeed) @
                Matrix.rotation_matrix(time * self.revolutionSpeed, [0, 0, 1]) @
                Matrix.makeScale(self.scaleFactor) @
                Matrix.makeTranslation(tansl_x, tansl_y, tansl_z)
            )
        else:
            # Calculate the model matrix for celestial bodies that revolve around another body
            parent_matrix = self.revolvesAround.translationMatrix
            self.translationMatrix = (
                parent_matrix @
                Matrix.rotation_matrix(time * self.revolutionSpeed, [0, 0, 1]) @
                Matrix.makeTranslation(tansl_x, tansl_y, tansl_z) @
                Matrix.makeRotationZ(time * self.rotationSpeed) @
                Matrix.makeScale(self.scaleFactor)
            )

        program.setUniformMat4('mModel', self.translationMatrix)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices))
