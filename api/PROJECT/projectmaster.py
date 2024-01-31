from fastapi import Form
from fastapi.responses import UJSONResponse
from config.connect import app, cursor, conp
from model.model import projectmaster

@app.get('/api/v1/project', tags=['ຂໍ້ມູນຂອງໂຄງການ'], response_class=UJSONResponse)
async def getProject():
    try:
        cursor.execute("SELECT * FROM ProjectMaster")
        proRows = cursor.fetchall()
        print(proRows)
        return proRows

    except Exception as e:
        return e

@app.post('/api/v1/project', tags=['ຂໍ້ມູນຂອງໂຄງການ'], response_class=UJSONResponse)
async def insertProject(projectmt: projectmaster
                        ):
    try:
        cursor.execute("INSERT INTO ProjectMaster VALUES(projectId, projectName, Acceptance_date, Start_date, \
                       End_date, Estimated_Man_Months, Actual_man_hours, Ordering_party, Remark, Description, progress, createdBy, updateBy) Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)",
                       (projectmt.projectId, projectmt.projectName, projectmt.Acceptance_date, projectmt.Start_date, projectmt.End_date, projectmt.Estimated_Man_Months, 
                        projectmt.Actual_man_hours, projectmt.Ordering_party, projectmt.Remark, projectmt.Description, projectmt.progress, projectmt.createdBy, projectmt.updateBy))
        conp.commit()
        return {"message": "Insert Success"}

    except Exception as e:
        return e

@app.put('/api/v1/project', tags=['ຂໍ້ມູນຂອງໂຄງການ'], response_class=UJSONResponse)
async def updateProject(projectmt: projectmaster
                        ):
    try:
        cursor.execute(f'UPDATE ProjectMaster SET projectName = "{projectmt.projectName}", Acceptance_date = "{projectmt.Acceptance_date}", Start_date = "{projectmt.Start_date}", \
                            End_date = "{projectmt.End_date}", Estimated_Man_Months = "{projectmt.Estimated_Man_Months}", Actual_man_hours = "{projectmt.Actual_man_hours}", \
                                Ordering_party = "{projectmt.Ordering_party}", Remark = "{projectmt.Remark}", Description = "{projectmt.Description}", progress = "{projectmt.progress}", \
                                    updateBy = "{projectmt.updateBy}", updateAt = NOW() WHERE projectId = "{projectmt.projectId}"')
        conp.commit()
        return {"message": "Update Success"}
    except Exception as e:
        return e

@app.delete('/api/v1/project', tags=['ຂໍ້ມູນຂອງໂຄງການ'], response_class=UJSONResponse)
async def deleteProject(projectId: str ):
    try:
        cursor.execute("DELETE FROM ProjectMaster WHERE projectId = %s", (projectId))
        conp.commit()
        return {"message": "Delete Success"}

    except Exception as e:
        return e
        
@app.get('/api/v1/project/{projectId}', tags=['ຂໍ້ມູນຂອງໂຄງການ'], response_class=UJSONResponse)
async def getProjectById(projectId: str):
    try:
        cursor.execute("SELECT * FROM ProjectMaster WHERE projectId = %s", (projectId))
        proRows = cursor.fetchone()
        return proRows

    except Exception as e:
        return e