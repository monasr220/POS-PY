from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlalchemy import Boolean,String,Integer,Numeric,Text,func,DateTime
from sqlalchemy.orm import Mapped , mapped_column

from core.database import Base

class Goods(Base):
    __tablename__="goods"
    
    id:Mapped[UUID] = mapped_column(Integer,primary_key=True,index=True)
    name:Mapped[str]=mapped_column(String(255),nullable=False,index=True)
    sku:Mapped[str]=mapped_column(String(100),unique=True,index=True,nullable=True)
    barcode:Mapped[Optional[str]]=mapped_column(String(100),unique=True,index=True)
    category:Mapped[Optional[str]]=mapped_column(String(100),index=True,nullable=True)
    
    
    cost_price:Mapped[Decimal]=mapped_column(Numeric(10,2),nullable=False,default=Decimal("0.00"))
    selling_price:Mapped[Decimal]=mapped_column(Numeric(10,2),nullable=False,default=Decimal("0.00"))
    stock_quantity:Mapped[int]=mapped_column(Integer,default=0,nullable=False)
    min_stock_level:Mapped[int]=mapped_column(Integer,default=5,nullable=False)
    
    unit:Mapped[str]=mapped_column(String(55),default="unit",nullable=False)
    is_active:Mapped[bool]=mapped_column(Boolean,default=True,nullable=False)
    description:Mapped[Optional[str]]=mapped_column(Text,nullable=True)
    
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
 