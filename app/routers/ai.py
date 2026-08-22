from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Expense
from ..auth import get_current_user

from ..services.langchain_service import analyze_with_langchain
from ..services.receipt_service import analyze_receipt


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


# ---------------------------------------------------------
# AI SPENDING ANALYSIS
# ---------------------------------------------------------

@router.post("/analyze")
def analyze_user_expenses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == current_user.id
        )
        .all()
    )

    # Handle empty database
    if not expenses:
        return {
            "analysis": {
                "total_spending": 0,
                "top_category": "No expenses",
                "insight": "You don't have any expenses yet.",
                "recommendation": "Upload a receipt to start tracking your spending."
            }
        }

    # Convert expenses into text for LangChain
    expense_text = "\n".join(
        [
            f"{expense.category}: €{expense.amount} - {expense.description}"
            for expense in expenses
        ]
    )

    # Send expenses to LangChain
    result = analyze_with_langchain(expense_text)

    return {
        "analysis": result
    }


# ---------------------------------------------------------
# RECEIPT ANALYSIS
# ---------------------------------------------------------

@router.post("/receipt")
def analyze_receipt_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    image_bytes = file.file.read()

    result = analyze_receipt(
        image_bytes,
        file.content_type
    )

    # Save extracted receipt information
    expense = Expense(
        amount=float(result["amount"]),
        category=result["category"],
        description=result.get(
            "description",
            "Receipt purchase"
        ),
        user_id=current_user.id
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return {
        "message": "Receipt analyzed and expense saved successfully",
        "expense": {
            "id": expense.id,
            "amount": expense.amount,
            "category": expense.category,
            "description": expense.description
        }
    }