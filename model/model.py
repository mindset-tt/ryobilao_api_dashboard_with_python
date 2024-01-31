from dataclasses import dataclass
from pydantic import BaseModel
from fastapi import Form, Request, UploadFile, File

class taskmanagement(BaseModel):
    taskId: str
    projectId: str
    sectionName: str
    taskName: str
    progress: str
    fromDate: str
    toDate: str
    createdBy: str
    updateBy: str

class workreport(BaseModel):
    workId: str
    TaskManageement_Id: str
    empId: str
    dateBegin: str
    dateEnd: str
    code_row_per_day: str
    doc_page_per_day: str
    progress: str
    workDescription: str
    createdBy: str
    updateBy: str

class department(BaseModel):
    depId: str 
    depName: str 
    createdBy: str 
    updateBy: str 

class position(BaseModel):
    positionId: str
    positionName: str
    createdBy: str
    updateBy: str

class projectmaster(BaseModel):
    projectId: str 
    projectName: str 
    Acceptance_date : str
    Start_date : str
    End_date : str
    Estimated_Man_Months : str
    Actual_man_hours : str
    Ordering_party : str
    Remark : str
    Description: str
    progress: str
    createdBy: str 
    updateBy: str 