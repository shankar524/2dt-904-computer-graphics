from OpenGL.GL import *
from sphere import generateSphere
from attribute import Attribute
from color import Color
from position import Position
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
    def __init__(self, name, scaleFactor=1, translation=Position(), rotationSpeed=0, revolutionSpeed=0, color=Color(1, 1, 1), ambience=0.15, diffuse=0.6, specular=1, shininess=0.5, revolvesAround=None, emitsLight=False, variationPercentage=0, variationColors=[Color(1, 1, 1), Color(0, 0, 0)]):
        self.name = name
        self.scaleFactor = scaleFactor
        self.translation = translation
        self.rotationSpeed = rotationSpeed
        self.revolutionSpeed = revolutionSpeed
        self.color = color
        self.revolvesAround = revolvesAround
        self.ambience = ambience
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.emitsLight = emitsLight
        self.variationPercentage = variationPercentage
        self.variationColors = variationColors

        self.translationMatrix = np.identity(4, dtype=np.float32)
        self.vao = glGenVertexArrays(1)

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

        self.vertices = generateSphere(radiusSegments=64, heightSegments=64)
        vertexAttribute = Attribute("vec3", self.vertices)
        vertexAttribute.associateVariable(program, "position" )

        colorAttribute = Attribute("vec3", self.generateColorVariation())
        colorAttribute.associateVariable(program, "vertexColor" )

    def draw(self, program, dt, time):
        glBindVertexArray(self.vao)

        baseTransformation = np.identity(4, dtype=np.float32)
        revolution_pivot = [0, 0, 1] # Default pivot is the z-axis

        if self.revolvesAround is not None:
            baseTransformation = self.revolvesAround.translationMatrix

        self.translationMatrix = (
            baseTransformation @
            Matrix.rotation_matrix(time * self.revolutionSpeed, revolution_pivot) @
            Matrix.makeTranslation(self.translation.x, self.translation.y, self.translation.z) @
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
