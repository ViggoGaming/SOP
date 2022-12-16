import random
from matplotlib import pyplot as plt
import csv
from typing import List

# Graf farver
colors = ["#FF0000", "#0000FF", "#00FF00"]
kMax = 99

figure, axis = plt.subplots(2, 2)


class Point:
    def __init__(self, x: float, y: float, z: float, label: int):
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.label: int = label

    def euklidDistance(self, x2, y2, z2):
        return ((x2 - self.x)**2 + (y2 - self.y)**2 + (z2 - self.z)**2)**0.5

    def manhattanDistance(self, x2, y2, z2):
        return abs(self.x - x2) + abs(self.y - y2) + abs(self.z - z2)

    def chebyshevDistance(self, x2, y2, z2):
        return max(abs(self.x - x2), abs(self.y - y2), abs(self.z - z2))


distFuncs: List = [Point.euklidDistance,
                   Point.manhattanDistance, Point.chebyshevDistance]


def KNN(x: float, y: float, z: float, k: int, funcIndex: int) -> int:
    point = Point(x, y, z, None)
    NN = sorted(dataPoints, key=lambda c: distFuncs[funcIndex](
        point, c.x, c.y, c.z))[0:k]
    NN = list((map(lambda c: c.label, NN)))
    return most_common(NN)


"""
def KNN(x: float, y: float, z: float, k: int, funcIndex: int) -> int:
    def distance(point, data_point):
        return distFuncs[funcIndex](point, data_point.x, data_point.y, data_point.z)

    point = Point(x, y, z, None)
    NN = sorted(dataPoints, key=lambda data_point: distance(point, data_point))[0:k]
    NN = [c.label for c in NN]
    return most_common(NN)
"""


def most_common(list: List) -> int:
    return max(set(list), key=list.count)


dataPoints = []
testPoints = []

protocols = {
    "BROWSER": 0,
    "DHCP": 1,
    "DNS": 2,
    "HTTP": 3,
    "ICMP": 4,
    "IGMPv3": 5,
    "MDNS": 6,
    "NBNS": 7,
    "NTP": 8,
    "OCSP": 9,
    "Protocol": 10,
    "SSDP": 11,
    "SSLv2": 12,
    "TCP": 13,
    "TLSv1.2": 14,
    "TLSv1.3": 15,
    "UDP": 17
}

# Erstatter attackType kolonen med numeriske værdier i stedet for strings
attackTypes = {
    "Clean": 0,
    "Attack": 1
}

numberOfLines = 0
for line in open("./datasets/SOP_dataset_mini.csv"):
    numberOfLines += 1


with open("./datasets/SOP_dataset_mini.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    csv_reader = [next(csv_reader) for x in range(numberOfLines - 2)]
    random.shuffle(csv_reader)

    lineCount = 0
    for row in csv_reader:
        # Opsætter de
        source = float(row[2].replace(".", ""))
        destination = float(row[3].replace(".", ""))
        protocol = protocols.get(row[4])
        length = int(row[5])
        destinationPort = int(row[7])
        attackType = attackTypes.get(row[8])

        # point = Point(source, destination, protocol, attackType)
        point = Point(destination, source, protocol, attackType)
        # Put 1/3 of data in training data, and 2/3 in test data
        if (lineCount % 3 == 0):
            dataPoints.append(point)
        else:
            testPoints.append(point)
        lineCount += 1


# Plotter alle datapointer
for data in dataPoints:
    axis[1, 1].scatter(data.x, data.y, c=colors[data.label], marker="o")

#    if data.label == 1:
#        print(data.x, data.y)


for funcIndex in range(len(distFuncs)):
    a = []
    pa = None
    for k in range(1, kMax):
        print(f"k: {k}")
        correct = 0
        for testPoint in testPoints:
            if KNN(testPoint.x, testPoint.y, testPoint.z, k, funcIndex) == testPoint.label:
                # axis[1,1].scatter(testPoint.x, testPoint.y, c=colors[testPoint.label], marker=matplotlib.markers.CARETUPBASE)
                correct += 1
        a.append(correct / len(testPoints))

    print(f"funcindex: {funcIndex}")
    match funcIndex:
        case 0:
            axis[0, 0].plot([k for k in range(1, kMax)], a,
                            "o-", color=colors[funcIndex])
            axis[0, 0].set_title("(K, Præcision)-graf for DDOS-angreb")
            axis[0, 0].legend("Euklid")
            # axis[0, 0].set_xlabel="K"
            # axis[0, 0].set_ylabel="Antal korrekte klassificeringer i %"
            axis[0, 0].set_xticks([x for x in range(1, kMax)])
        case 1:
            axis[0, 1].plot([k for k in range(1, kMax)], a,
                            "o-", color=colors[funcIndex])
            axis[0, 1].set_title("(K, Præcision)-graf for DDOS-angreb")
            axis[0, 1].legend("Manhattan")
            # axis[0, 0].set_xlabel="K"
            # axis[0, 0].set_ylabel="Antal korrekte klassificeringer i %"
            axis[0, 1].set_xticks([x for x in range(1, kMax)])
        case 2:
            axis[1, 0].plot([k for k in range(1, kMax)], a,
                            "o-", color=colors[funcIndex])
            axis[1, 0].set_title("(K, Præcision)-graf for DDOS-angreb")
            axis[1, 0].legend("Chebyshev")
            # axis[0, 0].set_xlabel="K"
            # axis[0, 0].set_ylabel="Antal korrekte klassificeringer i %"
            axis[1, 0].set_xticks([x for x in range(1, kMax)])

figure.supxlabel("K")
figure.supylabel("Antal korrekte klassificeringer i %")

plt.show()
