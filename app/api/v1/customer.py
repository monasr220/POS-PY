from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db  # your async session dependency
from schemas.customer import (
    CustomerBalanceUpdate,
    CustomerCreate,
    CustomerPointsUpdate,
    CustomerResponse,
    CustomerUpdate,
)
from services.customerService import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])


def get_customer_service(db: AsyncSession = Depends(get_db)) -> CustomerService:
    return CustomerService(db)


# ---------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------
@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="إنشاء عميل جديد",
)
async def create_customer(
    payload: CustomerCreate,
    service: CustomerService = Depends(get_customer_service),
):
    return await service.create_customer(payload)


# ---------------------------------------------------------------
# LIST
# ---------------------------------------------------------------
@router.get(
    "/",
    response_model=List[CustomerResponse],
    summary="عرض قائمة العملاء (مع بحث وترقيم صفحات)",
)
async def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: Optional[str] = Query(None, description="بحث بالاسم أو الهاتف أو البريد"),
    is_active: Optional[bool] = Query(None),
    service: CustomerService = Depends(get_customer_service),
):
    return await service.list_customer(
        skip=skip, limit=limit, search=search, is_active=is_active
    )


# ---------------------------------------------------------------
# GET ONE
# ---------------------------------------------------------------
@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
    summary="عرض بيانات عميل واحد",
)
async def get_customer(
    customer_id: UUID,
    service: CustomerService = Depends(get_customer_service),
):
    return await service.get_customer(customer_id)


# ---------------------------------------------------------------
# UPDATE
# ---------------------------------------------------------------
@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse,
    summary="تحديث بيانات عميل",
)
async def update_customer(
    customer_id: UUID,
    payload: CustomerUpdate,
    service: CustomerService = Depends(get_customer_service),
):
    return await service.update_customer(customer_id, payload)


# ---------------------------------------------------------------
# DEACTIVATE (soft delete)
# ---------------------------------------------------------------
@router.post(
    "/{customer_id}/deactivate",
    response_model=CustomerResponse,
    summary="تعطيل حساب عميل (بدون حذف بياناته)",
)
async def deactivate_customer(
    customer_id: UUID,
    service: CustomerService = Depends(get_customer_service),
):
    return await service.deactivate_customer(customer_id)


# ---------------------------------------------------------------
# HARD DELETE
# ---------------------------------------------------------------
@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="حذف عميل نهائيًا (فقط إذا لا يوجد له فواتير/طلبات مرتبطة)",
)
async def delete_customer(
    customer_id: UUID,
    service: CustomerService = Depends(get_customer_service),
):
    await service.delete_customer(customer_id)


# ---------------------------------------------------------------
# BALANCE ADJUSTMENT
# ---------------------------------------------------------------
@router.post(
    "/{customer_id}/balance",
    response_model=CustomerResponse,
    summary="تعديل رصيد/آجل العميل (إضافة أو خصم)",
)
async def adjust_balance(
    customer_id: UUID,
    payload: CustomerBalanceUpdate,
    service: CustomerService = Depends(get_customer_service),
):
    return await service.adjust_balance(customer_id, payload.amount)


# ---------------------------------------------------------------
# LOYALTY POINTS ADJUSTMENT
# ---------------------------------------------------------------
@router.post(
    "/{customer_id}/points",
    response_model=CustomerResponse,
    summary="تعديل نقاط الولاء للعميل (إضافة أو خصم)",
)
async def adjust_points(
    customer_id: UUID,
    payload: CustomerPointsUpdate,
    service: CustomerService = Depends(get_customer_service),
):
    return await service.adjust_points(customer_id, payload.points)