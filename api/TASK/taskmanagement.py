from fastapi import Depends, Form
from fastapi.responses import JSONResponse
from auth.auth import AuthHandler
from config.connect import app, cursor, conp
from model.model import taskmanagement


@app.get('/api/v1/task', tags=['ໜ້າວຽກຍ່ອຍ'])
async def getTask(empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute(
            f"SELECT Task_Id, sectionId, taskName, progress, DATE_FORMAT(fromDate, '%Y-%m-%d') as fromDate, date_format(toDate, '%Y-%m-%d') as toDate FROM TaskManageement")
        taskRows = cursor.fetchall()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ດຶງຂໍ້ມູນໜ້າວຽກຍ່ອຍສຳເລັດ',
                "task": taskRows}
        )
    except Exception as e:
        return e


@app.post('/api/v1/task', tags=['ໜ້າວຽກຍ່ອຍ'])
async def insertTask(task: taskmanagement,empID=Depends(AuthHandler.auth_wrapper)
                     ):
    try:
        cursor.execute("INSERT INTO TaskManageement VALUES(Task_Id, sectionId, taskName, progress, fromDate, toDate, createdBy, updateBy) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (task.taskId, task.sectionId, task.taskName, task.progress, task.fromDate, task.toDate, task.createdBy, task.updateBy))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ເພີ່ມຂໍ້ມູນໜ້າວຽກສຳເລັດ', }
        )
    except Exception as e:
        return e


@app.put('/api/v1/task', tags=['ໜ້າວຽກຍ່ອຍ'])
async def updateTask(taskmg: taskmanagement, empID=Depends(AuthHandler.auth_wrapper)
                     ):
    try:
        cursor.execute("UPDATE TaskManageement SET taskName = %s, updateBy = %s, sectionId = %s, progress = %s, \
                       fromDate =%s, toDate = %s, updateAt = NOW() WHERE Task_Id = %s",
                       (taskmg.taskName, taskmg.updateBy, taskmg.sectionId, taskmg.progress, taskmg.fromDate, taskmg.toDate, taskmg.taskId))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ແກ້ໄຂຂໍ້ມູນໜ້າວຽກສຳເລັດ', }
        )
    except Exception as e:
        return e


@app.delete('/api/v1/task', tags=['ໜ້າວຽກຍ່ອຍ'])
async def deleteTask(taskId: str,empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute(
            "DELETE FROM TaskManageement WHERE Task_Id = %s", (taskId))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ລົບຂໍ້ມູນໜ້າວຽກສຳເລັດ', }
        )
    except Exception as e:
        return e


@app.get('/api/v1/task/{taskId}', tags=['ໜ້າວຽກຍ່ອຍ'])
async def getTaskById(taskId: str, empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute(
            f"SELECT Task_Id, sectionId, taskName, progress, DATE_FORMAT(fromDate, '%Y-%m-%d') as fromDate, date_format(toDate, '%Y-%m-%d') as toDate FROM TaskManageement WHERE Task_Id = %s", (taskId))
        taskRows = cursor.fetchone()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ດຶງຂໍ້ມູນໜ້າວຽກຍ່ອຍສຳເລັດ',
                "task": taskRows}
        )

    except Exception as e:
        return e
