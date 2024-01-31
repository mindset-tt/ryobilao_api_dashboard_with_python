from fastapi import Form
from fastapi.responses import UJSONResponse
from config.connect import app, cursor, conp
from model.model import department


@app.get('/api/v1/department', tags=['ພາກສ່ວນ'], response_class=UJSONResponse)
async def getDepartment():
    try:
        cursor.execute("SELECT * FROM Department")
        depRows = cursor.fetchall()
        print(depRows)
        return depRows

    except Exception as e:
        return e


@app.post('/api/v1/department', tags=['ພາກສ່ວນ'], response_class=UJSONResponse)
async def insertDepartment(dep: department):
    try:
        cursor.execute("INSERT INTO Department VALUES(depId, depName, createdBy, updateBy) VALUES (%s, %s, %s, %s)",
                       (dep.depId, dep.depName, dep.createdBy, dep.updateBy))
        conp.commit()
        return {"message": "Insert Success"}

    except Exception as e:
        return e


@app.put('/api/v1/department', tags=['ພາກສ່ວນ'], response_class=UJSONResponse)
async def updateDepartment(dep: department):
    try:
        cursor.execute("UPDATE Department SET depName = %s, updateBy = %s, updateAt = NOW() WHERE depId = %s",
                       (dep.depName, dep.updateBy, dep.depId))
        conp.commit()
        return {"message": "Update Success"}

    except Exception as e:
        return e


@app.delete('/api/v1/department', tags=['ພາກສ່ວນ'], response_class=UJSONResponse)
async def deleteDepartment(depId: str):
    try:
        cursor.execute("DELETE FROM Department WHERE depId = %s", (depId))
        conp.commit()
        return {"message": "Delete Success"}

    except Exception as e:
        return print(e)


@app.get('/api/v1/department/{depId}', tags=['ພາກສ່ວນ'], response_class=UJSONResponse)
async def getDepartmentById(depId: str):
    try:
        cursor.execute("SELECT * FROM Department WHERE depId = %s", (depId))
        depRows = cursor.fetchone()
        return depRows
    except Exception as e:
        return e
