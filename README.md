# SplitWise - Expense Sharing App


## Overview
Splitwise is an expense sharing sharing app through which a group of people can share and divide their expenses among themselves as they deem right.


## Database Schema
The system would mainly contain of 3 Tables/Schemas to store the data of Users, Expenses/Transactions and the relation between the users and expenses respectively.
A demo schema for same is been defined in the module named - `database_schema.py`


## API Structure
The system would implement mainly 3 APIs:  
- Add user:  
This API will be used to add users to the system and would require 3 parametes:  
&nbsp; - Name,  
&nbsp; - Mobile Number, and  
&nbsp; - Email  
Id of the user should be generated automatically.

- Add Expense:  
This API will be used to add the any transaction or expense into the system of any amount with following details:  
&nbsp; - User object paying for the expense.  
&nbsp; - List of users the expense needs to be splited among.  
&nbsp; - Amount of the transaction/expense.  
&nbsp; - Type of the split need to be implemented.  

- Get Balance:  
This API will be used to fetch the current balance of the users.


The basic implementation of the classes need for the system is implemented in the modules:  
- `users.py`, and
- `splitwise.py`  

with the working examples specified in `main.py`.
