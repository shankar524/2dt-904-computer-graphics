from OpenGL.GL import glEnable, glClear, GL_CULL_FACE, GL_DEPTH_TEST, GL_DEPTH_BUFFER_BIT, GL_COLOR_BUFFER_BIT
from light import Light
from matrix import Matrix
from camera import Camera

class Scene:
    def __init__(self, camera = Camera(), light=Light(), objects=None):
        self.camera = camera
        self.light = light
        self.objects = objects if objects is not None else []

    def addObject(self, obj):
        self.objects.append(obj)

    def setup(self, program):
        for object in self.objects:
            object.upload(program)

        projection = Matrix.makePerspective(self.camera.angleOfView, self.camera.aspectRatio, self.camera.near, self.camera.far)
        invCameraPos = Matrix.makeTranslation(self.camera.position.x, self.camera.position.y, self.camera.position.z)
        mProjView = projection @ invCameraPos

        program.setUniformMat4('mProjView', mProjView)

        program.setUniformVec3('lightPos', self.light.position.asArray())
        program.setUniformVec3('viewPos', self.camera.position.asArray())
        program.setUniformVec3('lightColor', self.light.color.asArray())

        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)

    def draw(self, program, dt, time):
        glClear(GL_DEPTH_BUFFER_BIT)
        glClear(GL_COLOR_BUFFER_BIT)
        for object in self.objects:
            object.draw(program, dt, time)
