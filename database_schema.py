from enum import Enum


class Users:
    id: str
    name: str
    mobile: str
    email: str


class Transactions:
    id: int
    type: Enum # Choices among -> Equal, Exact and Percent.
    paid_by: Users # Many-to-One Field
    shared_by: Users #Many-to-Many Relation


class SplitTransaction:
    """Intermediate model for many-to-many relation of Transactions to Users"""
    user: Users
    trxn: Transactions
    shared_amount: float