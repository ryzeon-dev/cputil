from lib_cputil import *
from conf import *

while True:
    try:
        governor, minScalingFreq, maxScalingFreq, pollingInterval = parseConf(confFilePath)

    except:
        time.sleep(10)
        continue

    if governor is not None and governor != 'auto':
        setGovernor(governor, True)

    if minScalingFreq is not None and minScalingFreq != 'auto':
        setMinimumScalingFrequency(minScalingFreq, True)

    if maxScalingFreq is not None and maxScalingFreq != 'auto':
        setMaximumScalingFrequency(maxScalingFreq, True)

    time.sleep(int(pollingInterval) if pollingInterval is not None else 10)
