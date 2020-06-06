import tenpy.utility.operators as op
import math

class CreateVector:

    def __init__(self, info = []):
        self.info = info

########################################################################################################################
### VECTOR PROPERTIES
########################################################################################################################

    #Returns value of vector as an array
    def val(self):
        return self.info

    #Returns magnitude of vector
    def mag(self):
        mag = 0
        for i in range(len(self.info)):
            mag += math.pow(self.info[i], len(self.info))
        return math.sqrt(mag)

    #Returns angle of vector
    def angle(self):
        self.x = self.info[0]
        self.y = self.info[1]
        if len(self.info) > 2:
            self.z = self.info[2]

        if len(self.info) == 2:
            if (self.x < 0) and (self.y > 0):
                return math.pi + math.atan(self.y/self.x)
            elif (self.x < 0) and (self.y < 0):
                return math.pi - math.atan(self.y/self.x)
            elif (self.x > 0) and (self.y < 0):
                return 2*math.pi + math.atan(self.y/self.x)
            elif (self.x > 0) and (self.y > 0):
                return math.atan(self.y/self.x)
            elif (self.x > 0) and (self.y == 0):
                return 0.0
            elif (self.x < 0) and (self.y == 0):
                return math.pi
            elif (self.x == 0) and (self.y > 0):
                return math.pi/2
            elif (self.x == 0) and (self.y < 0):
                return 3*math.pi/2
            else:
                return math.atan(self.y/self.x)
        elif len(self.info) == 3:
            pass
        else:
            return "Error: Tenpy does not support non-two dimensional vector angles"

    def angle_between(self, other):
        angle = math.acos(self.dot_prod(other)/(self.mag()*other.mag()))
        return angle

########################################################################################################################
### GENERAL VECTOR EVALUATION
########################################################################################################################

    # Operates on vectors by element
    def element_eval(self, other=[], sign="+"):
        if len(self.info) == len(other.info):
            result = []
            for i in range(len(self.info)):
                result.append(op.get_operator_fn(sign)(self.info[i], other.info[i]))
            return CreateVector(result)
        else:
            return "Vector Not Operatable"

########################################################################################################################
### VECTOR MULTIPLICATION
########################################################################################################################

    def dot_prod(self, other):
        prod = 0
        if len(self.info) == len(other.info):
            for i in range(len(self.info)):
                prod += self.info[i] * other.info[i]
        else:
            return "Error: Vector Length Mismatch"
        return prod

    def cross_prod(self, other):
        prod = []

        a = self.info
        b = other.info
        if len(self.info) == len(other.info):
            if len(self.info) == 3 and len(other.info) == 3:
                #angle = math.acos(self.dot_prod(other)/self.mag()*other.mag())
                prod.append(a[1]*b[2]-a[2]*b[1])
                prod.append(a[2]*b[0]-a[0]*b[2])
                prod.append(a[0]*b[1]-a[1]*b[0])
            else:
                return "Sorry, cross product is only applicable for 3d vectors"
        else:
            return "Error: Vector Length Mismatch"
        return CreateVector(prod)

########################################################################################################################
### VECTOR RELATIONS
########################################################################################################################

    def is_parallel(self, other):
        tolerance = 2.0e-5
        if (self.angle_between(other) < 0.0+tolerance):
            print(self.angle_between(other))
            return True
        else:
            return False

    def is_orthogonal(self, other):
        if (self.dot_prod(other) == 0):
            return True
        else:
            return False