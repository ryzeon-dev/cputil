from lib_cputil import *
from conf import *

while True:
    try:
        governor, minScalingFreq, maxScalingFreq = parseConf(confFilePath)

    except:
        time.sleep(60)
        continue

    if governor is not None and governor != 'auto':
        setGovernor(governor, True)

    if minScalingFreq is not None and minScalingFreq != 'auto':
        setMinimumScalingFrequency(minScalingFreq, True)

    if maxScalingFreq is not None and maxScalingFreq != 'auto':
        setMaximumScalingFrequency(maxScalingFreq, True)

    time.sleep(60)