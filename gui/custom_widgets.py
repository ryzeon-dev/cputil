from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame, QComboBox, QGridLayout, QProgressBar
from PyQt6.QtCore import Qt
from cputil_data import J_DATA
import os

class GovernorPolicy(QWidget):
    def __init__(self, policy, governor, minFreq, maxFreq, energyPreference, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.policy = policy

        self.layout = QHBoxLayout()
        self.layout.addWidget(QLabel(f'Policy {policy}:'))

        ### GOVERNOR ###

        governorFrame = QFrame()
        governorFrame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)

        governorFrameLayout = QHBoxLayout()
        governorFrameLayout.addWidget(QLabel('Governor'))

        self.governorComboBox = QComboBox()
        for g in J_DATA['governors']:
            self.governorComboBox.addItem(g)
        self.governorComboBox.setCurrentText(governor)
        self.governorComboBox.currentTextChanged.connect(self.setGovernor)

        governorFrameLayout.addWidget(self.governorComboBox)
        governorFrame.setLayout(governorFrameLayout)

        self.layout.addWidget(governorFrame)

        ### MAX FREQ ###
        maxFreqFrame = QFrame()
        maxFreqFrame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)

        maxFreqFrameLayout = QHBoxLayout()
        maxFreqFrameLayout.addWidget(QLabel('Maximum Scaling Frequency'))

        self.maxFreqComboBox = QComboBox()
        for f in J_DATA['scaling frequencies']:
            self.maxFreqComboBox.addItem(str(f))
        self.maxFreqComboBox.setCurrentText(str(maxFreq))
        self.maxFreqComboBox.currentTextChanged.connect(self.setMaxFreq)

        maxFreqFrameLayout.addWidget(self.maxFreqComboBox)
        maxFreqFrame.setLayout(maxFreqFrameLayout)
        self.layout.addWidget(maxFreqFrame)

        ### MIN FREQ ###
        minFreqFrame = QFrame()
        minFreqFrame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)

        minFreqFrameLayout = QHBoxLayout()
        minFreqFrameLayout.addWidget(QLabel('Minimum Scaling Frequency'))

        self.minFreqComboBox = QComboBox()
        for f in J_DATA['scaling frequencies']:
            self.minFreqComboBox.addItem(str(f))
        self.minFreqComboBox.setCurrentText(str(minFreq))
        self.minFreqComboBox.currentTextChanged.connect(self.setMinFreq)

        minFreqFrameLayout.addWidget(self.minFreqComboBox)
        minFreqFrame.setLayout(minFreqFrameLayout)
        self.layout.addWidget(minFreqFrame)

        ### EPP ###

        energyPerformancePreferenceFrame = QFrame()
        energyPerformancePreferenceFrame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)

        energyPerformancePreferenceFrameLayout = QHBoxLayout()
        energyPerformancePreferenceFrameLayout.addWidget(QLabel('Energy Performance Preference'))

        self.energyPerformancePreferenceComboBox = QComboBox()
        for f in J_DATA['energy performance preferences']:
            self.energyPerformancePreferenceComboBox.addItem(str(f))
        self.energyPerformancePreferenceComboBox.setCurrentText(str(energyPreference))
        self.energyPerformancePreferenceComboBox.currentTextChanged.connect(self.setEnergyPerformancePreference)

        energyPerformancePreferenceFrameLayout.addWidget(self.energyPerformancePreferenceComboBox)
        energyPerformancePreferenceFrame.setLayout(energyPerformancePreferenceFrameLayout)
        self.layout.addWidget(energyPerformancePreferenceFrame)

        self.setLayout(self.layout)

    def setGovernor(self, governor):
        os.system(f'ssh-askpass | /usr/bin/sudo /usr/local/bin/cputil sg {governor} -cpu {self.policy}')

    def setMinFreq(self, freq):
        os.system(f'ssh-askpass | /usr/bin/sudo /usr/local/bin/cputil sfm {freq} -cpu {self.policy}')

    def setMaxFreq(self, freq):
        os.system(f'ssh-askpass | /usr/bin/sudo /usr/local/bin/cputil sfM {freq} -cpu {self.policy}')

    def setEnergyPerformancePreference(self, epp):
        os.system(f'ssh-askpass | /usr/bin/sudo /usr/local/bin/cputil sep {epp} -cpu {self.policy}')

class UsageRow(QFrame):
    def __init__(self, processorId, usage, frequency):
        super().__init__()
        self.usage = usage
        self.id = processorId

        self.layout = QGridLayout()

        self.layout.addWidget(QLabel(f'Processor {processorId}'), 0, 0)

        self.usageBar = QProgressBar()
        self.usageBar.setValue(round(usage['total']))
        self.usageBar.setMinimumWidth(700)
        self.layout.addWidget(self.usageBar, 0, 1, 1, 5, Qt.AlignmentFlag.AlignHCenter)

        self.freqLabel = QLabel(f'@ {frequency / 1000} GHz')
        self.layout.addWidget(self.freqLabel, 0, 6)

        self.userLabel = QLabel(f'User: {usage["user"]} %')
        self.layout.addWidget(self.userLabel, 1, 0)

        self.niceLabel = QLabel(f'Nice: {usage["nice"]} %')
        self.layout.addWidget(self.niceLabel, 1, 1)

        self.idleLabel = QLabel(f'Idle: {usage["idle"]} %')
        self.layout.addWidget(self.idleLabel, 1, 2)

        self.systemLabel = QLabel(f'System: {usage["system"]} %')
        self.layout.addWidget(self.systemLabel, 1, 3)

        self.iowaitLabel = QLabel(f'Iowait: {usage["iowait"]} %')
        self.layout.addWidget(self.iowaitLabel, 1, 4)

        self.interruptLabel = QLabel(f'Interrupt: {usage["interrupt"]} %')
        self.layout.addWidget(self.interruptLabel, 1, 5)

        self.softInterruptLabel = QLabel(f'Soft Interrupt: {usage["soft-interrupt"]} %')
        self.layout.addWidget(self.softInterruptLabel, 1, 6)

        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setLayout(self.layout)

    def updateContent(self, usage, freq):
        self.usageBar.setValue(round(usage['total']))
        self.usageBar.update()

        self.freqLabel.setText(f'@ {freq / 1000} GHz')
        self.userLabel.setText(f'User: {usage["user"]} %')
        self.niceLabel.setText(f'Nice: {usage["nice"]} %')
        self.idleLabel.setText(f'Idle: {usage["idle"]} %')
        self.systemLabel.setText(f'System: {usage["system"]} %')
        self.iowaitLabel.setText(f'Iowait: {usage["iowait"]} %')
        self.interruptLabel.setText(f'Interrupt: {usage["interrupt"]} %')
        self.softInterruptLabel.setText(f'Soft Interrupt: {usage["soft-interrupt"]} %')

        self.layout.update()
        self.update()
        print(f'{self.id} updated')
