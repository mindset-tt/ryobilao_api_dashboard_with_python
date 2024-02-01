from fastapi import Depends, Form
from fastapi.responses import JSONResponse
from config.connect import app, cursor, conp, auth_handler
from model.model import section


@app.get('/api/v1/task', tags=['ໜ້າວຽກ'])
async def getTask(empID=Depends(auth_handler.auth_wrapper)):
    try:
        cursor.execute(
            f"SELECT sectionId, projectId, sectionName, progress, DATE_FORMAT(fromDate, '%%Y-%%m-%%d') as fromDate, date_format(toDate, '%%Y-%%m-%%d') FROM Section")
        taskRows = cursor.fetchall()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ດຶງຂໍ້ມູນໜ້າວຽກສຳເລັດ',
                "section": taskRows}
        )

    except Exception as e:
        return e


@app.post('/api/v1/task', tags=['ໜ້າວຽກ'])
async def insertTask(task: section,empID=Depends(auth_handler.auth_wrapper)
                     ):
    try:
        cursor.execute("INSERT INTO Section VALUES(sectionId, projectId, sectionName, progress, fromDate, toDate, createdBy, updateBy) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (task.sectionId, task.projectId, task.sectionName, task.progress, task.fromDate, task.toDate, task.createdBy, task.updateBy))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ເພີ່ມຂໍ້ມູນໜ້າວຽກສຳເລັດ', }
        )

    except Exception as e:
        return e


@app.put('/api/v1/task', tags=['ໜ້າວຽກ'])
async def updateTask(taskmg: section,empID=Depends(auth_handler.auth_wrapper)
                     ):
    try:
        cursor.execute("UPDATE Section SET sectionName = %s, updateBy = %s, progress = %s, \
                       fromDate =%s, toDate = %s, projectId = %s, updateAt = NOW() WHERE sectionId = %s",
                       (taskmg.sectionName, taskmg.updateBy, taskmg.progress, taskmg.fromDate, taskmg.toDate, taskmg.projectId, taskmg.sectionId))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ແກ້ໄຂຂໍ້ມູນໜ້າວຽກສຳເລັດ', }
        )

    except Exception as e:
        return e


@app.delete('/api/v1/task', tags=['ໜ້າວຽກ'])
async def deleteTask(sectionId: str, empID=Depends(auth_handler.auth_wrapper)):
    try:
        cursor.execute(
            "DELETE FROM Section WHERE sectionId = %s", (sectionId))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ລົບຂໍ້ມູນໜ້າວຽກສຳເລັດ', }
        )

    except Exception as e:
        return e


@app.get('/api/v1/task/{sectionId}', tags=['ໜ້າວຽກ'])
async def getTaskById(sectionId: str, empID=Depends(auth_handler.auth_wrapper)):
    try:
        cursor.execute(
            f"SELECT sectionId, projectId, sectionName, progress, DATE_FORMAT(fromDate, '%%Y-%%m-%%d') as fromDate, date_format(toDate, '%%Y-%%m-%%d') FROM Section WHERE sectionId = %s", (sectionId))
        taskRows = cursor.fetchone()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ດຶງຂໍ້ມູນໜ້າວຽກສຳເລັດ',
                "section": taskRows}
        )

    except Exception as e:
        return e
