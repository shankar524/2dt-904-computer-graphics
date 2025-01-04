from OpenGL.GL import *
from celestialbody import CelestialBody
from color import Color
from app import run, readFile
from glslprogram import Program
from scene import Scene
from light import Light
from camera import Camera

vsCode = readFile('./1-vs.glsl')
fsCode = readFile('./1-fs.glsl')


def init():
    global program
    global scene

    # Load shaders and bind to program
    program = Program(vsCode, fsCode)
    program.use()

    # Create celestial bodies
    sun = CelestialBody("Sun",
                        color=Color(1, 1, 0),
                        scaleFactor=2,
                        emitsLight=True)

    mercury = CelestialBody("Mercury",
                            color=Color(0.3, 0.3, 0.3),
                            scaleFactor=0.20,
                            translation=[1.45, 0, 0],
                            rotationSpeed=0.5,
                            revolutionSpeed=1.5,
                            variationPercentage=0.05,
                            revolvesAround=sun)

    venus = CelestialBody("Venus",
                          color=Color(0.9, 0.7, 0.5),
                          scaleFactor=0.4,
                          translation=[2.45, 0, 0],
                          rotationSpeed=0.75,
                          revolutionSpeed=0.75,
                          variationPercentage=0.15,
                          variationColors=[Color(0, 1, 0), Color(1, 1, 0)],
                          revolvesAround=sun)

    earth = CelestialBody("Earth",
                          color=Color(0, 0.15, 0.95),
                          scaleFactor=0.50,
                          translation=[4, 0, 0],
                          rotationSpeed=0.35,
                          revolutionSpeed=0.5,
                          variationPercentage=0.45,
                          variationColors=[Color(0, 1, 0)],
                          revolvesAround=sun)

    moon = CelestialBody("Moon",
                         color=Color(0.8, 0.8, 0.8),
                         scaleFactor=0.25,
                         translation=[1.5, 0, 0],
                         rotationSpeed=0.1,
                         revolutionSpeed=2.5,
                         shininess=64.0,
                         ambience=2,
                         variationPercentage=0.35,
                         variationColors=[Color(0, 0, 0)],
                         revolvesAround=earth)

    mars = CelestialBody("Mars",
                          color=Color(1, 0, 0),
                          scaleFactor=0.55,
                          translation=[6, 0, 0],
                          rotationSpeed=0.8,
                          revolutionSpeed=0.85,
                          ambience=0.75,
                          variationPercentage=0.15,
                          variationColors=[Color(.7, .2, .8), Color(.5, .5, .5)],
                          revolvesAround=sun)

    # Create a scene
    light=Light(position=sun.translation, color=Color(1, 1, 1))
    camera=Camera(position=[0, 0, -25])
    scene = Scene(light=light, camera=camera)

    # Add render-able objects to the scene
    scene.addObject(sun)
    scene.addObject(mercury)
    scene.addObject(venus)
    scene.addObject(earth)
    scene.addObject(moon)
    scene.addObject(mars)

    # Setup the scene
    scene.setup(program)


def update(dt, time):
    # Draw the scene
    scene.draw(program, dt, time)

run("2DT904 - Programming assignment [Solar System]", init=init, update=update)
