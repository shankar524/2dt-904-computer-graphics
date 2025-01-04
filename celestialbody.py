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
    def __init__(self, name, scaleFactor=1, translation=[0,0,0], rotationSpeed=0, revolutionSpeed=0, color=Color(1, 1, 1), ambience=0, diffuse=0.5, specular=1, shininess=0.0005, revolvesAround=None, emitsLight=False, variationPercentage=0, variationColors=[Color(1, 1, 1), Color(0, 0, 0)]):
        self.name = name
        self.scaleFactor = scaleFactor
        self.translation = translation
        self.rotationSpeed = rotationSpeed
        self.revolutionSpeed = revolutionSpeed
        self.color = color
        self.vao = glGenVertexArrays(1)
        self.revolvesAround = revolvesAround
        self.ambience = ambience
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.emitsLight = emitsLight
        self.variationPercentage = variationPercentage
        self.variationColors = variationColors
        self.translationMatrix = np.identity(4, dtype=np.float32)

    def generateColorVariation(self):

        # Calculate the number of elements for each color
        totalVertices = len(self.vertices)
        otherColorsCount = int(totalVertices * self.variationPercentage)
        planetColorCount = totalVertices - otherColorsCount

        # Create arrays for each color
        planetColors = np.array([self.color] * planetColorCount)
        variations = self.variationColors

        # Randomly select from other colors to fill the remaining
        otherColorsArray = np.tile(variations, otherColorsCount // len(variations) + 1)[:otherColorsCount]

        # Combine the arrays
        colorArray = np.concatenate((planetColors, otherColorsArray))

        # Shuffle the array to mix the colors
        np.random.shuffle(colorArray)

        return [color.asArray() for color in colorArray]

    def upload(self, program):
        glBindVertexArray(self.vao)

        self.vertices = generateSphere(radiusSegments=64,heightSegments=64)
        positionAttributeSquare = Attribute("vec3", self.vertices)
        positionAttributeSquare.associateVariable(program, "position" )

        colorAttributeSquare = Attribute("vec3", self.generateColorVariation())
        colorAttributeSquare.associateVariable(program, "vertexColor" )

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

        program.setUniformFloat('ambientStrength', self.ambience)
        program.setUniformFloat('diffuseStrength', self.diffuse)
        program.setUniformFloat('specularStrength', self.specular)
        program.setUniformFloat('shininess', self.shininess)
        program.setUniformBoolean('emitsLight', self.emitsLight)
        program.setUniformMat4('mModel', self.translationMatrix)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices))
