from fastapi import Form
from fastapi.responses import UJSONResponse
from config.connect import app, cursor, conp
from model.model import position


@app.get('/api/v1/position', tags=['ຕຳແໜ່ງ'], response_class=UJSONResponse)
async def getPosition():
    try:
        cursor.execute("SELECT * FROM Position")
        posRows = cursor.fetchall()
        print(posRows)
        return posRows

    except Exception as e:
        return e


@app.post('/api/v1/position', tags=['ຕຳແໜ່ງ'], response_class=UJSONResponse)
async def insertPosition(pos: position):
    # try:

    cursor.execute("INSERT INTO Position (positionId, positionName, createdBy, updatedBy) VALUES (%s, %s, %s, %s)",
                    (pos.positionId, pos.positionName, pos.createdBy, pos.updateBy))
    conp.commit()

    return {"message": "Insert Success"}

    # except Exception as e:
    #     return {"message": e}


@app.put('/api/v1/position', tags=['ຕຳແໜ່ງ'], response_class=UJSONResponse)
async def updatePosition(pos: position):
    try:
        cursor.execute("UPDATE Position SET positionName = %s, updateBy = %s, updateAt = NOW() WHERE positionId = %s",
                       (pos.positionName, pos.updateBy, pos.positionId))
        conp.commit()
        return {"message": "Update Success"}

    except Exception as e:
        return e


@app.delete('/api/v1/position', tags=['ຕຳແໜ່ງ'], response_class=UJSONResponse)
async def deletePosition(positionId: str):
    try:
        cursor.execute(
            "DELETE FROM Position WHERE positionId = %s", (positionId))
        conp.commit()
        return {"message": "Delete Success"}

    except Exception as e:
        return print(e)


@app.get('/api/v1/position/{positionId}', tags=['ຕຳແໜ່ງ'], response_class=UJSONResponse)
async def getPositionById(positionId: str):
    try:
        cursor.execute(
            "SELECT * FROM Position WHERE positionId = %s", (positionId))
        posRows = cursor.fetchone()
        return posRows

    except Exception as e:
        return e
