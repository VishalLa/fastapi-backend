from fastapi import (
    APIRouter,
    Depends,
    status
)

from ..service.admin_service import AdminService 
from ..database.api_models.admin_model import DashboardSearchResponse


admin_dashboard_api = APIRouter(prefix="/admin/dashboard", tags=["Admin"])

@admin_dashboard_api.get(
    "/get/{query_string}",
    status_code=status.HTTP_200_OK,
    response_model=DashboardSearchResponse
)
async def query(
    query_string: str,
    service: AdminService = Depends(AdminService)
):
    return await service.query_(query_string=query_string)

