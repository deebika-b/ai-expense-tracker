from sqlalchemy.orm import Session

from . import models
from .schemas import UserCreate, ExpenseCreate, ExpenseUpdate
from .auth import hash_password


# ---------- USER CRUD ----------

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)

    db_user = models.User(
        email=user.email,
        password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_email(db: Session, email: str):
    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )


def get_user_by_id(db: Session, user_id: int):
    return (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )


# ---------- EXPENSE CRUD ----------

def create_expense(
    db: Session,
    expense: ExpenseCreate,
    user_id: int
):
    db_expense = models.Expense(
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        user_id=user_id
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense

def get_expenses(
    db: Session,
    user_id: int,
    category: str | None = None
):
    query = (
        db.query(models.Expense)
        .filter(models.Expense.user_id == user_id)
    )

    if category:
        query = query.filter(
            models.Expense.category == category
        )

    return query.all()

def delete_expense(
    db: Session,
    expense_id: int,
    user_id: int
):
    expense = (
        db.query(models.Expense)
        .filter(
            models.Expense.id == expense_id,
            models.Expense.user_id == user_id
        )
        .first()
    )

    if not expense:
        return None

    db.delete(expense)
    db.commit()

    return expense

def update_expense(
    db: Session,
    expense_id: int,
    user_id: int,
    expense_data: ExpenseUpdate
):
    expense = (
        db.query(models.Expense)
        .filter(
            models.Expense.id == expense_id,
            models.Expense.user_id == user_id
        )
        .first()
    )

    if not expense:
        return None

    expense.amount = expense_data.amount
    expense.category = expense_data.category
    expense.description = expense_data.description

    db.commit()
    db.refresh(expense)

    return expense

def get_expense_summary(
    db: Session,
    user_id: int
):
    expenses = (
        db.query(models.Expense)
        .filter(models.Expense.user_id == user_id)
        .all()
    )

    total_spending = sum(
        expense.amount for expense in expenses
    )

    expense_count = len(expenses)

    return {
        "total_spending": total_spending,
        "expense_count": expense_count
    }

def get_monthly_summary(
    db: Session,
    user_id: int,
    year: int,
    month: int
):
    expenses = (
        db.query(models.Expense)
        .filter(
            models.Expense.user_id == user_id
        )
        .all()
    )

    monthly_expenses = [
        expense
        for expense in expenses
        if expense.created_at.year == year
        and expense.created_at.month == month
    ]

    total_spending = sum(
        expense.amount
        for expense in monthly_expenses
    )

    expense_count = len(monthly_expenses)

    return {
        "year": year,
        "month": month,
        "total_spending": total_spending,
        "expense_count": expense_count
    }

def get_category_summary(
    db: Session,
    user_id: int
):
    expenses = (
        db.query(models.Expense)
        .filter(models.Expense.user_id == user_id)
        .all()
    )

    category_totals = {}

    for expense in expenses:
        category = expense.category

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += expense.amount

    return category_totals