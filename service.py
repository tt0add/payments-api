from database.crud import crud_add_money, crud_add_new_transaction, crud_get_money, crud_get_user_transactions, crud_remove_money, crud_transfer_money
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from exceptions import NegativeError, NotFoundError, BalanceError, SameUserError

def add_money_service(db: Session, user_id: int, sum: int):
    try:
        user = crud_add_money(db=db, user_id=user_id, sum=sum)
        db.commit()
        db.refresh(user)

        return user
    except SQLAlchemyError:
        db.rollback()
        raise
    except NegativeError:
        raise
    

def remove_money_service(db: Session, user_id: int, sum: int):
    try:
        user = crud_remove_money(db=db, user_id=user_id, sum=sum)

        db.commit()
        db.refresh(user)

        return user
    
    except SQLAlchemyError:
        db.rollback()
        raise
    
    except (NotFoundError, BalanceError, NegativeError) as e:
        raise
    
def get_money_service(db: Session, user_id: int):
    try:
        user = crud_get_money(db=db, user_id=user_id)

        return user
    
    except NotFoundError:
        raise

def add_transaction_service(db: Session, user_id: int, sum: int):
    try:
        transaction = crud_add_new_transaction(db=db, user_id=user_id, sum=sum)

        db.commit()
        db.refresh(transaction)
    except SQLAlchemyError:
        db.rollback()
        raise
    
def get_user_transactions_service(db: Session, user_id: int):
    transactions = crud_get_user_transactions(db=db, user_id=user_id)

    return transactions

def transfer_money_service(db: Session, user1_id: int, user2_id: int, sum: int):
    try:
        with db.begin():
            user2 = crud_transfer_money(db=db, user1_id=user1_id, user2_id=user2_id, sum=sum)

        db.refresh(user2)

        return user2

    except (NotFoundError, SameUserError, BalanceError) as e:
            raise

    