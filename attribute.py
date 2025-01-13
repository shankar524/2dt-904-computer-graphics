from OpenGL.GL import *
import numpy as np

# This class allows associate shader variable from python. Copied from book.
class Attribute(object):
    def __init__(self, dataType, data):
        # type of elements in data array:
        # int | float | vec2 | vec3 | vec4
        self.dataType = dataType
        # array of data to be stored in buffer
        self.data = data
        # reference of available buffer from GPU
        self.bufferRef = glGenBuffers(1)
        # upload data immediately
        self.uploadData()

    # upload this data to a GPU buffer
    def uploadData(self):
        # convert data to numpy array format;
        # convert numbers to 32 bit floats
        data =  np.array(self.data).ravel().astype(np.float32)
        # select buffer used by the following functions
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)

        # store data in currently bound buffer
        glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)

    # associate variable in program with this buffer
    def associateVariable(self, program, variableName):
        # get reference for program variable with given name
        variableRef = glGetAttribLocation(program.programId, variableName)
        # if the program does not reference the variable, then exit
        if variableRef == -1:
            return
        # select buffer used by the following functions
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)
        # specify how data will be read
        # from the currently bound buffer into the specified
        # variable
        if self.dataType == "int":
            glVertexAttribPointer(
            variableRef, 1, GL_INT, False, 0, None)
        elif self.dataType == "float":
            glVertexAttribPointer(
            variableRef, 1, GL_FLOAT, False, 0, None)
        elif self.dataType == "vec2":
            glVertexAttribPointer(
            variableRef, 2, GL_FLOAT, False, 0, None)
        elif self.dataType == "vec3":
            glVertexAttribPointer(variableRef, 3, GL_FLOAT, False, 0, None)
        elif self.dataType == "vec4":
            glVertexAttribPointer(variableRef, 4, GL_FLOAT, False, 0, None)
        else:
            raise Exception("Attribute " +variableName +" has unknown type "+ self.dataType)
        # indicate that data will be streamed to this variable
        glEnableVertexAttribArray( variableRef )
