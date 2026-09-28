from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Base Schema
class CustomerBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255, examples=["أحمد محمود"])
    email: Optional[EmailStr] = Field(None, examples=["ahmed@example.com"])
    phone: str = Field(..., min_length=8, max_length=50, examples=["01012345678"])
    address: Optional[str] = Field(None, examples=["القاهرة، مصر"])
    credit_limit: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="الحد الأقصى للائتمان/الآجل",
    )
    notes: Optional[str] = Field(None)


# Schema for Creating
class CustomerCreate(CustomerBase):
    pass


# Schema for Updating (all fields optional)
class CustomerUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None, min_length=8, max_length=50)
    address: Optional[str] = Field(None)
    credit_limit: Optional[Decimal] = Field(None, ge=0, max_digits=10, decimal_places=2)
    is_active: Optional[bool] = Field(None)
    notes: Optional[str] = Field(None)


# Schemas for adjusting balance / loyalty points
class CustomerBalanceUpdate(BaseModel):
    amount: Decimal = Field(
        ...,
        max_digits=10,
        decimal_places=2,
        description="القيمة المراد إضافتها أو خصمها",
    )


class CustomerPointsUpdate(BaseModel):
    points: int = Field(..., description="عدد النقاط المراد إضافتها أو خصمها")


# Schema for Response
class CustomerResponse(CustomerBase):
    id: UUID
    loyalty_points: int
    balance: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)