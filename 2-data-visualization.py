from OpenGL.GL import *
from app import run, readFile
from glslprogram import Program
from datapoints import createDatapoints
from scene import Scene
from quad import Quad
from color import Color
import numpy as np

vsCode = readFile('./2-vs.glsl')
fsCode = readFile('./2-fs.glsl')

screenSize = [512, 512]
red = Color(1.0, 0.0, 0.0)
green = Color(0.0, 1.0, 0.0)

def findAbsoluteMax(data):
    return max(data, key=abs)

def normalizePoints(points, target_ranges=[(-1, 1), (-1, 1), (0, 1)]):
    points = np.array(points)

    # Find minimum and maximum values for each dimension
    mins = np.min(points, axis=0)
    maxs = np.max(points, axis=0)

    target_ranges = np.array(target_ranges)  # Convert to NumPy array
    target_mins = target_ranges[:, 0]
    target_maxs = target_ranges[:, 1]

    # Normalize coordinates to range [-1, 1]
    normalized_points = (points - mins) / (maxs - mins)
    normalized_points = normalized_points * (target_maxs - target_mins) + target_mins

    return normalized_points

def init():
    global program
    global graph

    # Load shaders and bind to program
    program = Program(vsCode, fsCode)
    program.use()

    points = np.array(createDatapoints())
    graph = Scene(light=None, camera=None)

    for point in normalizePoints(points):
        quad = Quad(point[0], point[1], point[2] )
        graph.addObject(quad)

    program.setUniformVec2("resolution", screenSize)
    program.setUniformVec3("startColor", green.asArray())
    program.setUniformVec3("endColor", red.asArray())
    # Setup the scene
    graph.setup(program)

def update(dt, time):
    graph.draw(program, dt, time)

run("2DT904 - Programming assignment [Data Visualization]", init=init, update=update, screenSize=screenSize)
