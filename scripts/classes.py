# Tworzymy classe Bearing (Wysłana przez Sławka)
import numpy as np


class Bearing:
    def __init__(self, B_geom, speed):
        self.pitchDiameter = B_geom["Pd"]
        self.meanRollerDiameter = B_geom["Rd"]
        self.numberOfRollers = B_geom["N"]
        self.contactAngle = B_geom["Ca"]
        self.speed = speed

    def roller(self):
        return (self.speed * (self.pitchDiameter / (2 * self.meanRollerDiameter))) * (
            1
            - (
                (self.meanRollerDiameter / self.pitchDiameter)
                * np.cos((self.contactAngle * np.pi) / 180)
            )
            ** 2
        )

    def inner(self):
        return (self.speed * (self.numberOfRollers / 2)) * (
            1
            + (
                (self.meanRollerDiameter / self.pitchDiameter)
                * np.cos((self.contactAngle * np.pi) / 180)
            )
        )

    def outer(self):
        return (self.speed * (self.numberOfRollers / 2)) * (
            1
            - (
                (self.meanRollerDiameter / self.pitchDiameter)
                * np.cos((self.contactAngle * np.pi) / 180)
            )
        )

    def cage(self):
        return (self.speed / 2) * (
            1
            - (
                (self.meanRollerDiameter / self.pitchDiameter)
                * np.cos((self.contactAngle * np.pi) / 180)
            )
        )

    def shaft(self):
        print(self)
        return self.speed
