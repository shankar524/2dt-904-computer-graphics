from OpenGL.GL import glEnable, glClear, GL_CULL_FACE, GL_DEPTH_TEST, GL_DEPTH_BUFFER_BIT, GL_COLOR_BUFFER_BIT
from light import Light
from matrix import Matrix

class Scene:
    def __init__(self, cameraPos = [0, 0, -20], light=Light(position=[1, 1, 1], color=(1, 1, 1)), objects=None):
        self.cameraPos = cameraPos
        self.light = light
        self.objects = objects if objects is not None else []

    def addObject(self, obj):
        self.objects.append(obj)

    def setup(self, program):
        for object in self.objects:
            object.upload(program)

        projection = Matrix.makePerspective()
        invCameraPos = Matrix.makeTranslation(self.cameraPos[0], self.cameraPos[1], self.cameraPos[2])
        mProjView = projection @ invCameraPos

        program.setUniformMat4('mProjView', mProjView)

        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)

    def draw(self, program, dt, time):
        glClear(GL_DEPTH_BUFFER_BIT)
        glClear(GL_COLOR_BUFFER_BIT)
        for object in self.objects:
            object.draw(program, dt, time)
