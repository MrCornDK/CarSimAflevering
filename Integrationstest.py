import model
import openpyxl as xl

import test_funktioner as test_

wb = xl.load_workbook("test.xlsx")
test_sheet = wb['test']


# Burde have integreret op samme måde som test cases
# But time is a thing and i have a deadline.
settings_order = ["wheel_orientation", "wheel_omkreds", "wheels", "currentGear", "clutchEngaged", "gears",
                  "throttlePosition", "currentRpm", "consumptionConstant", "maxRpm", "f_capacity", "f_content"]


# make new car with custom settings
def newCar(s):
    # wheel
    wheel = model.Wheel(int(s["wheel_orientation"]), int(s["wheel_omkreds"]))
    wheels = {}
    for w in s["wheels"].split(","):
        wheels[w] = wheel

    # Gear
    gears = []
    for gear in s["gears"].split(","):
        gears.append(float(gear))

    if s["clutchEngaged"] == "False":
        clutch = False
    elif s["clutchEngaged"] == "True":
        clutch = True
    else:
        clutch = s["clutchEngaged"]

    gearbox = model.Gearbox(wheels=wheels, currentGear=int(s["currentGear"]), clutchEngaged=clutch, gears=gears)

    tank = model.Tank(int(s["f_capacity"]), int(s["f_content"]))

    engine = model.Engine(float(s["throttlePosition"]), gearbox, float(s["currentRpm"]), float(s["consumptionConstant"]), int(s["maxRpm"]), tank)

    car = model.Car(engine)

    return car


def main(settings_order, ark):
    # Car settings
    settings = test_.new_settings_from_ark(ark, settings_order)
    #print((f'Car settings \n {settings} \n'))


    # Make Car
    car = newCar(settings)
    #print(f'Car: \n {car} \n')


    # Get tests
    tests = test_.new_test_from_ark(ark)

    test_cases = test_.TestCases(car, tests)


    # Test Car
    test_cases.run_cases(ark)
    wb.save("test.xlsx")
    wb.close()


if __name__ == "__main__":
    main(settings_order, test_sheet)

