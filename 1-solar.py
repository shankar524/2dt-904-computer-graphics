from OpenGL.GL import *
from celestialbody import CelestialBody
from color import Color
from app import run, readFile
from glslprogram import Program
from scene import Scene
from light import Light
from camera import Camera
from position import Position

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
                        variationPercentage=0.05,
                        variationColors=[Color(0, 0, 0), Color(1, 0, 0)],
                        rotationSpeed=0.45,
                        emitsLight=True)

    mercury = CelestialBody("Mercury",
                            color=Color(0.3, 0.3, 0.3),
                            scaleFactor=0.25,
                            translation=Position(1.65, 0, 0),
                            rotationSpeed=0.0045,
                            revolutionSpeed=0.75,
                            variationPercentage=0.25,
                            variationColors=[Color(1.0, 0.84, 0.0) , Color(0.95, 0.90, 0.0)],
                            ambience=0.45,
                            shininess=1,
                            revolvesAround=sun)

    venus = CelestialBody("Venus",
                          color=Color(0.9, 0.7, 0.5),
                          scaleFactor=0.4,
                          translation=Position(2.65, 0, 0),
                          rotationSpeed=0.065,
                          revolutionSpeed=0.35,
                          variationPercentage=0.65,
                          variationColors=[Color(0.9, 0.7, 0.5), Color(1.0, 1.0, 1.0), Color(1.0, 0, 0)],
                          revolvesAround=sun)

    earth = CelestialBody("Earth",
                          color=Color(0.0, 1.0, 0.0),
                          scaleFactor=0.50,
                          translation=Position(4.2, 0, 0),
                          rotationSpeed=0.0025,
                          revolutionSpeed=0.25,
                          variationPercentage=0.45,
                          variationColors=[Color(0.0, 0.5, 1.0), Color(1.0, 1.0, 1.0)],
                          revolvesAround=sun)

    moon = CelestialBody("Moon",
                         color=Color(0.8, 0.8, 0.8),
                         scaleFactor=0.3,
                         translation=Position(1.75, 0, 0),
                         rotationSpeed=0.005,
                         revolutionSpeed=1.5,
                         shininess=1,
                         ambience=0.5,
                         variationPercentage=0.45,
                         variationColors=[Color(0.8, 0.8, 0.8), Color(0.5, 0.5, 0.5)],
                         revolvesAround=earth)

    mars = CelestialBody("Mars",
                          color=Color(1, 0, 0),
                          scaleFactor=0.55,
                          translation=Position(6, 0, 0),
                          rotationSpeed=0.025,
                          revolutionSpeed=0.65,
                          variationPercentage=0.30,
                          variationColors=[Color(1.0, 0.5, 0.0), Color(0.6, 0.3, 0.0), Color(1.0, 1.5, 1.0)],
                          revolvesAround=sun)

    # Create a scene
    light=Light(position=sun.translation, color=Color(1, 1, 1))
    camera=Camera()
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
