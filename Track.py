import time

class Track:
    def __init__(self,points):
        self.points = points

    def getStart(self):
        return self.points[0]
    
    def getEnd(self):
        return self.points[len(self.points)]

    def getDuration(self)
        ## measure duration between Start & end
        start  = self.points[0]
        end = self.points[len(self.points)]
        print(end-start)

