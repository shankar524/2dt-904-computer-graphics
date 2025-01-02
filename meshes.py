from math import sin, cos, pi

def parametricSurface(uStart, uEnd, uResolution, vStart, vEnd, vResolution, surfaceFunction):
    # generate set of points on function
    deltaU = (uEnd - uStart) / uResolution
    deltaV = (vEnd - vStart) / vResolution
    positions = []
    texcoords = []

    for uIndex in range(uResolution+1):
        vArray = []
        tArray = []
        for vIndex in range(vResolution+1):
            u = uStart + uIndex * deltaU
            v = vStart + vIndex * deltaV
            vArray.append(surfaceFunction(u, v))
            tArray.append([u / (2 * pi), (v + pi / 2) / pi])
        positions.append(vArray)
        texcoords.append(tArray)

    # store vertex data
    positionData = []
    texcoordData = []

    # group vertex data into triangles # note: .copy() is necessary to avoid storing references
    for xIndex in range(uResolution):
        for yIndex in range(vResolution):
            # position data
            pA, tA = positions[xIndex+0][yIndex+0], texcoords[xIndex+0][yIndex+0]
            pB, tB = positions[xIndex+1][yIndex+0], texcoords[xIndex+1][yIndex+0]
            pD, tD = positions[xIndex+0][yIndex+1], texcoords[xIndex+0][yIndex+1]
            pC, tC = positions[xIndex+1][yIndex+1], texcoords[xIndex+1][yIndex+1]
            positionData += [pA.copy(), pB.copy(), pC.copy(),
                             pA.copy(), pC.copy(), pD.copy()]
            texcoordData += [tA.copy(), tB.copy(), tC.copy(),
                             tA.copy(), tC.copy(), tD.copy()]
    return positionData, texcoordData

def generateSphere(radiusSegments=32, heightSegments=16):
    """Generates the geometry for a unit sphere."""
    radius = 1
    size = 2*radius

    def S(u, v):
        x = size/2 * sin(u) * cos(v)
        y = size/2 * sin(v)
        z = size/2 * cos(u) * cos(v)
        point = [x, y, z]
        return point

    positions = parametricSurface(
        0, 2*pi, radiusSegments, -pi/2, pi/2, heightSegments, S)

    return positions
