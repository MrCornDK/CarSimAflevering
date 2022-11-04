from random import randint


class Wheel(object):
    def __init__(self, orientation=randint(0, 360), omkreds = 135):
        self.orientation = orientation  # int Range 0 to 360 (grader)
        self.omkreds = omkreds # int cm

    def rotate(self, revolutions):
        self.orientation = (self.orientation + revolutions   * 360) % 360


class Gearbox(object):
    def __init__(self, wheels={'frontLeft': Wheel(), 'frontRight': Wheel(), 'rearLeft': Wheel(), 'rearRight': Wheel()},
                 currentGear=0, clutchEngaged=False, gears=[0, 0.8, 1, 1.4, 2.2, 3.8]):
        self.wheels = wheels  # Dict
        self.currentGear = currentGear  # Int
        self.clutchEngaged = clutchEngaged  # Bool
        self.gears = gears  # list

    def shiftUp(self):
        if self.currentGear < len(self.gears) - 1 and not self.clutchEngaged:
            self.currentGear += 1

    def shiftDown(self):
        if self.currentGear > 0 and not self.clutchEngaged:
            self.currentGear -= 1

    def rotate(self, revolutions):
        if self.clutchEngaged:
            for wheel in self.wheels:
                self.wheels[wheel].rotate(revolutions * self.gears[self.currentGear])


class Tank(object):
    def __init__(self, capacity=100, contents=100):
        self.capacity = capacity  # int
        self.contents = contents  # int

    def remove(self, amount):
        self.contents -= amount
        if self.contents < 0:
            self.contents = 0

    def refuel(self):
        self.contents = self.capacity


class Engine(object):
    def __init__(self, throttlePosition=0, theGearbox=Gearbox(), currentRpm=0, consumptionConstant=0.0025, maxRpm=100,
                 theTank=Tank()):
        self.throttlePosition = throttlePosition  # Opgave siger int men lyder mere som float. Range 0 to 1
        self.theGearbox = theGearbox  # Instans af Gearbox
        self.currentRpm = currentRpm  # Int af nuværende omdrejningstal
        self.consumptionConstant = consumptionConstant  # float brændstof forbrug af moteren pr. omdrejning pr. min
        self.maxRpm = maxRpm  # int. Det maksimal omdrejningstal
        self.theTank = theTank  # Instans af Tank

    def updateModel(self, dt):
        if self.theTank.contents > 0:
            self.currentRpm = self.throttlePosition * self.maxRpm
            """if self.currentRpm != 0:
                muligConsumptionProcent = ((self.currentRpm * self.consumptionConstant) / self.theTank.contents)
                # ved brug af modulo kan vi få en krøk af hvor meget kraft vi kan deliver. Og vis at tanken meget over hvad der vil blive brugt så vil det stadig give et da 1 modulo med noget der er hæjeren 1 er = 1
                kraft = 1 % muligConsumptionProcent
            else:
                kraft = 0
            # self.currentRpm = self.currentRpm * kraft"""
            self.theTank.remove(self.currentRpm * self.consumptionConstant)  # Vi fjerner brændstoffet fra tanken
            self.theGearbox.rotate(self.currentRpm * (dt / 60))  # Rotere hjul
        else:
            self.currentRpm = 0


class Car(object):
    def __init__(self, theEngine = Engine()):
        self.theEngine = theEngine

    def updateModel(self, dt):
        self.theEngine.updateModel(dt)
