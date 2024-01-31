from fastapi import Form
from fastapi.responses import UJSONResponse
from config.connect import app, cursor, conp
from model.model import taskmanagement


@app.get('/api/v1/task', tags=['ໜ້າວຽກ'], response_class=UJSONResponse)
async def getTask():
    try:
        cursor.execute("SELECT * FROM TaskManageement")
        taskRows = cursor.fetchall()
        print(taskRows)
        return taskRows

    except Exception as e:
        return e


@app.post('/api/v1/task', tags=['ໜ້າວຽກ'], response_class=UJSONResponse)
async def insertTask(task: taskmanagement,
                     ):
    try:
        cursor.execute("INSERT INTO TaskManageement VALUES(TaskManageement_Id, projectId, sectionName, taskName, progress, fromDate, toDate, createdBy, updateBy) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (task.taskId, task.projectId, task.sectionName, task.taskName, task.progress, task.fromDate, task.toDate, task.createdBy, task.updateBy))
        conp.commit()
        return {"message": "Insert Success"}

    except Exception as e:
        return e


@app.put('/api/v1/task', tags=['ໜ້າວຽກ'], response_class=UJSONResponse)
async def updateTask(taskmg: taskmanagement
                     ):
    try:
        cursor.execute("UPDATE TaskManageement SET taskName = %s, updateBy = %s, sectionName = %s, progress = %s, \
                       fromDate =%s, toDate = %s, projectId = %s, updateAt = NOW() WHERE taskId = %s",
                       (taskmg.taskName, taskmg.updateBy, taskmg.sectionName, taskmg.progress, taskmg.fromDate, taskmg.toDate, taskmg.projectId, taskmg.taskId))
        conp.commit()
        return {"message": "Update Success"}

    except Exception as e:
        return e


@app.delete('/api/v1/task', tags=['ໜ້າວຽກ'], response_class=UJSONResponse)
async def deleteTask(taskId: str):
    try:
        cursor.execute(
            "DELETE FROM TaskManageement WHERE taskId = %s", (taskId))
        conp.commit()
        return {"message": "Delete Success"}

    except Exception as e:
        return e


@app.get('/api/v1/task/{taskId}', tags=['ໜ້າວຽກ'], response_class=UJSONResponse)
async def getTaskById(taskId: str):
    try:
        cursor.execute(
            "SELECT * FROM TaskManageement WHERE taskId = %s", (taskId))
        taskRows = cursor.fetchone()
        return taskRows

    except Exception as e:
        return e
