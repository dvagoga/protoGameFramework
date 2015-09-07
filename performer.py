NAME_REPLACE_PREFIX = '@!!:'
NAME_REPLACE_CONSTANT = 'name' + NAME_REPLACE_PREFIX
TASK_FILE_NAME = 'currentTask.txt'
HTML_TEMPLATE_FILE_NAME = 'html_template.txt'
JS_TEMPLATE_FILE_NAME = 'js_template.txt'
JS_LIBRARY_FILE_NAME = 'js_lib.txt'

import os

def getTask():
    res = {'name':'', 'level':[]}
    with open(TASK_FILE_NAME, 'r') as taskFile:
        taskList = taskFile.readlines()

    res['name'] = taskList[0][0:-1]
    for i in range(1, len(taskList)):
        words = taskList[i].split()
        if words[0] == 'level:':
            res['level'].append({'o':[], 'f':[], 'cell':[]})
        elif words[0] == 'o:':
            res['level'][-1]['o'] += words[1:]
        elif words[0] == 'f:':
            res['level'][-1]['f'] += words[1:]
        elif words[0] == 'cell:':
            res['level'][-1]['cell'].append({'intersection':words[1:], 'f':[]})
        elif words[0] == 'p:':
            res['level'][-1]['cell'][-1]['f'].append({'index':words[1], 'operands':words[2:]})

    return res

def createFolder(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)

def createHtml(fileName):
    templateCode = []
    newCode = []
    with open(HTML_TEMPLATE_FILE_NAME, 'r') as htmlTemplateFile:
        templateCode = htmlTemplateFile.readlines()

    for line in templateCode:
        if NAME_REPLACE_CONSTANT in line:
            newCode.append(line.replace(NAME_REPLACE_CONSTANT, fileName))
        else:
            newCode.append(line)

    htmlFileName = fileName + '/' + fileName + '.html'

    with open(htmlFileName, 'w+', encoding='utf-8') as htmlFile:
        for line in newCode:
            htmlFile.write(line)

def createJs(fileName):
    templateCode = []
    newCode = []
    with open(JS_TEMPLATE_FILE_NAME, 'r') as jsTemplateFile:
        templateCode = jsTemplateFile.readlines()

    for line in templateCode:
        newCode.append(line)

    jsFileName = fileName + '/' + fileName + '.js'

    with open(jsFileName, 'w+', encoding='utf-8') as jsFile:
        for line in newCode:
            jsFile.write(line)

def addJsLib(levels):
    libCode = []
    newCode = []
    selectedNames = []

    def getSelectedNames(selectedNames, allNames):
        res = []
        for name in allNames:
            if name not in selectedNames:
                res.append(name)
        return res

    def codeFoundInLib(lib, name):
        res = []
        pattern = name + NAME_REPLACE_PREFIX
        libIndex = 0
        done = False
        soughtFor = False
        while libIndex < len(lib) or not done:
            st = lib[libindex].split
            if soughtFor:
                if st[0] == pattern:
                    done = True
                else:
                    res.append(lib[libindex])
            if st[0] == pattern:
                soughtFor = True
            libIndex += 1
        return res

    for l in levels:
        print(l)

    with open(JS_LIBRARY_FILE_NAME, 'r') as jsLibFile:
        libCode = jsLibFile.readlines()

    for level in levels:
        selectedNames += getSelectedNames(selectedNames, level.o) + getSelectedNames(selectedNames, level.f)

    for name in selectedNames:
        newCode += codeFoundInLib(libCode, name)

    print(newCode)

    #with open(jsFileName, 'a') as jsFile:
    #    for line in newCode:
    #        jsFile.write(line)

    
############################################################


task = getTask()
createFolder(task['name'])
createHtml(task['name'])
createJs(task['name'])
addJsLib(task['level'])
print('creating ' + task['name'] + ' done.')
