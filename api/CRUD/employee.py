from re import match
from fastapi import Depends, Form, Request, UploadFile
from fastapi.responses import JSONResponse
from werkzeug.security import generate_password_hash
from auth.auth import AuthHandler
from config.connect import app, cursor, conp
import uuid
import os
ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg'}
ALLOWED_EXTENSIONS_ATTACH = {'doc', 'docx', 'pdf'}

def allowed_file_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE

def allowed_file_attach(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_ATTACH

@app.get('/api/v1/employee', tags=['ພະນັກງານ'])
async def getEmployee():
    try:
        cursor.execute(f"SELECT empId, empnickName, empGivenName, empFamilyName, gender, password, address, img, empTel,\
                        email, date_format(dateOfBirth, '%Y-%m-%d') as DateOfBirth, attacthMent, depId, positionId, empStatus, date_format(joinDate, '%Y-%m-%d') as joinDate,\
                        trainingPeriod, date_format(finishedTraining, '%Y-%m-%d') as finishedTraining, seatStatus, date_format(retireDate, '%Y-%m-%d') as retireDate, remark FROM Employee")
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


@app.post('/api/v1/employee', tags=['ພະນັກງານ'])
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
                         remark: str = Form(...),
                         empID=Depends(AuthHandler.auth_wrapper)
                         ):
    try:
        form_data = await request.form()
        # Accessing file information
        attachs_info = form_data["attachs"]
        photo_info = form_data["photo"]

        # Extract filenames
        attachs_filename = attachs_info.filename # type: ignore
        photo_filename = photo_info.filename # type: ignore

        cursor.execute(
                'SELECT emp_ID FROM employee WHERE emp_ID = %s', (empId))
        if empid := cursor.fetchone():
            respone = JSONResponse(status_code=405, content={
                                'message': 'ມີລະຫັດນີ້ແລ້ວ'})
        elif not match(r'[A-Z]+[0-9]+', empId):
            respone = JSONResponse(status_code=403, content={
                                'message': 'ຮູບແບບລະຫັດບໍ່ຖືກຕ້ອງ'})
        if attachs_info and (not allowed_file_attach(attachs_filename)):
            respone = JSONResponse(status_code=403, content={
                                'message': 'ເອກະສານບໍ່ຖືກຕ້ອງ'})
        elif photo_info and (not allowed_file_image(photo_filename)):
            respone = JSONResponse(status_code=403, content={
                                'message': 'ຮູບບໍ່ຖືກຕ້ອງ'})
        else:
            # Secure filenames
            secure_attachs_name = str(uuid.uuid4()) + (attachs_filename[-5:] if attachs_filename.endswith('.jpeg') else attachs_filename[-4:]) # type: ignore
            secure_photo_name = str(uuid.uuid4()) + (photo_filename[-5:] if photo_filename.endswith('.docx') else photo_filename[-4:]) # type: ignore

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
            respone = JSONResponse(
                status_code=201,
                content={
                    'message': 'ເພີ່ມຂໍ້ມູນສຳເລັດ', 'status': 'ok'}
            )
        return respone
    except Exception as e:
        return e


@app.put('/api/v1/employee', tags=['ພະນັກງານ'])
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
                         remark: str = Form(...),
                         empID=Depends(AuthHandler.auth_wrapper)
                         ):
    try:
        form_data = await request.form()
        # Accessing file information
        attachs_info = form_data["attachs"]
        photo_info = form_data["photo"]

        # Extract filenames
        attachs_filename = attachs_info.filename # type: ignore
        photo_filename = photo_info.filename # type: ignore

        cursor.execute(
                'SELECT emp_ID FROM employee WHERE emp_ID = %s', (empId))
        if empid := cursor.fetchone():
            respone = JSONResponse(status_code=405, content={
                                'message': 'ມີລະຫັດນີ້ແລ້ວ'})
        elif not match(r'[A-Z]+[0-9]+', empId):
            respone = JSONResponse(status_code=403, content={
                                'message': 'ຮູບແບບລະຫັດບໍ່ຖືກຕ້ອງ'})
        if attachs_info and (not allowed_file_image(attachs_filename)):
            respone = JSONResponse(status_code=403, content={
                                'message': 'ເອກະສານບໍ່ຖືກຕ້ອງ'})
        elif photo_info and (not allowed_file_image(photo_filename)):
            respone = JSONResponse(status_code=403, content={
                                'message': 'ຮູບບໍ່ຖືກຕ້ອງ'})
        else:
            # Secure filenames
            secure_attachs_name = str(uuid.uuid4()) + (attachs_filename[-5:] if attachs_filename.endswith('.jpeg') else attachs_filename[-4:]) # type: ignore
            secure_photo_name = str(uuid.uuid4()) + (photo_filename[-5:] if photo_filename.endswith('.docx') else photo_filename[-4:]) # type: ignore

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
            respone = {"status": "ok", "message": "Update Success", "code": 200}
        return respone
    except Exception as e:
        return e


@app.delete('/api/v1/employee', tags=['ພະນັກງານ'])
async def deleteEmployee(empId: str = Form(...), empID=Depends(AuthHandler.auth_wrapper)):
    try:
        sqlQuery = f'update Employee set empStatus = "Retire" where empId = "{empId}"'
        cursor.execute(sqlQuery)
        conp.commit()
        return {"status": "ok", "message": "Delete Success", "code": 200}
    except Exception as e:
        return e


@app.get('/api/v1/employee/{empId}', tags=['ພະນັກງານ'])
async def getEmployeeById(empId: str, empID=Depends(AuthHandler.auth_wrapper)):
    try:
        sqlQuery = f"SELECT empId, empnickName, empGivenName, empFamilyName, gender, password, address, img, empTel, email, date_format(dateOfBirth, '%Y-%m-%d') as DateOfBirth,\
              attacthMent, depId, positionId, empStatus, date_format(joinDate, '%Y-%m-%d') as joinDate, trainingPeriod, date_format(finishedTraining, '%Y-%m-%d') as finishedTraining,\
                  seatStatus, date_format(retireDate, '%Y-%m-%d') as retireDate, remark FROM Employee WHERE empId = '{empId}'"
        cursor.execute(sqlQuery)
        empRows = cursor.fetchone()
        return empRows
    except Exception as e:
        return e