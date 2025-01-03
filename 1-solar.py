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
    sun = CelestialBody("Sun", color=Color(1, 1, 0), scaleFactor=2, rotationSpeed=1)

    mercury = CelestialBody("Mercury",
                            color=Color(0.3, 0.3, 0.3),
                            scaleFactor=0.20,
                            translation=[1.45, 0, 0],
                            rotationSpeed=0,
                            revolutionSpeed=1.5,
                            revolvesAround=sun)

    venus = CelestialBody("Venus",
                          color=Color(0.9, 0.7, 0.5),
                          scaleFactor=0.4,
                          translation=[2.45, 0, 0],
                          rotationSpeed=0,
                          revolutionSpeed=0.75,
                          revolvesAround=sun)

    earth = CelestialBody("Earth",
                          color=Color(0, 0.5, 0.5),
                          scaleFactor=0.50,
                          translation=[4, 0, 0],
                          rotationSpeed=0,
                          revolutionSpeed=0.5,
                          revolvesAround=sun)

    moon = CelestialBody("Moon",
                         color=Color(0.8, 0.8, 0.8),
                         scaleFactor=0.15,
                         translation=[1.5, 0, 0],
                         rotationSpeed=0,
                         revolutionSpeed=2.5,
                         revolvesAround=earth)

    mars = CelestialBody("Mars",
                          color=Color(1, 0, 0),
                          scaleFactor=0.60,
                          translation=[6, 0, 0],
                          rotationSpeed=0,
                          revolutionSpeed=0.85,
                          revolvesAround=sun)

    # Create a scene
    scene = Scene()

    # Add objects to the scene
    scene.addObject(sun)
    scene.addObject(mercury)
    scene.addObject(venus)
    scene.addObject(earth)
    scene.addObject(moon)
    scene.addObject(mars)

    # Setup the scene
    scene.setup(program)


def update(dt, time):
    scene.draw(program, dt, time)

run("2DT904 - Programming assignment [Solar System]", init=init, update=update)
