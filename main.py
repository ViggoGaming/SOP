import random
from matplotlib import pyplot as plt
import streamlit as st
import io
import csv
from PIL import Image
from typing import List

# Hexadecimal farvekoder til mine plots 
colors = ["#FF0000", "#0000FF", "#00FF00"]
# Maksimale k-værdi
kMax = 30


class Point:
    """
    En klasse, der repræsenterer et punkt i et 3D rum.
    
    Attributter:
        x (float): X-koordinaten for punktet.
        y (float): Y-koordinaten for punktet.
        z (float): Z-koordinaten for punktet.
        label (int): En label, der tildeles punktet.

    Metoder:
    euklidDistance(x2, y2, z2)
        Beregner Euklids afstand mellem dette punkt og et andet punkt.
    manhattanDistance(x2, y2, z2)
        Beregner Manhattan afstanden mellem dette punkt og et andet punkt.
    chebyshevDistance(x2, y2, z2)
        Beregner Chebyshev afstanden mellem dette punkt og et andet punkt.
    """

    # Klassens instruktør
    def __init__(self, x: float, y: float, z: float, label: int):
        """
        Initialiserer et Point-objekt.

        Args:
            x (float): X-koordinaten for punktet.
            y (float): Y-koordinaten for punktet.
            z (float): Z-koordinaten for punktet.
            label (int): En etiket, der er tildelt punktet.
        """
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.label: int = label

    # Her defineres de tre distanceformler 
    def euklidDistance(self, x2, y2, z2):
        """
        Beregner Euklids afstand mellem dette punkt og et andet punkt.

        Args:
            x2 (float): X-koordinaten for det andet punkt.
            y2 (float): Y-koordinaten for det andet punkt.
            z2 (float): Z-koordinaten for det andet punkt.

        Returns:
            float: Euklids afstand mellem de to punkter.
        """
        return ((x2 - self.x)**2 + (y2 - self.y)**2 + (z2 - self.z)**2)**0.5

    def manhattanDistance(self, x2, y2, z2):
        """
        Beregner Manhattan afstanden mellem dette punkt og et andet punkt.

        Args:
            x2 (float): X-koordinaten for det andet punkt.
            y2 (float): Y-koordinaten for det andet punkt.
            z2 (float): Z-koordinaten for det andet punkt.

        Returns:
            float: Manhattan afstanden mellem de to punkter.
        """
        return abs(self.x - x2) + abs(self.y - y2) + abs(self.z - z2)

    def chebyshevDistance(self, x2, y2, z2):
        """
        Beregner Chebyshev afstanden mellem dette punkt og et andet punkt.

        Args:
            x2 (float): X-koordinaten for det andet punkt.
            y2 (float): Y-koordinaten for det andet punkt.
            z2 (float): Z-koordinaten for det andet punkt.

        Returns:
            float: Chebyshev afstanden mellem de to punkter.
        """

        return max(abs(self.x - x2), abs(self.y - y2), abs(self.z - z2))


distFuncs: List = [Point.euklidDistance,
                   Point.manhattanDistance, Point.chebyshevDistance]


def KNN(x: float, y: float, z: float, k: int, funcIndex: int) -> int:
    """
    Finder den label af det punkt med den mest almindelige label blandt de k-nærmeste naboer for et givent input punkt.
    
    Args:
        x (float): X-koordinatet for punktet.
        y (float): Y-koordinatet for punktet.
        z (float): Z-koordinatet for punktet.
        k (int): Antallet af nærmeste naboer, der skal tages i betragtning.
        funcIndex (int): Indekset for afstandsfunktionen, der skal bruges.
    
    Returns:
        Label af det punkt med den mest almindelige label blandt de k-nærmeste naboer.
    """
    point = Point(x, y, z, None)
    NN = sorted(dataPoints, key=lambda c: distFuncs[funcIndex](
        point, c.x, c.y, c.z))[0:k]
    NN = list((map(lambda c: c.label, NN)))
    return most_common(NN)

# Finder det mest anvendte element i en liste
def most_common(list: List) -> int:
    """
    Finder det mest anvendte element i en given liste.
    
    Args:
        list (List): Listen, der skal gennemgås.
    
    Returns:
        Det mest anvendte element i listen.
    """
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


def calculateNumberOfLines():
    file = io.StringIO(file_contents)
    lines = csv.reader(file, delimiter=',')
    numberOfLines = 0
    for line in lines:
        numberOfLines += 1
    file.close()
    return numberOfLines


def main():
    start = False
    figure, axis = plt.subplots(2, 2)
    # Variabel der indeholder antal linjer i den indlæste csv fil
    numberOflines: int = calculateNumberOfLines()

    # Følgende kode itererer igennem hver linje i csv-filen og blander dem tilfældigt
    file = io.StringIO(file_contents)
    csv_reader = csv.reader(file, delimiter=',')
    next(csv_reader)
    csv_reader = [next(csv_reader) for x in range(numberOflines - 2)]
    random.shuffle(csv_reader)

    if st.button("Start KNN"):
        st.write("KNN kører, vent venligst... ☕")
        # Variabel der indeholder linjenummeret løkken er nået til
        lineCount = 0
        attackCount = 0
        for row in csv_reader:

            # 0    1    2        3          4        5        6             7           8
            # No.,Time,Source,Destination,Protocol,Length,Source port,Destination port,Type
            # Her udplukkes de 3 features fra  indekset, og demmer dem i hver deres variabel
            source = float(row[2].replace(".", ""))
            destination = float(row[3].replace(".", ""))
            protocol = protocols.get(row[4])
            length = int(row[5])
            destinationPort = int(row[7])
            # Her udplukkese min label
            attackType = attackTypes.get(row[8])

            if attackType:
                attackCount += 1

            # Her initialiseres et Point objekt med alle de angivne features og min label
            point = Point(protocol, length, destinationPort, attackType)
            # Her fravælges 1/3 af datasættet til træningsdata, som K-NN kan anvende til træning
            # De andre 2/3 af datasættet anvendes til at teste K-nn algoritmen 
            if (lineCount % 3 == 0):
                dataPoints.append(point)
            else:
                testPoints.append(point)
            lineCount += 1

        # Plotter alle datapointer i et punktdiagram (scatter)
        for data in dataPoints:
            axis[1, 1].scatter(
                data.x, data.y, c=colors[data.label], marker="o")

        # Plotter en præcisions graf af k-værdien
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
                a.append((correct / len(testPoints))*100)

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

    #    st.pyplot(figure)

        figure = plt.gcf()  # get current figure
        figure.set_size_inches(19, 10)
        # when saving, specify the DPI
        plt.savefig("out.png", dpi=100)

        image = Image.open("out.png")
        st.image(image)

        st.subheader(
            f"Der blev i alt fundet {attackCount} DDoS angreb i datasættet")

# Titel på min IDS hjemmeside
st.header("Victors IDS system ved brug af KNN")
# Generere et upload felt inde på hjemmesiden, så man kan uploade csv datasættet
inputFile = st.file_uploader("Upload venligst dit datasæt", type="csv")

# Tjekker om der bliver uploadet en fil
if inputFile is not None:
    global file_contents
    file_contents = inputFile.read().decode("utf-8")
    main()
