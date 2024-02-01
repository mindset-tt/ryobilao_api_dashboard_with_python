from fastapi import Depends, Form, Request, UploadFile
from fastapi.responses import UJSONResponse, JSONResponse
from werkzeug.security import check_password_hash
from config.connect import SECRET_KEY, app, cursor, conp
from model.model import LoginStart
import uuid
import os
import jwt
from datetime import datetime, timedelta, timezone
from re import match


@app.post('/myproject1/login', tags=['ເຂົ້າສູ່ລະບົບ'])
async def Login(info: LoginStart):
    # try:
        cursor.execute(
            "SELECT d1.empID, d1.password, d1.empStatus FROM Employee as d1 where d1.empId=%s and d1.empStatus = 1", (info.empId))
        if row := cursor.fetchone():
            password = row['password']
            if not match(r'[A-Z0-9]+', info.empId):
                return JSONResponse(
                    status_code=401,
                    content={'message': 'username ບໍ່ຖືກຕ້ອງ'}
                )
            if check_password_hash(password, info.password) == True:
                token = jwt.encode({'public_id': info.empId, 'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=12), 'iat': datetime.now(timezone.utc)}, SECRET_KEY, algorithm='HS256') # type: ignore
                cursor.execute(
                    f"SELECT empId, empnickName, empGivenName, empFamilyName, gender, password, address, img, empTel,\
                        email, date_format(dateOfBirth, '%%Y-%%m-%%d') as DateOfBirth, attacthMent, depId, positionId, empStatus, date_format(joinDate, '%%Y-%%m-%%d') as joinDate,\
                        trainingPeriod, date_format(finishedTraining, '%%Y-%%m-%%d') as finishedTraining, seatStatus, date_format(retireDate, '%%Y-%%m-%%d') as retireDate, remark FROM Employee where empId=%s and empStatus=1", (info.empId))
                userRows = cursor.fetchone()
                return JSONResponse(
                    status_code=200,
                    content={
                        "status": "ok",
                        "message": 'ເຂົ້າສູ່ລະບົບສຳເລັດ',
                        'token': token,
                        'user': userRows}
                )
            else:
                respone = JSONResponse(
                    status_code=401,
                    content={'message': 'password ບໍ່ຖືກຕ້ອງ'}
                )
                return respone
        else:
            respone = JSONResponse(
                status_code=401,
                content={'message': 'ບໍ່ມີຜູ້ໃຊ້ນີ້'}
            )
            return respone

    # except Exception as e:
    #     return e
