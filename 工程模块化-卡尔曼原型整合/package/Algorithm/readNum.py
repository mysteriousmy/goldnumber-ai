def readFile(userInfoFile):
    strs = ''
    lists = []
    with open(userInfoFile) as f:
        strs = f.read()
    for i in strs.split(','):
        lists.append(float(i))
    return lists