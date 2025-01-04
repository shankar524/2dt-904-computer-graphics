from OpenGL.GL import *
import numpy as np


def fromSource(vsCode, fsCode):

    def initializeShader(shaderCode, shaderType):
        shaderCode = '#version 330\n' + shaderCode

        ref = glCreateShader(shaderType)
        glShaderSource(ref, shaderCode)
        glCompileShader(ref)

        success = glGetShaderiv(ref, GL_COMPILE_STATUS)
        if not success:
            message = glGetShaderInfoLog(ref)
            glDeleteShader(ref)

            message = '\n' + message.decode('utf-8')
            raise Exception(message)
        return ref

    vsRef = initializeShader(vsCode, GL_VERTEX_SHADER)
    fsRef = initializeShader(fsCode, GL_FRAGMENT_SHADER)

    program = glCreateProgram()
    glAttachShader(program, vsRef)
    glAttachShader(program, fsRef)

    glLinkProgram(program)

    success = glGetProgramiv(program, GL_LINK_STATUS)
    if not success:
        message = glGetProgramInfoLog(program)
        glDeleteProgram(program)

        message = '\n' + message.decode('utf-8')
        raise Exception(message)

    return program


class Program(object):
    def __init__(self, vsSource, fsSource) -> None:
        self.programId = fromSource(vsSource, fsSource)

    def setUniformFloat(self, name, value):
        ref = glGetUniformLocation(self.programId, name)
        glUniform1f(ref, value)

    def setUniformBoolean(self, name, value):
        ref = glGetUniformLocation(self.programId, name)
        glUniform1i(ref, 1 if value==True else 0)

    def setUniformVec3(self, name, value):
        ref = glGetUniformLocation(self.programId, name)
        glUniform3f(ref, value[0], value[1], value[2])

    def setUniformVec4(self, name, value):
        ref = glGetUniformLocation(self.programId, name)
        glUniform4fv(ref, 1, np.array(value, dtype=np.float32))

    def setUniformMat4(self, name, value):
        ref = glGetUniformLocation(self.programId, name)
        glUniformMatrix4fv(ref, 1, GL_TRUE, value)

    def getAttribute(self, name):
        return glGetAttribLocation(self.programId, name)

    def use(self):
        glUseProgram(self.programId)
