from fastapi import Form
from fastapi.responses import UJSONResponse
from config.connect import app, cursor, conp
from model.model import workreport


@app.get('/api/v1/workreport', tags=['ໜ້າວຽກ'], response_class=UJSONResponse)
async def getWorkreport():
    try:
        cursor.execute("SELECT * FROM Work_Record")
        workRows = cursor.fetchall()
        print(workRows)
        return workRows

    except Exception as e:
        return e


@app.post('/api/v1/workreport', tags=['ໜ້າວຽກ'], response_class=UJSONResponse)
async def insertWorkreport(workrp: workreport):
    try:
        cursor.execute("INSERT INTO Work_Record VALUES(Id, TaskManageement_Id, empId, dateBegin, dateEnd, code_row_per_day, doc_page_per_day, progress, \
                       workDescription, createdBy, updatedBy) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
                       (workrp.workId, workrp.TaskManageement_Id, workrp.empId, workrp.dateBegin, workrp.dateEnd, 
                        workrp.code_row_per_day, workrp.doc_page_per_day, workrp.progress, workrp.workDescription, workrp.createdBy, workrp.updateBy))
        conp.commit()
        return {"message": "Insert Success"}

    except Exception as e:
        return e

@app.put('/api/v1/workreport', tags=['ໜ້າວຽກ'], response_class=UJSONResponse)
async def updateWorkreport(workrp: workreport
                           ):
    try:
        cursor.execute("UPDATE Work_Record SET TaskManageement_Id=%s, empId=%s, dateBegin=%s, dateEnd=%s, code_row_per_day=%s, doc_page_per_day=%s, progress=%s, \
                       workDescription=%s, updatedBy=%s WHERE workId=%s",
                       (workrp.TaskManageement_Id, workrp.empId, workrp.dateBegin, workrp.dateEnd, workrp.code_row_per_day,
                        workrp.doc_page_per_day, workrp.progress, workrp.workDescription, workrp.updateBy, workrp.workId))
        conp.commit()
        return {"message": "Update Success"}

    except Exception as e:
        return e
    
@app.delete('/api/v1/workreport', tags=['ໜ້າວຽກ'], response_class=UJSONResponse)
async def deleteWorkreport(workId: str):
    try:
        cursor.execute("DELETE FROM Work_Record WHERE workId=%s", (workId))
        conp.commit()
        return {"message": "Delete Success"}

    except Exception as e:
        return e

@app.get('/api/v1/workreport/{Id}', tags=['ໜ້າວຽກ'], response_class=UJSONResponse)
async def getWorkreportByEmpId(Id: str):
    try:
        cursor.execute("SELECT * FROM Work_Record WHERE empId=%s", (Id))
        workRows = cursor.fetchall()
        print(workRows)
        return workRows

    except Exception as e:
        return e