NAME_REPLACE_PREFIX = '@!!:'
NAME_REPLACE_CONSTANT = 'name' + NAME_REPLACE_PREFIX
TASK_FILE_NAME = 'currentTask.txt'
HTML_TEMPLATE_FILE_NAME = 'html_template.txt'
JS_TEMPLATE_FILE_NAME = 'js_template.txt'
JS_OBJ_LIBRARY_FILE_NAME = 'js_lib_obj.txt'
JS_FUN_LIBRARY_FILE_NAME = 'js_lib_fun.txt'

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
            res['level'][-1]['o'].append({'type':words[1], 'init':words[2:]})
        elif words[0] == 'f:':
            res['level'][-1]['f'] += words[1:]
        elif words[0] == 'cell:':
            res['level'][-1]['cell'].append({'intersection':words[1:], 'f':[]})
        elif words[0] == 'p:':
            res['level'][-1]['cell'][-1]['f'].append({'name':words[1], 'operands':words[2:]})

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

def createJs(fileName, types, funcs, levelConst, cells):
    templateCode = []
    newCode = []
    for im in cells:
        print(im)
    with open(JS_TEMPLATE_FILE_NAME, 'r') as jsTemplateFile:
        templateCode = jsTemplateFile.readlines()

    for line in templateCode:
        if 'typecmp'+NAME_REPLACE_PREFIX in line:
            for t in types:
                newCode.append('            if (level[levelIndex][i].type == "' + t + '"){o.push(new ' + t + '(level[levelIndex][i].init))}\n')
        elif 'funccmp'+NAME_REPLACE_PREFIX in line:
            for f in funcs:
                newCode.append('            ' + f + '();\n')
        elif 'level'+NAME_REPLACE_PREFIX in line:
            newCode.append('var level = ' + str(levelConst) + '\n');
        elif 'param'+NAME_REPLACE_PREFIX in line:
            newCode.append('    p = {"move":[]}\n');
        elif 'add'+NAME_REPLACE_PREFIX in line:
            for lvl in range(len(cells)):
                for c in cells[lvl]:
                    newCode.append('    if (levelIndex == ' + str(lvl) + ' && x == ' + c['intersection'][0] + ' && y == ' + c['intersection'][1] + '){')
                    for f in c['f']:
                        opr = ''
                        for op in f['operands']:
                            newCode.append('        p.' + f['name'] + '.push(o[' + op + '])\n')
                    newCode.append('}\n')
        else:
            newCode.append(line)

    jsFileName = fileName + '/' + fileName + '.js'

    with open(jsFileName, 'w+', encoding='utf-8') as jsFile:
        for line in newCode:
            jsFile.write(line)

def addJsLib(fileName, levels):
    libObjCode = []
    libFunCode = []
    newCode = ['/*\n', 'generated library\n', '*/\n']
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
        lastIndex = len(lib) - 1
        while libIndex < lastIndex and not done:
            st = lib[libIndex].split()
            checkName = st and st[0] == pattern
            if soughtFor:
                if checkName:
                    done = True
                else:
                    res.append(lib[libIndex])
            if checkName:
                soughtFor = True
            libIndex += 1
        return res

    with open(JS_OBJ_LIBRARY_FILE_NAME, 'r') as jsLibFile:
        libObjCode = jsLibFile.readlines()

    with open(JS_FUN_LIBRARY_FILE_NAME, 'r') as jsLibFile:
        libFunCode = jsLibFile.readlines()

    objs = []
    funs = []
    for level in levels:
        for obj in level['o']:
            objs.append(obj['type'])
        funs += level['f']

    for name in set(objs):
        newCode += codeFoundInLib(libObjCode, name)

    for name in set(funs):
        newCode += codeFoundInLib(libFunCode, name)

    jsFileName = fileName + '/' + fileName + '.js'
    with open(jsFileName, 'a') as jsFile:
        for line in newCode:
            jsFile.write(line)

    
############################################################


#task file parser
task = getTask()

#create folder
createFolder(task['name'])
#create html
createHtml(task['name'])
#create js
allPossibleTypes = []
allPossibleFunctions = []
jsLevelConst = []
intersectionCells = []
for l in task['level']:
    for t in l['o']:
        allPossibleTypes.append(t['type'])
    allPossibleFunctions += l['f']
    jsLevelConst.append(l['o'])
    intersectionCells.append(l['cell'])
createJs(task['name'], set(allPossibleTypes), set(allPossibleFunctions), jsLevelConst, intersectionCells)
#modify js
addJsLib(task['name'], task['level'])
print('creating ' + task['name'] + ' done.')
