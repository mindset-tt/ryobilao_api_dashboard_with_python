from fastapi import Depends, Form
from fastapi.responses import JSONResponse
from auth.auth import AuthHandler
from config.connect import app, cursor, conp
from model.model import projectmaster


@app.get('/api/v1/project', tags=['ຂໍ້ມູນຂອງໂຄງການ'])
async def getProject(empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute(f"SELECT projectId, projectName, Acceptance_date, date_format(Start_date, '%Y-%m-%d'), date_format(End_date, '%Y-%m-%d'),\
                        Estimated_Man_Months, Actual_man_hours, Ordering_party, Remark, Description, progress FROM ProjectMaster")
        proRows = cursor.fetchall()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ດຶງຂໍ້ມູນໂຄງການສຳເລັດ',
                'project': proRows}
        )

    except Exception as e:
        return e


@app.post('/api/v1/project', tags=['ຂໍ້ມູນຂອງໂຄງການ'])
async def insertProject(projectmt: projectmaster, empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute("INSERT INTO ProjectMaster VALUES(projectId, projectName, Acceptance_date, Start_date, \
                       End_date, Estimated_Man_Months, Actual_man_hours, Ordering_party, Remark, Description, progress, createdBy, updateBy) Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)",
                       (projectmt.projectId, projectmt.projectName, projectmt.Acceptance_date, projectmt.Start_date, projectmt.End_date, projectmt.Estimated_Man_Months,
                        projectmt.Actual_man_hours, projectmt.Ordering_party, projectmt.Remark, projectmt.Description, projectmt.progress, projectmt.createdBy, projectmt.updateBy))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ເພີ່ມຂໍ້ມູນໂຄງການສຳເລັດ', }
        )

    except Exception as e:
        return e


@app.put('/api/v1/project', tags=['ຂໍ້ມູນຂອງໂຄງການ'])
async def updateProject(projectmt: projectmaster, empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute(f'UPDATE ProjectMaster SET projectName = "{projectmt.projectName}", Acceptance_date = "{projectmt.Acceptance_date}", Start_date = "{projectmt.Start_date}", \
                            End_date = "{projectmt.End_date}", Estimated_Man_Months = "{projectmt.Estimated_Man_Months}", Actual_man_hours = "{projectmt.Actual_man_hours}", \
                                Ordering_party = "{projectmt.Ordering_party}", Remark = "{projectmt.Remark}", Description = "{projectmt.Description}", progress = "{projectmt.progress}", \
                                    updateBy = "{projectmt.updateBy}", updateAt = NOW() WHERE projectId = "{projectmt.projectId}"')
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ແກ້ໄຂຂໍ້ມູນໂຄງການສຳເລັດ', }
        )
    except Exception as e:
        return e


@app.delete('/api/v1/project', tags=['ຂໍ້ມູນຂອງໂຄງການ'])
async def deleteProject(projectId: str, empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute(
            "DELETE FROM ProjectMaster WHERE projectId = %s", (projectId))
        conp.commit()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ລົບຂໍ້ມູນໂຄງການສຳເລັດ', }
        )

    except Exception as e:
        return e


@app.get('/api/v1/project/{projectId}', tags=['ຂໍ້ມູນຂອງໂຄງການ'])
async def getProjectById(projectId: str,empID=Depends(AuthHandler.auth_wrapper)):
    try:
        cursor.execute(f"SELECT projectId, projectName, Acceptance_date, date_format(Start_date, '%Y-%m-%d'), date_format(End_date, '%Y-%m-%d'),\
                        Estimated_Man_Months, Actual_man_hours, Ordering_party, Remark, Description, progress FROM ProjectMaster WHERE projectId = %s", (projectId))
        proRows = cursor.fetchone()
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": 'ດຶງຂໍ້ມູນໂຄງການສຳເລັດ',
                'project': proRows}
        )

    except Exception as e:
        return e
