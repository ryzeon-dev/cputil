import time

import PyQt6 as pyqt

from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer, QThread
from PyQt6.QtGui import *


import json
import subprocess

from _thread import start_new_thread

from sympy.physics.wigner import wigner_3j

from custom_widgets import *
from cputil_data import TOPOLOGY, PROCESSOR_KEYS, update

class ThreadedWorker(QThread):
    def __init__(self, origin):
        self.origin = origin
        super().__init__(origin)

    def run(self):
        while True:
            update()
            print('updated')

            for widget in self.origin.usageRows:
                if not isinstance(widget, UsageRow):
                    continue

                print(widget.id)
                data = J_DATA[f'processor{widget.id}']
                widget.updateContent(data['usage'], data['frequency'])
                widget.update()

            self.origin.usageScrollAreaLayout.update()
            self.origin.usageScrollAreaWidget.update()
            self.origin.usageTab.update()

            time.sleep(1)

def makeRoEntry(value):
    entry = QTextEdit()
    entry.setText(str(value))
    entry.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
    entry.setMaximumHeight(30)

    entry.setReadOnly(True)
    return entry

def makeSquaredGridFrame(label):
    frame = QFrame()
    layout = QGridLayout()

    layout.addWidget(QLabel(label), 0, 0)

    frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
    frame.setLayout(layout)

    return frame, layout

def makeSquaredVFrame():
    frame = QFrame()
    layout = QVBoxLayout()

    frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)

    frame.setLayout(layout)
    return frame, layout

