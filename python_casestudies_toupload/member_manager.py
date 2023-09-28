import pandas as pd
from datetime import datetime, timedelta

class MemberManager:
    

    def save_data(self):
  
         self.member_details.to_csv('member_details.csv', index=False,mode='a')
         self.member_transaction.to_csv('member_transaction.csv', index=False,mode='a')
         self.gym_revenue.to_csv('gym_revenue.csv', index=False,mode='a')
member_details_df = pd.read_csv('member_details.csv')
member_transaction_df = pd.read_csv('member_transaction.csv')
gym_revenue_df = pd.read_csv('gym_revenue.csv')

# Display the contents of the DataFrames
print("Member Details:")
print(member_details_df)

print("\nMember Transactions:")
print(member_transaction_df)

print("\nGym Revenue:")
print(gym_revenue_df)
