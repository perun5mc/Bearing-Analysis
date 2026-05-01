import numpy as np

from PyQt5 import QtCore

import pyqtgraph as pg
import colorsys

def createGraph(valuesAll, names, harmonics, type):
    win = pg.GraphicsLayoutWidget(show=False)
    win.setBackground("white")

    label = pg.LabelItem(justify='center')
    label.setText(f"<span style='font-size: 12pt;color: none'>‎</span>") # dodaję pustą linijkę w miejscu normalnego labela
    win.addItem(label)

    p1 = win.addPlot(row=1, col=0)
    p1.avgPen = pg.mkPen('#FFFFFF')
    p1.avgShadowPen = pg.mkPen('#8080DD', width=10)
    labelStyle = {'color': 'black;', 'font-size': '15px; padding: 5px;'}
    if type == "ACC":
        p1.getAxis('left').setLabel('Amplitude', units='G', **labelStyle)
    else:
        p1.getAxis('left').setLabel('Amplitude', units='m/s', **labelStyle)

    p1.getAxis('left').setTextPen('black')
    p1.getAxis('bottom').setLabel('Frequency', units='Hz', **labelStyle)
    p1.getAxis('bottom').setTextPen('black')

    region = pg.LinearRegionItem()
    region.setZValue(10)
    p1.setAutoVisible(y=True)

    legend = pg.LegendItem((80, 60), offset=(-1, 1), labelTextColor='black', labelTextSize='15px', colCount=3)
    legend.setParentItem(p1.graphicsItem())
    itemsList = []
    for i in range(len(valuesAll)):
        x = valuesAll[i][0][0]
        y = valuesAll[i][0][1]
        y = y[:int(len(y) / 2)]
        data1 = [x, y]
        color = colorsys.hsv_to_rgb(((360 / len(valuesAll)) * (i + 1) + 60) / 360, 1, 0.85)
        newColor = (color[0] * 255, color[1] * 255, color[2] * 255)
        pen = pg.mkPen(color=newColor, width=1)
        item = p1.plot(x, y, pen=pen, name=names[i])
        itemsList.append(item)
        legend.addItem(item, names[i])
    maxValues = []
    for value in valuesAll:
        val = max(value[0][1])
        maxValues.append(val)
    maxValue = max(maxValues)


    if harmonics > 0: # funkcja dodaje harmoniczne i sprawia, że harmonicsy o tych samych wartościach X mają ten sam kolor. Nie nakłada ich także na siebie (pomija je)
        value = valuesAll[0]
        if len(value[1]) > 0:
            uniqueHarmonics = {}
            for i in range(len(value[1])):
              uniqueHarmonics[value[1][i][0][0]] = ""
            keys = list(uniqueHarmonics.keys())
            for i in range(len(keys)):
              color = colorsys.hsv_to_rgb(((340 / (len(keys))) * (i)) / 360, 1, 1)
              newColor = (color[0] * 255, color[1] * 255, color[2] * 255, 120)
              uniqueHarmonics[keys[i]] = newColor
            alreadyPlaced = []
            for i in range(len(value[1])): 
                # print(value[1][i][0])
                for j in range(harmonics):
                    pos = value[1][i][0][0] + (j * value[1][i][0][0])
                    if not alreadyPlaced.__contains__(pos):
                        item = p1.plot([pos, pos], [0, maxValue],
                                     pen=pg.mkPen(color=uniqueHarmonics[value[1][i][0][0]], width=2, style=QtCore.Qt.DotLine),
                                     name=value[1][i][3], ignoreBounds=True)
                        alreadyPlaced.append(pos)
                    else:
                        item = p1.plot([0, 0], [0, 0],
                                       pen=pg.mkPen(color=uniqueHarmonics[value[1][i][0][0]], width=2,
                                                    style=QtCore.Qt.DotLine),
                                       name=value[1][i][3], ignoreBounds=True)
                    if j == 0:
                            legend.addItem(item, value[1][i][3])

    p1.autoRange(padding=None, items=itemsList)

    p1.autoBtn.clicked.connect(lambda: p1.autoRange(padding=None, items=itemsList))

    p1.setDefaultPadding(0)
    vLine = pg.InfiniteLine(angle=90, movable=False)
    hLine = pg.InfiniteLine(angle=0, movable=False)
    p1.addItem(vLine, ignoreBounds=True)
    p1.addItem(hLine, ignoreBounds=True)
    p1.getAxis('left').setGrid(50)
    p1.getAxis('bottom').setGrid(50)

    vb = p1.vb

    def mouseMoved(evt):
        pos = evt
        if p1.sceneBoundingRect().contains(pos):
            mousePoint = vb.mapSceneToView(pos)
            index = mousePoint.x()
            text = f"<span style='font-size: 12pt; color: black;'>x={round(mousePoint.x(), 2)}"
            if index > 0 and index < len(data1[0]):
                for i in range(len(valuesAll)):
                    x = valuesAll[i][0][0]
                    y = valuesAll[i][0][1]
                    y = y[:int(len(y) / 2)]
                    color = colorsys.hsv_to_rgb(((360 / len(valuesAll)) * (i + 1) + 60) / 360, 1, 0.85)
                    newColor = (color[0] * 255, color[1] * 255, color[2] * 255)
                    if type == "ACC":
                        text = f"{text}, <span style='color: rgb{newColor}'>y<sub>{i}</sub>={round(np.interp(mousePoint.x(), x, y), 3)}G</span>"
                    else:
                        text = f"{text}, <span style='color: rgb{newColor}'>y<sub>{i}</sub>={round(np.interp(mousePoint.x(), x, y) * 1000, 3)}mm/s</span>"
                label.setText(text)
            vLine.setPos(mousePoint.x())
            hLine.setPos(mousePoint.y())

    p1.scene().sigMouseMoved.connect(mouseMoved)

    return win