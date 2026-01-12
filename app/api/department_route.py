from fastapi import (
    APIRouter,
    Depends,
    status
)

from ..database.api_models.department_model import (
    DepartmentCreate,
    DepartmentResponse,
    DepatemtntUpdate
)
from ..service import DepartmentService

admin_department_api_route = APIRouter(prefix="/admin/department", tags=["Department"])


@admin_department_api_route.post(
    "/add/department",
    status_code=status.HTTP_201_CREATED
)
async def create_department(
    payload: DepartmentCreate, 
    service: DepartmentService = Depends(DepartmentService)
):
    return await service.create_new_department(payload=payload)


@admin_department_api_route.get(
    "/get/all",
    status_code=status.HTTP_200_OK,
    response_model=list[DepartmentResponse]
)
async def get_all_department(
    service: DepartmentService = Depends(DepartmentService)
):
    return await service.get_all_department_()


@admin_department_api_route.get(
    "/get/doctor/{department_id}",
    status_code=status.HTTP_200_OK,
    response_model=DepartmentResponse
)
async def get_department(
    department_id, 
    service: DepartmentService = Depends(DepartmentService)
):
    return await service.get_department(department_id=department_id)


@admin_department_api_route.put(
    "/update/{department_id}",
    status_code=status.HTTP_200_OK
)
async def update_department(
    department_id: str, 
    payload: DepatemtntUpdate,
    service: DepartmentService = Depends(DepartmentService)
):
    return await service.update_department_(department_id=department_id, payload=payload)


@admin_department_api_route.delete(
    "/delete/{department_id}",
    status_code=status.HTTP_200_OK
)
async def delete_department(
    department_id: str, 
    service: DepartmentService = Depends(DepartmentService)
):
    return await service.delete_department_(department_id=department_id)

