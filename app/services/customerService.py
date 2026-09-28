from decimal import Decimal
from typing import Optional,Sequence
from uuid import UUID

from fastapi import HTTPException , status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.customer import Customer
from schemas.customer import CustomerCreate, CustomerUpdate

class CustomerService:
    def __init__(self ,db:AsyncSession):
        self.db =db
        
    async def create_customer(self,data:CustomerCreate)->Customer:
        customer=Customer(**data.model_dump())
        self.db.add(customer)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email or phone is found already"
            )
        await self.db.refresh(customer)
        return customer
    

    async def get_customer(self,customer_id:UUID)->Customer:
        customer = await self.db.get(Customer,customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
                
            )
            
        return customer
      
    async def list_customer(
        self,
        skip:int = 0,
        limit :int = 50,
        search:Optional[str]=None,
        is_active:Optional[bool]=None,
        )->Sequence[Customer]:
        stmt = select(Customer)
        
        if search:
            pattern=f"%{search}"
            stmt = stmt.where(
            (Customer.full_name.ilike(pattern))
            | (Customer.phone.ilike(pattern))
            |(Customer.email.ilike(pattern))
            )
        if is_active is not None:
            stmt=stmt.where(Customer.is_active==is_active)
            
        stmt=stmt.offset(skip).limit(limit).order_by(Customer.created_at.desc())
        result= await self.db.execute(stmt)
        return result.scalars().all()
    
    async def update_customer(self,customer_id,data:CustomerUpdate)->Customer:
        customer = await self.get_customer(customer_id)
        
        update_data = data.model_dump(exclude_unset=True)
        
        for field,value in update_data.items():
            setattr(customer,field , value)
        
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="email or phone number is in use"
            )
        await self.db.refresh(customer)
        return customer
    

    async def deactivate_customer(self,customer_id:UUID)->Customer:
        customer=await self.get_customer(customer_id)
        customer.is_active =False
        await self.db.commit()
        await self.db.refresh(customer)
        return customer
    
    async def delete_customer(self,customer_Id:UUID)->None:
        """Hard Delete if customer has no linked orders or invoices"""
        
        customer = await self.get_customer(customer_Id)
        await self.db.delete(customer)
        await self.db.commit()
    
    async def adjust_balance(self,customer_id:UUID ,amount:Decimal)->Customer:
        customer= await self.get_customer(customer_id)
        new_balance = customer.balance + amount
        
        if new_balance > customer.credit_limit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"credit score if overflow {customer.credit_limit}"
                    ,f"the new balance:{new_balance}"
                )
            )
        customer.balance= new_balance
        await self.db.commit()
        await self.db.refresh(customer)
        return customer
    
    async def adjust_points(self, customer_id: UUID, points: int) -> Customer:
        customer = await self.get_customer(customer_id)
        new_points = customer.loyalty_points + points
 
        if new_points < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="لا يمكن أن يكون رصيد النقاط أقل من صفر",
            )
 
        customer.loyalty_points = new_points
        await self.db.commit()
        await self.db.refresh(customer)
        return customer