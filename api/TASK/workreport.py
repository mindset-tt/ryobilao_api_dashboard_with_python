from fastapi import Depends, Form
from fastapi.responses import JSONResponse
from config.connect import app, cursor, conp, auth_handler
from model.model import workreport


@app.get('/api/v1/workreport', tags=['ລາຍງານວຽກ'])
async def getWorkreport(empID=Depends(auth_handler.auth_wrapper)):
    try:
        cursor.execute(f"SELECT Id, empId, TaskId, DATE_FORMAT(dateBegin, '%%Y-%%m-%%d') as date_start, DATE_FORMAT(dateEnd, '%%Y-%%m-%%d') as date_end,\
                        code_row_per_day, doc_page_per_day, progress, workDescription FROM Work_Record")
        workRows = cursor.fetchall()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ດຶງຂໍ້ມູນລາຍງານວຽກສຳເລັດ',
                "workreport": workRows}
        )

    except Exception as e:
        return e


@app.post('/api/v1/workreport', tags=['ລາຍງານວຽກ'])
async def insertWorkreport(workrp: workreport,empID=Depends(auth_handler.auth_wrapper)):
    try:
        cursor.execute("INSERT INTO Work_Record VALUES(Id, Task_Id, empId, dateBegin, dateEnd, code_row_per_day, doc_page_per_day, progress, \
                       workDescription, createdBy, updatedBy) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
                       (workrp.workId, workrp.Task_Id, workrp.empId, workrp.dateBegin, workrp.dateEnd,
                        workrp.code_row_per_day, workrp.doc_page_per_day, workrp.progress, workrp.workDescription, workrp.createdBy, workrp.updateBy))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ດຶງຂໍ້ມູນລາຍງານວຽກສຳເລັດ',
                }
        )
    except Exception as e:
        return e


@app.put('/api/v1/workreport', tags=['ລາຍງານວຽກ'])
async def updateWorkreport(workrp: workreport,empID=Depends(auth_handler.auth_wrapper)):
    try:
        cursor.execute("UPDATE Work_Record SET Task_Id=%s, empId=%s, dateBegin=%s, dateEnd=%s, code_row_per_day=%s, doc_page_per_day=%s, progress=%s, \
                       workDescription=%s, updatedBy=%s WHERE workId=%s",
                       (workrp.Task_Id, workrp.empId, workrp.dateBegin, workrp.dateEnd, workrp.code_row_per_day,
                        workrp.doc_page_per_day, workrp.progress, workrp.workDescription, workrp.updateBy, workrp.workId))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ດຶງຂໍ້ມູນລາຍງານວຽກສຳເລັດ',
                }
        )
    except Exception as e:
        return e


@app.delete('/api/v1/workreport', tags=['ລາຍງານວຽກ'])
async def deleteWorkreport(workId: str, empID=Depends(auth_handler.auth_wrapper)):
    try:
        cursor.execute("DELETE FROM Work_Record WHERE workId=%s", (workId))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ດຶງຂໍ້ມູນລາຍງານວຽກສຳເລັດ',
                }
        )
    except Exception as e:
        return e


@app.get('/api/v1/workreport/{Id}', tags=['ລາຍງານວຽກ'])
async def getWorkreportByEmpId(Id: str,empID=Depends(auth_handler.auth_wrapper)):
    try:
        cursor.execute(f"SELECT Id, empId, TaskId, DATE_FORMAT(dateBegin, '%%Y-%%m-%%d') as date_start, DATE_FORMAT(dateEnd, '%%Y-%%m-%%d') as date_end,\
                        code_row_per_day, doc_page_per_day, progress, workDescription FROM Work_Record WHERE empId=%s", (Id))
        workRows = cursor.fetchall()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ດຶງຂໍ້ມູນລາຍງານວຽກສຳເລັດ',
                "workreport": workRows}
        )

    except Exception as e:
        return e
