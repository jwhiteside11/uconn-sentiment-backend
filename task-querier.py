def getTaskList():
    return

def requestTaskForVM():
    return

def outputTask():
    return

taskList = getTaskList()

pendingTasks = [e for e in taskList if e['Status'] is "Pending"]

outputTask(requestTaskForVM(pendingTasks.pop()))