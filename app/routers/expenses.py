from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from .. import crud
from ..auth import get_current_user


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"]
)


@router.post("/", response_model=ExpenseResponse)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.create_expense(
        db,
        expense,
        current_user.id
    )
@router.get("/", response_model=list[ExpenseResponse])
def get_expenses(
    category: str | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_expenses(
        db,
        current_user.id,
        category
    )
@router.get("/summary")
def expense_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_expense_summary(
        db,
        current_user.id
    )
@router.get("/summary/monthly")
def monthly_summary(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_monthly_summary(
        db,
        current_user.id,
        year,
        month
    )
@router.get("/summary/categories")
def category_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_category_summary(
        db,
        current_user.id
    )

@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    expense = crud.delete_expense(
        db,
        expense_id,
        current_user.id
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "message": "Expense deleted successfully"
    }

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    expense = crud.update_expense(
        db,
        expense_id,
        current_user.id,
        expense_data
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense 



