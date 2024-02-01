from fastapi import Depends, Form
from fastapi.responses import JSONResponse
from auth.auth import AuthHandler
from config.connect import app, cursor, conp
from model.model import department


@app.get('/api/v1/department', tags=['ພາກສ່ວນ'])
async def getDepartment(empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute("SELECT depId, depName FROM Department")
        depRows = cursor.fetchall()
        print(depRows)
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ດຶງຂໍ້ມູນພະແນກສຳເລັດ',
                'department': depRows}
        )

    except Exception as e:
        return e


@app.post('/api/v1/department', tags=['ພາກສ່ວນ'])
async def insertDepartment(dep: department, empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute("INSERT INTO Department VALUES(depId, depName, createdBy, updateBy) VALUES (%s, %s, %s, %s)",
                       (dep.depId, dep.depName, dep.createdBy, dep.updateBy))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ເພີ່ມຂໍ້ມູນພະແນກສຳເລັດ'}
        )

    except Exception as e:
        return e


@app.put('/api/v1/department', tags=['ພາກສ່ວນ'])
async def updateDepartment(dep: department, empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute("UPDATE Department SET depName = %s, updateBy = %s, updateAt = NOW() WHERE depId = %s",
                       (dep.depName, dep.updateBy, dep.depId))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ແກ້ໄຂຂໍ້ມູນພະແນກສຳເລັດ',
                }
        )

    except Exception as e:
        return e


@app.delete('/api/v1/department', tags=['ພາກສ່ວນ'])
async def deleteDepartment(depId: str, empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute("DELETE FROM Department WHERE depId = %s", (depId))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ລົບຂໍ້ມູນພະແນກສຳເລັດ',
                }
        )

    except Exception as e:
        return e


@app.get('/api/v1/department/{depId}', tags=['ພາກສ່ວນ'])
async def getDepartmentById(depId: str, empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute(
            "SELECT depId, depName FROM Department WHERE depId = %s", (depId))
        depRows = cursor.fetchone()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ດຶງຂໍ້ມູນພະແນກສຳເລັດ',
                'user': depRows}
        )
    except Exception as e:
        return e
