from sqlalchemy.orm import Session
import database.models as models
from exceptions import NotFoundError, BalanceError, NegativeError, SameUserError

def crud_add_money(db: Session, user_id: int, sum: int):

    if sum <= 0:
        raise NegativeError()

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        new_user = models.User(id=user_id, balance=sum)
        crud_add_new_transaction(db=db, 
                            user_id=user_id,
                            sum=sum)

        db.add(new_user)

        return new_user

    user.balance += sum
    crud_add_new_transaction(db=db, 
                            user_id=user_id,
                            sum=sum)
    

    return user

def crud_remove_money(db: Session, user_id: int, sum: int):
    if sum <= 0:
        raise NegativeError()

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise NotFoundError()

    if user.balance < sum:
        raise BalanceError()
    

    user.balance -= sum
    crud_add_new_transaction(db=db, 
                            user_id=user_id,
                            sum=-(sum))

    return user

def crud_get_money(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise NotFoundError()
    
    return user
    
def crud_transfer_money(db: Session, 
                        user1_id: int, 
                        user2_id: int, 
                        sum: int):
    
    if user1_id == user2_id:
        raise SameUserError()

    user1 = db.query(models.User).filter(models.User.id == user1_id).first()

    if not user1:
        raise NotFoundError()
    
    try:
        crud_remove_money(db=db, user_id=user1_id, sum=sum)

    except (NotFoundError, BalanceError) as e:
        raise
    
    user2 = crud_add_money(db=db, user_id=user2_id, sum=sum)

    return user2


def crud_add_new_transaction(db: Session, 
                             user_id: int, 
                             sum: int):
    new_transaction = models.Transaction(user_id=user_id, sum=sum)
    db.add(new_transaction)

    return new_transaction

def crud_get_user_transactions(db: Session, user_id: int):
    transactions = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()

    return transactions
