from subprocess import getstatusoutput

def grep(target, pattern, returnFirstMatch=False, count=False, ignoreCase=False):
    res = []

    if isinstance(target, list):
        chunks = target

    elif isinstance(target, str):
        chunks = target.split('\n')

    for chunk in chunks:
        if ignoreCase:
            match = pattern.lower() in chunk.lower()

        else:
            match = pattern in chunk

        if match:
            if returnFirstMatch:
                return chunk

            res.append(chunk)

    if count:
        return len(res)

    return res if len(res) > 1 else (None if len(res) == 0 else res[0])

def terminal(cmd):
    statusCode, output = getstatusoutput(cmd)

    if statusCode != 0:
        raise Exception('Non 0 return code from console')

    return output

def readFile(path):
    with open(path, 'r') as file:
        content = file.read()
    return content.strip()