from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from os import environ
import argparse
import json
from time import sleep
from Library.plot import plotPropeller, plotMotor, plotBattery
import simulation as sim

load_dotenv()

# Defining the arguments
parser = argparse.ArgumentParser(
    description="Given a type of graph, plots the results of a simulation."
)
parser.add_argument(
    "-p",
    "--propeller",
    action="store_true",
    help="Plot graphs with propeller curves.",
)
parser.add_argument(
    "-m",
    "--motor",
    action="store_true",
    help="Plot graphs with motor curves.",
)
parser.add_argument(
    "-b",
    "--battery",
    action="store_true",
    help="Plot graphs with battery curves.",
)
parser.add_argument(
    "-r",
    "--remake",
    action="store_true",
    help="You can use with a plot type to re-render the graphs without having to simulate again.",
)

args, _ = parser.parse_known_args()

if not True in vars(args).values():
    print("\nMissing arguments for simulation type! \n")
    parser.print_help()
    exit()

# Remake Condition
if args.propeller and args.remake:
    plotPropeller(remake=True)
    exit()

if args.motor and args.remake:
    plotMotor(remake=True)
    exit()

if args.battery and args.remake:
    plotBattery(remake=True)
    exit()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Ecalc Login URL
loginUrl = (
    "https://www.ecalc.ch/calcmember/login.php?https://www.ecalc.ch/xcoptercalc.php"
)

login = environ.get("ECALC_LOGIN")
password = environ.get("ECALC_PASSWORD")

driver.get(loginUrl)

# Login to Ecalc
driver.find_element(By.ID, "username").send_keys(login)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.ID, "myButton").click()

# Waiting for alert to appear
wait = WebDriverWait(driver, 50)
wait.until(expected_conditions.alert_is_present()).accept()
# Acception Cookies
driver.find_element(By.XPATH, "/html/body/div[3]/div").click()

# Defining inputs
battery = Select(driver.find_element(By.XPATH, '//*[@id="inBCell"]'))
batteryCells = driver.find_element(By.XPATH, '//*[@id="inBS"]')
propellerBlades = driver.find_element(By.XPATH, '//*[@id="inPBlades"]')
frameSize = driver.find_element(By.XPATH, '//*[@id="inGFrame"]')
propellerBrand = Select(driver.find_element(By.XPATH, '//*[@id="inPType"]'))
propellerDiameter = driver.find_element(By.XPATH, '//*[@id="inPDiameter"]')
pitch = driver.find_element(By.XPATH, '//*[@id="inPPitch"]')
esc = Select(driver.find_element(By.XPATH, '//*[@id="inEType"]'))
motorBrand = Select(driver.find_element(By.XPATH, '//*[@id="inMManufacturer"]'))
motorModel = Select(driver.find_element(By.XPATH, '//*[@id="inMType"]'))
weight = driver.find_element(By.XPATH, '//*[@id="inGWeight"]')
MassType = Select(driver.find_element(By.XPATH, '//*[@id="inGWeightCalc"]'))

# Defining Outputs
totalWeight = driver.find_element(By.XPATH, '//*[@id="outTotAUW"]')
flightTime = driver.find_element(By.XPATH, '//*[@id="outBHoverFlightTime"]')
thrustWeight = driver.find_element(By.XPATH, '//*[@id="outTotThrustWeight"]')
specificThrust = driver.find_element(By.XPATH, '//*[@id="outPEfficiency"]')
driveWeight = driver.find_element(By.XPATH, '//*[@id="outTotDriveWeight"]')
maxVelocity = driver.find_element(By.XPATH, '//*[@id="outCopterV"]')
mixedFlightTime = driver.find_element(By.XPATH, '//*[@id="outBMixedFlightTime"]')
current = driver.find_element(By.XPATH, '//*[@id="outHoverI"]')
Voltage = driver.find_element(By.XPATH, '//*[@id="outHoverV"]')
rpm = driver.find_element(By.XPATH, '//*[@id="outHoverRpm"]')

# Splitting using the comma
motorsBrands = sim.motorBrand.split(",")
motorsModels = sim.motorModels.split(",")
batteries = sim.batteries.split(",")
bladeNumbers = sim.bladeNumbers.split(",")
propellersBrands = sim.propellersBrands.split(",")
propellers = sim.propellers.split(",")

# Setting General Inputs
MassType.select_by_visible_text(sim.massType)
frameSize.send_keys(Keys.BACKSPACE * 3, sim.frameSize)
esc.select_by_visible_text(sim.esc)