def makeSquaredHFrame(label):
    frame = QFrame()
    layout = QHBoxLayout()

    layout.addWidget(QLabel(label))
    frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)

    frame.setLayout(layout)
    return frame, layout

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.jData = None
        self.processorKeys = {}
        self.updateData()

        self.setWindowTitle('QtCputil')
        self.setMinimumSize(1440, 600)

        self.mainFrame = QTabWidget()

        self.performanceTab = QWidget()
        self.infoTab = QWidget()
        self.usageTab = QWidget()

        self.mainFrame.addTab(self.performanceTab, 'Performance')
        self.mainFrame.addTab(self.infoTab, 'Info')
        self.mainFrame.addTab(self.usageTab, 'Usage')

        self.makePerformanceTab()
        self.makeInfoTab()
        self.makeUsageTab()

        self.setCentralWidget(self.mainFrame)

    def updateData(self):
        output = subprocess.getoutput('/usr/local/bin/cputil json')
        self.jData = json.loads(output)

        for key in self.jData.keys():
            if key.startswith('processor'):
                n = int(key.replace('processor', ''))
                self.processorKeys[n] = key

    def makePerformanceTab(self):
        self.performanceTabLayout = QVBoxLayout()

        self.topGridWidget = QWidget()
        self.topGrid = QGridLayout()
        self.topGrid.addWidget(QLabel('Available\nGovernors'), 0, 0)
        self.topGrid.addWidget(QLabel('Available\nScaling Frequencies'), 0, 1)
        self.topGrid.addWidget(QLabel('Available\nEnergy Performance Preferences'), 0, 2)

        self.governorsArea = QTextEdit()
        self.governorsArea.setText('\n'.join(self.jData.get('governors')))
        self.governorsArea.setReadOnly(True)
        self.governorsArea.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.governorsArea.adjustSize()
        self.topGrid.addWidget(self.governorsArea, 1, 0)

        self.frequenciesArea = QTextEdit()
        self.frequenciesArea.setText('\n'.join(str(f) for f in self.jData.get('scaling frequencies')))
        self.frequenciesArea.setReadOnly(True)
        self.frequenciesArea.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.frequenciesArea.adjustSize()
        self.topGrid.addWidget(self.frequenciesArea, 1, 1)

        self.performancePreferencesArea = QTextEdit()
        self.performancePreferencesArea.setText('\n'.join(self.jData.get('energy performance preferences')))
        self.performancePreferencesArea.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.performancePreferencesArea.adjustSize()
        self.performancePreferencesArea.setReadOnly(True)
        self.topGrid.addWidget(self.performancePreferencesArea, 1, 2)

        self.policiesScrollView = QScrollArea()
        self.policiesWidget = QWidget()
        self.policiesLayout = QVBoxLayout()

        for n, key in self.processorKeys.items():
            policy = self.jData[key]
            self.policiesLayout.addWidget(GovernorPolicy(n, policy['governor'], policy['minimum scaling frequency'], policy['maximum scaling frequency'], policy['energy performance preference']))

        self.policiesWidget.setLayout(self.policiesLayout)
        self.policiesScrollView.setWidget(self.policiesWidget)

        self.topGridWidget.setLayout(self.topGrid)
        self.performanceTabLayout.addWidget(self.topGridWidget)
        self.performanceTabLayout.addWidget(self.policiesScrollView)
        self.performanceTab.setLayout(self.performanceTabLayout)

    def makeInfoTab(self):
        layout = QVBoxLayout()
        layout.setSpacing(1)

        gridwidget = QWidget()
        gridLayout = QGridLayout()

        row = 0
        col = 0

        if (model := J_DATA['model name']):
            gridLayout.addWidget(QLabel('CPU Model'), row, col % 4)
            gridLayout.addWidget(makeRoEntry(model), row, (col+1) % 4)
            col += 2

        if (architecture := J_DATA['architecture']):
            gridLayout.addWidget(QLabel('Architecture'), row, col % 4)
            gridLayout.addWidget(makeRoEntry(architecture), row, (col+1) % 4)
            col += 2

            if not col % 4:
                row += 1

        if (coreCount := J_DATA['core count']):
            gridLayout.addWidget(QLabel('Cores count'), row, col % 4)
            gridLayout.addWidget(makeRoEntry(coreCount), row, (col+1) % 4)
            col += 2

            if not col % 4:
                row += 1

        if (threadCount := J_DATA['thread count']):
            gridLayout.addWidget(QLabel('Threads count'), row, col % 4)
            gridLayout.addWidget(makeRoEntry(threadCount), row, (col+1) % 4)
            col += 2

            if not col % 4:
                row += 1

        if (clockBoost := J_DATA['clock boost']):
            gridLayout.addWidget(QLabel('Clock Boost'), row, col % 4)
            gridLayout.addWidget(makeRoEntry(clockBoost), row, (col+1) % 4)
            col += 2

            if not col % 4:
                row += 1

        if (minClock := J_DATA['minimum frequency']):
            gridLayout.addWidget(QLabel('Minimum Clock'), row, col % 4)
            gridLayout.addWidget(makeRoEntry(f'{minClock / 1000} GHz'), row, (col+1) % 4)
            col += 2

            if not col % 4:
                row += 1

        if (maxClock := J_DATA['maximum frequency']):
            gridLayout.addWidget(QLabel('Maximum Clock'), row, col % 4)
            gridLayout.addWidget(makeRoEntry(f'{maxClock / 1000} GHz'), row, (col+1) % 4)
            col += 2

            if not col % 4:
                row += 1

        if (pStateStatus := J_DATA['amd-p-state-status']):
            gridLayout.addWidget(QLabel('AMD P-State Status'), row, col % 4)
            gridLayout.addWidget(makeRoEntry(pStateStatus), row, (col+1) % 4)
            col += 2

            if not col % 4:
                row += 1

        if (pStatePrefcore := J_DATA['amd-p-state-prefcore']):
            gridLayout.addWidget(QLabel('AMD P-State Prefcore'), row, col % 4)
            gridLayout.addWidget(makeRoEntry(pStatePrefcore), row, (col+1) % 4)
            col += 2

            if not col % 4:
                row += 1

        gridwidget.setLayout(gridLayout)
        layout.addWidget(gridwidget)

        scrollArea = QScrollArea()
        scrollAreaWidget = QWidget()
        scrollAreaLayout = None #QVBoxLayout()

        for outerGroup in TOPOLOGY:
            inner = TOPOLOGY[outerGroup]

            if isinstance(inner, dict):
                if scrollAreaLayout is None:
                    scrollAreaLayout = QVBoxLayout()

                outerFrame, outerLayout = makeSquaredGridFrame(f'Die {outerGroup}')

                outerCol = 0
                for core in sorted(inner.keys()):
                    coreFrame, coreLayout = makeSquaredGridFrame(f'Core {core}')

                    innerFrame, innerLayout = makeSquaredVFrame()
                    for thread in sorted(inner[core]):
                        innerLayout.addWidget(QLabel(f'Processor {thread}'))

                    coreLayout.addWidget(innerFrame, 1, 0)

                    outerLayout.addWidget(coreFrame, 1, outerCol)
                    outerCol += 1

            else:
                if scrollAreaLayout is None:
                    scrollAreaLayout = QHBoxLayout()

                outerFrame, outerLayout = makeSquaredGridFrame(f'Die {outerGroup}')
                innerFrame, innerLayout = makeSquaredVFrame()

                for thread in sorted(inner):
                    innerLayout.addWidget(QLabel(f'Processor {thread}'))

                outerLayout.addWidget(innerFrame, 1, 0)
            scrollAreaLayout.addWidget(outerFrame)

        scrollAreaWidget.setLayout(scrollAreaLayout)
        scrollArea.setWidget(scrollAreaWidget)
        layout.addWidget(scrollArea)

        self.infoTab.setLayout(layout)

    def makeUsageTab(self):
        usageLayout = QVBoxLayout()
        scrollArea = QScrollArea()

        self.usageScrollAreaWidget = QWidget()
        self.usageScrollAreaLayout = QVBoxLayout()

        self.usageRows = []
        for id, key in PROCESSOR_KEYS.items():
            row = UsageRow(id, J_DATA[key]['usage'], J_DATA[key]['frequency'])
            self.usageRows.append(row)
            self.usageScrollAreaLayout.addWidget(row)

        self.usageScrollAreaWidget.setLayout(self.usageScrollAreaLayout)
        scrollArea.setWidget(self.usageScrollAreaWidget)

        usageLayout.addWidget(scrollArea)
        self.usageTab.setLayout(usageLayout)

        # timer = QTimer(self)
        # timer.setInterval(1000)
        # timer.timeout.connect(self.renderUsage)
        # timer.start()

        threadedWorker = ThreadedWorker(self)
        threadedWorker.start()


    def renderUsage(self):
        update()
        print('updated')

        for widget in self.usageScrollAreaWidget.children():
            if not isinstance(widget, UsageRow):
                continue

            print(widget.id)
            data = J_DATA[f'processor{widget.id}']
            widget.updateContent(data['usage'], data['frequency'])
            widget.update()

        self.usageScrollAreaLayout.update()
        self.usageScrollAreaWidget.update()
        self.usageTab.update()

        time.sleep(1)

if __name__ == '__main__':
    app = QApplication([])
    i = Interface()
    i.show()
    app.exec()