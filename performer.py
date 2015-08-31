NAME_REPLACE_CONSTANT = 'name@!!:'

import os

def getTask():
    with open('currentTask.txt', 'r') as taskFile:
        taskList = taskFile.readlines()

    return {'name':taskList[0], 'objects':taskList[1:]}

def createFolder(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)

def createHtml(fileName):
    templateCode = []
    newCode = []
    with open('html_template.txt', 'r') as htmlTemplateFile:
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
    with open('js_template.txt', 'r') as jsTemplateFile:
        templateCode = jsTemplateFile.readlines()

    for line in templateCode:
        newCode.append(line)

    jsFileName = fileName + '/' + fileName + '.js'

    with open(jsFileName, 'w+', encoding='utf-8') as jsFile:
        for line in newCode:
            jsFile.write(line)


############################################################


task = getTask()
createFolder(task['name'])
createHtml(task['name'])
createJs(task['name'])
print('creating ' + task['name'] + ' done.')