# Simulate button
simulateBtn = driver.find_element(
    By.XPATH, '//*[@id="theForm"]/table/tbody/tr[5]/td[17]/input'
)


def getDataByMass(minMass, maxMass, interval):
    data = {
        "flightTime": [],
        "totalWeight": [],
        "thrustWeight": [],
        "specificThrust": [],
        "driveWeight": [],
        "maxVelocity": [],
        "mixedFlightTime": [],
        "current": [],
        "Voltage": [],
        "rpm": [],
    }

    for mass in range(minMass, maxMass + 1, interval):
        weight.send_keys(Keys.BACKSPACE * 25, mass)
        simulateBtn.click()
        sleep(3)
        data["flightTime"].append(float(flightTime.text))
        data["totalWeight"].append(float(totalWeight.text))
        data["thrustWeight"].append(float(thrustWeight.text))
        data["specificThrust"].append(float(specificThrust.text))
        data["driveWeight"].append(float(driveWeight.text))
        data["maxVelocity"].append(float(maxVelocity.text))
        data["mixedFlightTime"].append(float(mixedFlightTime.text))
        data["current"].append(float(current.text))
        data["Voltage"].append(float(Voltage.text))
        data["rpm"].append(float(rpm.text))

    return data


if args.propeller:

    propData = {
        "title": f"{motorsBrands[0]} {motorsModels[0]} | {batteries[0]} {sim.batteryCells}S | ESC {sim.esc}",
        "filename": f"{motorsBrands[0]}_{motorsModels[0]}_{batteries[0]}_{sim.batteryCells}S_{sim.esc}".replace(
            " ", "_"
        ).replace(
            "/", "-"
        ),
    }

    battery.select_by_visible_text(batteries[0])
    batteryCells.send_keys(Keys.BACKSPACE, sim.batteryCells)
    motorBrand.select_by_visible_text(motorsBrands[0])
    motorModel.select_by_visible_text(motorsModels[0])
    for idx, propeller in enumerate(propellers):

        if len(bladeNumbers) == 1:
            idxBladeNum = 0
        else:
            idxBladeNum = idx

        if len(propellersBrands) == 1:
            idxPropBrand = 0
        else:
            idxPropBrand = idx

        _diameter, _pitch = propeller.split("x")
        propellerBrand.select_by_visible_text(propellersBrands[idxPropBrand])
        propellerBlades.send_keys(Keys.BACKSPACE, bladeNumbers[idxBladeNum])
        propellerDiameter.send_keys(Keys.BACKSPACE * 10, _diameter)
        pitch.send_keys(Keys.BACKSPACE * 10, _pitch)

        propData[f"{propeller} {propellersBrands[idxPropBrand]}"] = getDataByMass(
            sim.minMass, sim.maxMass, sim.massInterval
        )

    driver.close()
    plotPropeller(propData)
    with open("JSON/propData.json", "w") as fp:
        json.dump(propData, fp, indent=4)

if args.motor:

    motorData = {
        "title": f"Hélice {propellersBrands[0]} - {propellers[0]} | {batteries[0]} {sim.batteryCells}S | ESC {sim.esc}",
        "filename": f"Helice_{propellersBrands[0]}_{propellers[0]}_{batteries[0]}_{sim.batteryCells}S_{sim.esc}".replace(
            " ", "_"
        ).replace(
            "/", "-"
        ),
    }
    battery.select_by_visible_text(batteries[0])
    batteryCells.send_keys(Keys.BACKSPACE, sim.batteryCells)
    _diameter, _pitch = propellers[0].split("x")
    propellerBrand.select_by_visible_text(propellersBrands[0])
    propellerBlades.send_keys(Keys.BACKSPACE, bladeNumbers[0])
    propellerDiameter.send_keys(Keys.BACKSPACE * 10, _diameter)
    pitch.send_keys(Keys.BACKSPACE * 10, _pitch)
    for _motorBrand, _motorModel in zip(motorsBrands, motorsModels):
        motorBrand.select_by_visible_text(_motorBrand)
        motorModel.select_by_visible_text(_motorModel)

        motorData[f"{_motorBrand} {_motorModel}"] = getDataByMass(
            sim.minMass, sim.maxMass, sim.massInterval
        )

    driver.close()
    plotMotor(motorData)
    with open("JSON/motorData.json", "w") as fp:
        json.dump(motorData, fp, indent=4)
