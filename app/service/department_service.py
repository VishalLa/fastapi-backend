from fastapi import (
    Depends,
    HTTPException,
    status 
)

from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from ..database.session import get_db

from ..database.model import Department 
from ..database.api_models.department_model import (
    DepartmentCreate,
    DepartmentResponse,
    DepatemtntUpdate
)


class DepartmentService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db 

    
    async def create_new_department(self, payload: DepartmentCreate):
        query = (
            select(Department)
            .where(Department.department_id == payload.department_id)
        )

        result = await self.db.execute(query)
        existing_department = result.scalars().first()

        if existing_department:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Department with department id: {payload.department_id} already exists !"
            )
        
        new_department = Department(**payload.model_dump())

        self.db.add(new_department)
        
        try:
            await self.db.commit()
            await self.db.refresh(new_department)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    
        return {"message": f"Department {payload.department_id} Create succfully"}
    

    async def get_all_department_(self):
        query = select(Department)

        result = await self.db.execute(query)
        departments = result.scalars().all()

        summary_list = []
        for dep in departments:
            summary_list.append({
                "department_id": dep.department_id,
                "department_name": dep.department_name,
                "location": dep.location,
                "description": dep.description,
                "head_of_department": dep.head_of_department
            })

        return summary_list


    async def get_department(self, department_id: str):
        query = (
            select(Department).
            where(Department.department_id == department_id)
        )

        result = await self.db.execute(query)
        department = result.scalars().first()

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Department with department id: {department_id} found !"
            )
        
        return department
       

    async def update_department_(self, department_id: str, payload: DepatemtntUpdate):
        query = (
            select(Department).
            where(Department.department_id == department_id)
        )

        result = await self.db.execute(query)
        department = result.scalars().first()

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Department with department id: {department_id} found !"
            )
        
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(department, key, value)

        return {"message": f"department with department id: {department_id} updated !"}
    

    async def delete_department_(self, department_id: str):
        query = (
            select(Department).
            where(Department.department_id == department_id)
        )

        result = await self.db.execute(query)
        department = result.scalars().first()

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Department with department id: {department_id} found !"
            )
        
        try: 
            await self.db.delete(department)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        
        return {"message": f"department with department id: {department_id} deleted !"}

