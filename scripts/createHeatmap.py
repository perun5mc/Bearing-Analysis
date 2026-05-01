# KOMENTARZE PO ANGIELSKU SĄ Z PRZYKŁADU
# PRZYKŁADY DOSTĘPNE SĄ W SKRYPCIE O ZAWARTOŚCI:
# import pyqtgraph.examples
# pyqtgraph.examples.run()
# JEŚLI CHCESZ ICH UŻYĆ, UTWÓRZ NOWY SKRYPT I GO URUCHOM
# ps. heatmapa w tym tutorialu nazywa się matrix

from pyqtgraph.Qt import QtGui
import pyqtgraph as pg
import numpy as np
import math

# jest to funkcja która przyjmuje dane i zwraca nam okno, które 
# potem dodajemy do odpowiedniego docka w postaci widgetu

def createHeatmap(data):
    gr_wid = pg.GraphicsLayoutWidget(show=False) # tworzymy sobie okno
    gr_wid.setBackground("white")

    label = pg.LabelItem(justify='center') # dodajemy label
    label.setText(f"<span style='font-size: 12pt;color: none'>‎</span>") # ustawiamy text labela na niewidoczny na start
    gr_wid.addItem(label)

    plotItem = gr_wid.addPlot(row=1, col=0)  # add PlotItem to the main GraphicsLayoutWidget
    plotItem.invertY(False)  # orient y axis to run top-to-bottom
    plotItem.setDefaultPadding(0.1)  # plot without padding data range

    corrMatrix = np.array(data["Heatmap"]["z"]) # tworzymy matrycę na podstawie podanych wartości
    pg.setConfigOption('imageAxisOrder', 'row-major')  # Switch default order to Row-major

    correlogram = pg.ImageItem()
    # correlogram.setOpacity(0.5)

    tr = QtGui.QTransform().translate(-0.5, 0)  # oś X przesuwamy odrobinę w lewo, osi y natomiast nie
    correlogram.setTransform(tr)
    correlogram.setImage(corrMatrix)

    plotItem.addItem(correlogram)  # display correlogram

    # dodajemy labele z jednostkami oraz zmieniamy ich kolory
    labelStyle = {'color': 'black;', 'font-size': '15px; padding: 5px;'}
    plotItem.getAxis('left').setLabel('Time', units='s', **labelStyle)
    plotItem.getAxis('bottom').setLabel('Frequency', units='Hz', **labelStyle)
   
    plotItem.getAxis('left').setTextPen('black')
    plotItem.getAxis('right').setTextPen('black')
    plotItem.getAxis('top').setTextPen('black')
    plotItem.getAxis('bottom').setTextPen('black')

    plotItem.getAxis('left').setTickPen('black')
    plotItem.getAxis('right').setTickPen('black')
    plotItem.getAxis('top').setTickPen('black')
    plotItem.getAxis('bottom').setTickPen('black')
    
    # show full frame, label tick marks at top and left sides, with some extra space for labels:
    plotItem.showAxes(True, showValues=(True, False, False, True), size=20)

    # zmieniamy skalę tak, aby wartości X oraz Y na wykresie odpowiadały wartościom X oraz Z poszczególnych kwadracików heatmapy
    scaleX = max(data["Heatmap"]["x"]) / (len(data["Heatmap"]["z"][0]) - 1)
    plotItem.getAxis('bottom').setScale(scaleX)

    scaleY = max(data["Heatmap"]["y"]) / (len(data["Heatmap"]["z"]) - 0.5)
    plotItem.getAxis('left').setScale(scaleY)

    plotItem.getAxis('bottom').setHeight(45)  # include some additional space at bottom of figure
    plotItem.getAxis('left').setWidth(60)

    # colorMap = pg.colormap.get("CET-D1")  # Domyślny colormap 
    colorMap = pg.colormap.get("CET-L1")    # Ten colormap wybrałem bo o taki poprosił mnie Kamil
                                            # Colormapy są dostępne w folderze pyqtgraph/colors/maps

    maxZ = []
    for table in data["Heatmap"]["z"]:
        maxZ.append(max(table))
    maxZ = max(maxZ)

    bar = pg.ColorBarItem(values=(0, maxZ), colorMap=colorMap)
    bar.getAxis("right").setTextPen("black")
    bar.getAxis("right").setTickPen("black")
    # link color bar and color map to correlogram, and show it in plotItem:
    bar.setImageItem(correlogram, insert_in=plotItem)
    plotItem.autoBtn.clicked.connect(lambda: bar.setLevels((0, maxZ))) # kiedy klikniemy autoButton to resetuje sie nam również skala color bara

    plotItem.setDefaultPadding(0)
    
    # dodajemy linie wskazujące
    vLine = pg.InfiniteLine(angle=90, movable=False)
    hLine = pg.InfiniteLine(angle=0, movable=False)
    plotItem.addItem(vLine, ignoreBounds=True)
    plotItem.addItem(hLine, ignoreBounds=True)

    vb = plotItem.vb

    # event ruchu myszką
    def mouseMoved(evt):
        pos = evt
        if plotItem.sceneBoundingRect().contains(pos):
            mousePoint = vb.mapSceneToView(pos)
            posX = mousePoint.x() * scaleX
            posY = mousePoint.y() * scaleY
            if (posX >= min(data["Heatmap"]["x"]) - (0.5 * scaleX) and posX <= max(data["Heatmap"]["x"]) + (0.5 * scaleX)) and (   # sprawdzamy czy kursor znajduje się na heatmapie
                    posY >= min(data["Heatmap"]["y"]) - (0.575 * scaleY) and posY <= max(data["Heatmap"]["y"]) + (0.5 * scaleY)):  # te wartości typu 0.5 albo 0.575 po prostu udało mi się znaleźć na zasadzie prób i błędów, nie radzę edytować xD
                try: # try i except gdyż czasami zdarza mu się wybrać za duży index y
                    # na podstawie położenia kursora znajduje nam wartości X, Y oraz Z kwadracika na który najechaliśmy myszką
                    text = (f"<span style='font-size: 12pt'>"
                            f"<span style='color: red'>"
                            f"x={round(data['Heatmap']['x'][round(mousePoint.x())], 4)}, </span>"
                            f"<span style='color: green'>"
                            f"y={round(data['Heatmap']['y'][math.floor(mousePoint.y())], 4)}, </span>"
                            f"<span style='color: blue'>"
                            f"z={round(data['Heatmap']['z'][math.floor(mousePoint.y())][round(mousePoint.x())], 4)}</span></span>")
                except IndexError:
                    pass
                label.setText(text)
            # ustawiamy pozycję linii na pozycje kursora
            vLine.setPos(mousePoint.x()) 
            hLine.setPos(mousePoint.y())

    plotItem.scene().sigMouseMoved.connect(mouseMoved)

    return gr_wid