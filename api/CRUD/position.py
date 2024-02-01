from fastapi import Depends, Form
from fastapi.responses import JSONResponse
from auth.auth import AuthHandler
from config.connect import app, cursor, conp
from model.model import position


@app.get('/api/v1/position', tags=['ຕຳແໜ່ງ'])
async def getPosition(empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute("SELECT positionId, positionName FROM Position")
        posRows = cursor.fetchall()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ດຶງຂໍ້ມູນຕຳແໜ່ງສຳເລັດ',
                'position': posRows}
        )

    except Exception as e:
        return e


@app.post('/api/v1/position', tags=['ຕຳແໜ່ງ'])
async def insertPosition(pos: position,empID=Depends(AuthHandler.auth_wrapper)):
    try:

        cursor.execute("INSERT INTO Position (positionId, positionName, createdBy, updatedBy) VALUES (%s, %s, %s, %s)",
                       (pos.positionId, pos.positionName, pos.createdBy, pos.updateBy))
        conp.commit()

        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ເພີ່ມຂໍ້ມູນຕຳແໜ່ງສຳເລັດ',
                }
        )

    except Exception as e:
        return {"message": e}


@app.put('/api/v1/position', tags=['ຕຳແໜ່ງ'])
async def updatePosition(pos: position, empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute("UPDATE Position SET positionName = %s, updateBy = %s, updateAt = NOW() WHERE positionId = %s",
                       (pos.positionName, pos.updateBy, pos.positionId))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ແກ້ໄຂຂໍ້ມູນສຳເລັດ',
                }
        )

    except Exception as e:
        return e


@app.delete('/api/v1/position', tags=['ຕຳແໜ່ງ'])
async def deletePosition(positionId: str, empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute(
            "DELETE FROM Position WHERE positionId = %s", (positionId))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ລົບຂໍ້ມູນຕຳແໜ່ງສຳເລັດ'}
        )

    except Exception as e:
        return print(e)


@app.get('/api/v1/position/{positionId}', tags=['ຕຳແໜ່ງ'])
async def getPositionById(positionId: str, empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute(
            "SELECT positionId, positionName FROM Position WHERE positionId = %s", (positionId))
        posRows = cursor.fetchone()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ດຶງຂໍ້ມູນຕຳແໜ່ງສຳເລັດ',
                'position': posRows}
        )

    except Exception as e:
        return e
