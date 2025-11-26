from fastapi import APIRouter, Depends, status, HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
from exceptions import BalanceError, NotFoundError, NegativeError, SameUserError
from exchange_rates import get_usd_rate, get_eur_rate
from service import add_money_service, remove_money_service, transfer_money_service, get_money_service, get_user_transactions_service
from schemas import MoneyOperation, TransferOperation

router = APIRouter()


@router.get('/users/{user_id}/balance')
def get_user_balance(user_id: int, currency: str = 'RUB', db: Session = Depends(get_db)):
    try:
        user = get_money_service(db=db, user_id=user_id)

    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with ID: {user_id} not found')
    if currency == 'EUR':
        eur_rate = get_eur_rate()
        return user.balance / eur_rate
    elif currency == 'USD':
        usd_rate = get_usd_rate()
        return user.balance / usd_rate
    elif currency == 'RUB':
        return user.balance
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Wrong currency, supported only: USD, EUR')


@router.get('/users/{user_id}/transactions')
def get_transactions(user_id: int, db: Session = Depends(get_db)):
    transactions = get_user_transactions_service(db=db, user_id=user_id)

    return transactions[::-1]


@router.post('/payments/add')
def add_money(data: MoneyOperation, db: Session = Depends(get_db)):
    try:
        user = add_money_service(
            db=db, 
            user_id=data.user_id, 
            sum=data.sum
        )
    except NegativeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Negative sum is not allowed')
    
    return user


@router.post('/payments/remove')
def remove_money(data: MoneyOperation, db: Session = Depends(get_db)):
    try:
        user = remove_money_service(
            db=db, 
            user_id=data.user_id, 
            sum=data.sum
        )
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with ID {data.user_id} not found')

    except BalanceError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'User balance is lower than {data.sum}')

    except NegativeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Negative sum is not allowed')
    
    return user


@router.post('/payments/transfer')
def transfer_money(data: TransferOperation, db: Session = Depends(get_db)):
    try:
        user2 = transfer_money_service(
            db=db, 
            user1_id=data.user1_id,
            user2_id=data.user2_id,
            sum=data.sum
        )
    except NegativeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Negative sum is not allowed')

    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')

    except BalanceError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'User balance is lower than {data.sum}')

    except SameUserError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Transferring money to yourself is not allowed')
    
    return user2