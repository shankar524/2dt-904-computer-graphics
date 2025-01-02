from OpenGL.GL import *
from celestialbody import CelestialBody
from color import Color
from app import run, readFile
from glslprogram import Program
from matrix import Matrix

vsCode = readFile('./vs.glsl')
fsCode = readFile('./fs.glsl')

class Light:
    def __init__(self, direction = [0,0,0], color = Color(1,1,1)):
        self.direction = direction

class Scene:
    def __init__(self, cameraPos = [0,0,-20], light=Light()):
        self.cameraPos = cameraPos
        self.light = light


def init():
    global program
    global sun, earth

    program = Program(vsCode, fsCode)
    program.use()

    sun = CelestialBody("Sun", color=Color(1, 1, 0))
    sun.upload(program)

    earth = CelestialBody("Earth", color=Color(0, 0, 1))
    earth.upload(program)

    projection = Matrix.makePerspective()
    invCameraPos = Matrix.makeTranslation(0, 0, -20)
    mProjView = projection @ invCameraPos

    program.setUniformMat4('mProjView', mProjView)

    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)


def update(dt, time):
    speed = time * 0.3
    glClear(GL_DEPTH_BUFFER_BIT)
    glClear(GL_COLOR_BUFFER_BIT)
    #glClear(GL_DEPTH_BUFFER_BIT)
    glBindVertexArray(sun.vao)
    #program.setUniformMat4('mModel', Matrix.makeScale(0.95) @ Matrix.makeRotationY(speed) @ Matrix.makeRotationZ(2*speed))
    #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    program.setUniformMat4('mModel', Matrix.makeScale(1.25))
    glDrawArrays(GL_TRIANGLES, 0, sun.vertexCount())

    glBindVertexArray(earth.vao)
    program.setUniformMat4('mModel', Matrix.rotation_matrix(2*speed, [0,0,1]) @ Matrix.makeScale(0.5) @ Matrix.makeTranslation(6.5, 0, 0))
    #glClear(GL_DEPTH_BUFFER_BIT)

    glDrawArrays(GL_TRIANGLES, 0, earth.vertexCount())
    # glClear(GL_DEPTH_BUFFER_BIT)
    # glClear(GL_COLOR_BUFFER_BIT)


run("2DT904 - Programming assignment[Solar System]", init=init, update=update)