import openpyxl as xl


class TestCase:
    def __init__(self, pos, desc, wheel_orientation, currentGear, clutchEngaged, throttlePosition, currentRpm,
                 f_content):
        # [Start Value, Input]
        self.pos = pos
        self.desc = desc
        self.wheel_orientation = wheel_orientation
        self.currentGear = currentGear
        self.clutchEngaged = clutchEngaged
        self.throttlePosition = throttlePosition
        self.currentRpm = currentRpm
        self.f_content = f_content
        self.executed = [False]

    def gear_process(self, car):

        # Set clutch state
        car.theEngine.theGearbox.clutchEngaged = self.clutchEngaged[0]

        # set current Gear
        car.theEngine.theGearbox.currentGear = int(self.currentGear[0])

        # Make sure input exist and that it is not none
        if len(self.currentGear) > 1 and self.currentGear[1] is not None:
            if int(self.currentGear[1]) > 0:  # gear Up
                for i in range(int(self.currentGear[1])):
                    car.theEngine.theGearbox.shiftUp()
            elif self.currentGear[1] < 0:  # gear Down
                for i in range(abs(int(self.currentGear[1]))):
                    car.theEngine.theGearbox.shiftDown()

        # gear result
        if len(self.currentGear) < 3:
            self.currentGear.append(car.theEngine.theGearbox.currentGear)

        # If input set clutch state to input
        if len(self.clutchEngaged) > 1:
            if self.clutchEngaged[1] is not None:
                car.theEngine.theGearbox.clutchEngaged = self.clutchEngaged[1]

        # clutch Result
        if len(self.clutchEngaged) < 3:
            self.clutchEngaged.append(car.theEngine.theGearbox.clutchEngaged)


    def throttle_process(self, car, dt):
        # Fuel contents
        car.theEngine.theTank.contents = self.f_content[0]

        # Refuel
        if self.f_content[1] is not None:
            car.theEngine.theTank.refuel()


        # currentRpm
        car.theEngine.currentRpm = int(self.currentRpm[0])
        if self.currentRpm[1] is not None:
            car.theEngine.currentRpm += self.currentRpm[1]

        # Throttle
        car.theEngine.throttlePosition = self.throttlePosition[0]
        if self.throttlePosition[1] is not None:
            car.theEngine.throttlePosition = self.throttlePosition[1]

        # wheel
        for wheel in car.theEngine.theGearbox.wheels:
            car.theEngine.theGearbox.wheels[wheel].orientation = int(self.wheel_orientation[0])

        # update
        car.updateModel(dt)

        # fuel result
        if len(self.f_content) < 3:
            self.f_content.append(car.theEngine.theTank.contents)

        # throttle result
        if len(self.throttlePosition) < 3:
            self.throttlePosition.append(car.theEngine.throttlePosition)

        # Current rpm result
        if len(self.currentRpm) < 3:
            self.currentRpm.append(car.theEngine.currentRpm)

        # wheel result
        if len(self.wheel_orientation) < 3:
            self.wheel_orientation.append(round(car.theEngine.theGearbox.wheels["frontLeft"].orientation/4))


    def run(self, car, dt):
        # Gear
        self.gear_process(car)

        # Throttle Wheel Fuel
        self.throttle_process(car, dt)

        self.executed = True



class TestCases:
    def __init__(self, car, tests=[]):
        self.car = car
        self.tests = tests

    def run_cases(self, ark, dt):
        prev_case = None
        for case in self.tests:
            if prev_case is not None:
                # check if new settings applied or else use prev results
                for key in case.__dict__.keys():
                    # ikke røre pos, desc, executed. Der er intet at hente der haha
                    if key not in ["pos", "desc", "executed"]:
                        if case.__dict__[key][0] is None:
                            case.__dict__[key][0] = prev_case.__dict__[key][2]

            # run
            case.run(self.car, dt)

            # print to terminal / save results to
            print(case.desc)
            case_row_nr = int(case.pos[1:]) # get test case row
            nr = 0
            for i in case.__dict__.keys():
                if i not in ["pos", "desc", "executed"]:

                    # save to excel
                    nr += 1
                    result_data = case.__dict__[i][2]
                    ark["E" + str(case_row_nr + nr)] = result_data if type(case.__dict__[i][2]) is not bool else str(result_data)

                    # print to excel
                    if len(case.__dict__[i]) > 2:
                        print(i, case.__dict__[i][0:3])

            print("\n")
            prev_case = case



# getting car preset
def new_settings_from_ark(ark, settingOrder):
    current_settings = {}
    for i in range(len(settingOrder)):
        current_settings[settingOrder[i]] = ark.cell(row=i + 2, column=2).value
    return current_settings


# getting tests presets
def new_test_from_ark(ark):
    test_cases = []
    for row in ark.iter_rows():
        temp_cell = row[0]
        if temp_cell.value is not None:

            if "Test" in temp_cell.value:
                test_parameters = temp_cell.value.split(" ")
                test_coordinate = temp_cell.coordinate
                test_row_nr = int(test_coordinate[1:])

                # A, E
                if "Tilstand" in ark["B" + str(test_row_nr)].value and "Input" in ark["C" + str(test_row_nr)].value:
                    temp_tilstand = {}

                    i = test_row_nr + 1
                    while ark["A" + str(i)].value is not None:

                        if type(ark["B" + str(i)].value) is not None:
                            # make bool
                            if ark["B" + str(i)].value in ["True", "False"]:
                                if ark["B" + str(i)].value ==  "True":
                                    c_tilstand = True
                                elif ark["B" + str(i)].value == "False":
                                    c_tilstand = False
                            #make value
                            elif ark["B" + str(i)].value is not None:
                                c_tilstand = float(ark["B" + str(i)].value)
                            else:
                                c_tilstand = None
                        else:
                            c_tilstand = None

                        if type(ark["C" + str(i)].value) is not None:
                            if ark["C" + str(i)].value in ["True", "False"]:
                                c_input = bool(ark["C" + str(i)].value)
                            elif ark["C" + str(i)].value is not None:
                                c_input = float(ark["C" + str(i)].value)
                            else:
                                c_input = None
                        else:
                            c_input = None

                        temp_tilstand[ark["A" + str(i)].value] = [c_tilstand, c_input]
                        i += 1

                    """for t in temp_tilstand:
                        print(t, temp_tilstand[t])"""

                    test_cases.append(TestCase(test_coordinate,
                                               test_parameters[1:],
                                               temp_tilstand["wheel_orientation"],
                                               temp_tilstand["currentGear"],
                                               temp_tilstand["clutchEngaged"],
                                               temp_tilstand["throttlePosition"],
                                               temp_tilstand["currentRpm"],
                                               temp_tilstand["f_content"]))

    return test_cases
