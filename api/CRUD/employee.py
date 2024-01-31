from fastapi import Depends, Form, Request, UploadFile
from fastapi.responses import UJSONResponse
from werkzeug.security import generate_password_hash
from config.connect import app, cursor, conp
import uuid
import os


@app.get('/api/v1/employee', tags=['ພະນັກງານ'], response_class=UJSONResponse)
async def getEmployee():
    try:
        cursor.execute("SELECT * FROM Employee")
        empRows = cursor.fetchall()
        return empRows

    except Exception as e:
        return e


async def copy_file(src: UploadFile, dst_directory: str):
    # Read the contents of the UploadFile
    contents = await src.read()

    # Write the contents to the specified path
    with open(os.path.join((dst_directory)), 'wb') as dst_file:
        dst_file.write(contents)


@app.post('/api/v1/employee', tags=['ພະນັກງານ'], response_class=UJSONResponse)
async def insertEmployee(request: Request,
                         empId: str = Form(...),
                         empnickName: str = Form(...),
                         empGivenName: str = Form(...),
                         empFamilyName: str = Form(...),
                         gender: str = Form(...),
                         password: str = Form(...),
                         address: str = Form(...),
                         empTel: str = Form(...),
                         email: str = Form(...),
                         dateOfBirth: str = Form(...),
                         empStatus: str = Form(...),
                         depId: str | None = Form(None),
                         positionId:  str | None = Form(None),
                         joinDate: str = Form(...),
                         trainingPeriod: str = Form(...),
                         finishedTraining: str = Form(...),
                         seatStatus: str = Form(...),
                         createdBy: str = Form(...),
                         updateBy: str = Form(...),
                         retireDate: str = Form(...),
                         remark: str = Form(...)
                         ):
    try:
        form_data = await request.form()
        # Accessing file information
        attachs_info = form_data["attachs"]
        photo_info = form_data["photo"]
        # Extract filenames
        attachs_filename = attachs_info.filename # type: ignore
        photo_filename = photo_info.filename # type: ignore

        # Secure filenames
        secure_attachs_name = str(uuid.uuid4()) + attachs_filename # type: ignore
        secure_photo_name = str(uuid.uuid4()) + photo_filename # type: ignore

        # Copy files to destination
        await copy_file(attachs_info, f"static\\attachments\\{secure_attachs_name}") # type: ignore
        await copy_file(photo_info, f"static\\images\\{secure_photo_name}") # type: ignore
 
        passhash = generate_password_hash(password)
        sqlQuery = 'INSERT INTO Employee (empId, empnickName, empGivenName, empFamilyName, gender, password, \
                        address, img, empTel, email, dateOfBirth, attacthMent, depId, positionId, empStatus, joinDate, trainingPeriod, \
                        finishedTraining, seatStatus, createdBy, updatedBy, retireDate, remark) VALUES (%s, %s, %s, %s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        binddata = empId, empnickName, empGivenName, empFamilyName, gender, passhash, address, secure_photo_name, empTel, email, dateOfBirth, \
            secure_attachs_name, depId, positionId, empStatus, joinDate, trainingPeriod, finishedTraining, seatStatus, createdBy, updateBy, retireDate, remark
        cursor.execute(sqlQuery, binddata)
        conp.commit()
        return {"status": "ok", "message": "Insert Success", "code": 200}
    except Exception as e:
        return e


@app.put('/api/v1/employee', tags=['ພະນັກງານ'], response_class=UJSONResponse)
async def updateEmployee(request: Request,
                         empId: str = Form(...),
                         empnickName: str = Form(...),
                         empGivenName: str = Form(...),
                         empFamilyName: str = Form(...),
                         gender: str = Form(...),
                         password: str = Form(...),
                         address: str = Form(...),
                         empTel: str = Form(...),
                         email: str = Form(...),
                         dateOfBirth: str = Form(...),
                         empStatus: str = Form(...),
                         depId: str | None = Form(None),
                         positionId:  str | None = Form(None),
                         joinDate: str = Form(...),
                         trainingPeriod: str = Form(...),
                         finishedTraining: str = Form(...),
                         seatStatus: str = Form(...),
                         updateBy: str = Form(...),
                         retireDate: str = Form(...),
                         remark: str = Form(...)
                         ):
    try:
        form_data = await request.form()
        # Accessing file information
        attachs_info = form_data["attachs"]
        photo_info = form_data["photo"]
        # Extract filenames
        attachs_filename = attachs_info.filename if attachs_info.filename else "" # type: ignore
        photo_filename = photo_info.filename if photo_info.filename else "" # type: ignore

        # Secure filenames
        secure_attachs_name = str(uuid.uuid4()) + attachs_filename
        secure_photo_name = str(uuid.uuid4()) + photo_filename

        # Copy files to destination
        await copy_file(attachs_info, f"static\\attachments\\{secure_attachs_name}") # type: ignore
        await copy_file(photo_info, f"static\\images\\{secure_photo_name}") # type: ignore
        passhash = generate_password_hash(password)
        sqlQuery = f'UPDATE Employee SET empnickName = "{empnickName}", empGivenName = "{empGivenName}", empFamilyName = "{empFamilyName}", \
            gender = {gender}, password = "{passhash}", address = "{address}", img = "{secure_photo_name}", empTel = "{empTel}", email = "{email}", \
                dateOfBirth = "{dateOfBirth}", attacthMent = "{secure_attachs_name}", depId = "{depId}", positionId = "{positionId}", empStatus = "{empStatus}", \
                    joinDate = "{joinDate}", trainingPeriod = "{trainingPeriod}", finishedTraining = "{finishedTraining}", seatStatus = "{seatStatus}", \
                        updatedBy = "{updateBy}", retireDate = "{retireDate}", remark = "{remark}", updateAt = NOW() WHERE empId = "{empId}"'
        cursor.execute(sqlQuery)
        conp.commit()
        return {"status": "ok", "message": "Update Success", "code": 200}
    except Exception as e:
        return e


@app.delete('/api/v1/employee', tags=['ພະນັກງານ'], response_class=UJSONResponse)
async def deleteEmployee(empId: str = Form(...)):
    try:
        sqlQuery = f'update Employee set empStatus = "Retire" where empId = "{empId}"'
        cursor.execute(sqlQuery)
        conp.commit()
        return {"status": "ok", "message": "Delete Success", "code": 200}
    except Exception as e:
        return e


@app.get('/api/v1/employee/{empId}', tags=['ພະນັກງານ'], response_class=UJSONResponse)
async def getEmployeeById(empId: str):
    try:
        sqlQuery = f'SELECT * FROM Employee WHERE empId = "{empId}"'
        cursor.execute(sqlQuery)
        empRows = cursor.fetchone()
        return empRows
    except Exception as e:
        return e