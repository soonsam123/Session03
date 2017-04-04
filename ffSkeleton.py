import lib601.sm as sm

class FollowFigure(sm.SM):
    def __init__(self, points):
        self.points = points
        self.startState = 0   # index
        self.len = len(self.points)
    def getNextValues(self, state, inp):
        # See if the pose is near to any point.
        for i in range(self.len):
            if inp.odometry.point().isNear(self.points[i], 0.01):
                # If it is near to the last point.
                # Go to the first point again.
                if i == self.len -1:
                    return (0, self.points[0])
                # If it is, go to the next point.
                else:
                    return (i + 1, self.points[i + 1])
        # If it is near to no point, keep outputting the next.
        return (state, self.points[state])
