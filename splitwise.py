from typing import List, Optional, Union
from collections import defaultdict
from enum import Enum
from users import Users


class SplitType(Enum):
    EQUAL = 'equal'
    EXACT = 'exact'
    PERCENT = 'percent'


class TransactionType(Enum):
    OWE = 'owe'
    LEND = 'lend'


class Transaction:
    def __init__(self, amount: int, user: Users, type: TransactionType):
        self.amount = amount
        self._type = type
        self.user = user

    @property
    def owed(self) -> bool:
        return self._type == TransactionType.OWE

    @property
    def lent(self) -> bool:
        return self._type == TransactionType.LEND


class SplitService:
    def __init__(self):
        self.transactions_for_users = defaultdict(list)

    def expense(self, amount_paid: int, user_owed: Users, num_users: int, users: List[Users], split_type: SplitType, split_amount: Optional[List[Union[int, float]]] = None):
        self.validate(split_type=split_type, split_amount=split_amount, num_users=num_users, amount_paid=amount_paid)
        if split_type == SplitType.EQUAL:
            amount_owed = amount_paid / num_users
            for user in users:
                if user == user_owed:
                    continue    
                self.transactions_for_users[user_owed].append(Transaction(user=user, amount=amount_owed, type=TransactionType.LEND))
                self.transactions_for_users[user].append(Transaction(user=user_owed, amount=amount_owed, type=TransactionType.OWE))
        if split_type == SplitType.EXACT:
            for user, amount_owed in zip(users, split_amount):
                if user == user_owed:
                    continue
                self.transactions_for_users[user_owed].append(Transaction(user=user, amount=amount_owed, type=TransactionType.LEND))
                self.transactions_for_users[user].append(Transaction(user=user_owed, amount=amount_owed, type=TransactionType.OWE))
        if split_type == SplitType.PERCENT:
            for user, owed_percent in zip(users, split_amount):
                if user == user_owed:
                    continue
                amount_owed = round((amount_paid * owed_percent / 100), 2)
                
                self.transactions_for_users[user_owed].append(Transaction(user=user, amount=amount_owed, type=TransactionType.LEND))
                self.transactions_for_users[user].append(Transaction(user=user_owed, amount=amount_owed, type=TransactionType.OWE))

    def validate(self, split_type: SplitType, split_amount: List[int], num_users: int, amount_paid: int):
        if split_type == SplitType.EQUAL:
            return
        if split_type == SplitType.EXACT:
            if num_users != len(split_amount):
                raise Exception(f'The number of users owing {len(split_amount)}, does not equal the total number of users {num_users}')
            if amount_paid != sum(split_amount):
                raise Exception(f'The sum of the split amount {split_amount} = {sum(split_amount)} does not equal the total amount paid {amount_paid}')
        if split_type == SplitType.PERCENT:
            if num_users != len(split_amount):
                raise Exception(f'The number of users owing {len(split_amount)}, does not equal the total number of users {num_users}')
            if 100 != sum(split_amount):
                raise Exception(f'The total percentage of {sum(split_amount)} does not equal 100')

    def calculate_transactions(self, user: Users):
        if user not in self.transactions_for_users:
            print(f'No balances for {user.id}')
            return {}
        transaction_map = defaultdict(int)
        users_in_debt = defaultdict(list)
        for transaction in self.transactions_for_users[user]:
            if transaction.owed:
                transaction_map[transaction.user] += transaction.amount
            if transaction.lent:
                transaction_map[transaction.user] -= transaction.amount
        if all(amount_owed == 0 for _, amount_owed in transaction_map.items()):
            return {}
        for other_user, amount_owed in transaction_map.items():
            amount_owed = round(amount_owed, 2)
            if amount_owed < 0:
                users_in_debt[other_user].append((user, abs(amount_owed)))
            if amount_owed > 0:
                users_in_debt[user].append((other_user, amount_owed))
        return users_in_debt

    def show_balance(self, user: Optional[Users] = None):
        users_in_debt = defaultdict(list)
        if user:
            print('====' * 10)
            print(f'showing transactions for user: {user.id}\n')
            users_in_debt = self.calculate_transactions(user=user)
        else:
            print('====' * 10)
            print('showing transactions for all\n')
            for user in self.transactions_for_users.keys():
                for user_in_debt, owed_users in self.calculate_transactions(user=user).items():
                    users_in_debt[user_in_debt] = list(set(users_in_debt[user_in_debt] + owed_users))
        if not users_in_debt:
            print('No balances')
        for user_in_debt, users_owed in users_in_debt.items():
            for (user_owed, amount_owed) in users_owed:
                print(f'{user_in_debt.id} owes {user_owed.id}: {abs(amount_owed)}')
