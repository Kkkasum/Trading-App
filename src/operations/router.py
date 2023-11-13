from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate


router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get('/')
async def get_operation(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail={
            "status": e.status_code,
            "data": None,
            "details": e.detail
        })
    else:
        return {
            "status": "success",
            "data": result.all(),
            "details": None
        }


@router.post('/')
async def add_operation(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(operation).values(**new_operation.model_dump())
        await session.execute(stmt)
        await session.commit()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail={
            "status": e.status_code,
            "data": None,
            "details": e.detail
        })
    else:
        return {
            "status": "success",
            "data": None,
            "details": "Operation inserted successfully"
        }
