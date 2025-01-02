from OpenGL.GL import *
from celestialbody import CelestialBody
from color import Color
from app import run, readFile
from glslprogram import Program
from scene import Scene

vsCode = readFile('./1-vs.glsl')
fsCode = readFile('./1-fs.glsl')


def init():
    global program
    global scene

    program = Program(vsCode, fsCode)
    program.use()

    print("Create celestial bodies")
    # Create celestial bodies
    sun = CelestialBody("Sun", color=Color(1, 1, 0), scaleFactor=1.5, rotationSpeed=1)

    earth = CelestialBody("Earth",
                          color=Color(0, 0, 1),
                          scaleFactor=0.5,
                          translation=[6.5, 0, 0],
                          rotationSpeed=2,
                          revolutionSpeed=1)

    # Create a scene
    scene = Scene()

    # Add objects to the scene
    scene.addObject(sun)
    scene.addObject(earth)

    # Setup the scene
    scene.setup(program)


def update(dt, time):
    scene.draw(program, dt, time)

run("2DT904 - Programming assignment [Solar System]", init=init, update=update)
