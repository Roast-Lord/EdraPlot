import matplotlib.pyplot as plt
from tqdm import tqdm
import json
import os

current_directory_path = os.getcwd()


def plotPropeller(propData=None, remake=False):

    if remake:
        with open(
            os.path.join(current_directory_path, "JSON/propData.json")
        ) as jsonFile:
            propData = json.load(jsonFile)

    print("\n Plotting Graphs...\n")
    initials = ["TWxFT", "TWxMFT", "TWxTW", "TWxST"]
    xlabels = ["Total Weight (g)"] * 4
    ylabels = [
        "Flight Time (min)",
        "Mixed Flight Time (min)",
        "Thrust-Weight",
        "Specific Thrust (g/W)",
    ]
    keys1 = ["totalWeight"] * 4
    keys2 = ["flightTime", "mixedFlightTime", "thrustWeight", "specificThrust"]
    for key1, key2, inital, xlabel, ylabel in tqdm(
        zip(keys1, keys2, initials, xlabels, ylabels)
    ):
        for prop in propData:
            try:
                plt.plot(
                    propData[prop][key1],
                    propData[prop][key2],
                    label=prop,
                )
            except TypeError:
                pass
        plt.xticks(propData[prop][key1])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.title(f"{propData['title']}")
        plt.legend()
        subfolder_path = os.path.join(current_directory_path, "Plots")
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        file_path = os.path.join(subfolder_path, f"{propData['filename']}-{inital}.png")
        plt.savefig(file_path, dpi=1200)
        plt.close()
    print("\n Graphs plotted!\n")


def plotMotor(motorData=None, remake=False):
    if remake:
        with open(
            os.path.join(current_directory_path, "JSON/motorData.json")
        ) as jsonFile:
            motorData = json.load(jsonFile)

    print("\n Plotting Graphs...\n")
    initials = [
        "TWxFT",
        "TWxMFT",
        "TWxTW",
        "TWxST",
        "TWxMV",
    ]
    xlabels = ["Total Weight (g)"] * 5
    ylabels = [
        "Flight Time (min)",
        "Mixed Flight Time (min)",
        "Thrust-Weight",
        "Specific Thrust (g/W)",
        "Max Velocity (km/h)",
    ]
    keys1 = ["totalWeight"] * 5
    keys2 = [
        "flightTime",
        "mixedFlightTime",
        "thrustWeight",
        "specificThrust",
        "maxVelocity",
    ]

    for key1, key2, inital, xlabel, ylabel in tqdm(
        zip(keys1, keys2, initials, xlabels, ylabels)
    ):
        for motor in motorData:
            try:
                plt.plot(
                    motorData[motor][key1],
                    motorData[motor][key2],
                    label=motor,
                )
            except TypeError:
                pass
        plt.xticks(motorData[motor][key1])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.title(f"{motorData['title']}")
        plt.legend()
        subfolder_path = os.path.join(current_directory_path, "Plots")
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        file_path = os.path.join(
            subfolder_path, f"{motorData['filename']}-{inital}.png"
        )
        plt.savefig(file_path, dpi=1200)
        plt.close()
    print("\n Graphs plotted!\n")


def plotBattery(batteryData):
    pass
