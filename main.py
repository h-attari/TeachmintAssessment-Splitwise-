from splitwise import SplitService, SplitType
from users import Users


# Inputs
user1 = Users("u1", "user1", 1029384756, "user1@test.com")
user2 = Users("u2", "user2", 1029465739, "user2@test.com")
user3 = Users("u3", "user3", 1129456739, "user3@test.com")
user4 = Users("u4", "user4", 1224965739, "user4@test.com")

split_service = SplitService()
split_service.show_balance()
split_service.show_balance(user=user1)

split_service.expense(amount_paid=1000,
    user_owed=user1,
    num_users=4,
    users=[user1, user2, user3, user4],
    split_type=SplitType.EQUAL)
split_service.show_balance(user=user4)
split_service.show_balance(user=user1)

split_service.expense(amount_paid=1250,
    user_owed=user1,
    num_users=2,
    users=[user2, user3],
    split_type=SplitType.EXACT,
    split_amount=[370, 880])
split_service.show_balance()

split_service.expense(amount_paid=1200,
    user_owed=user4,
    num_users=4,
    users=[user1, user2, user3, user4],
    split_type=SplitType.PERCENT,
    split_amount=[40, 20, 20, 20])
split_service.show_balance(user=user1)
split_service.show_balance()