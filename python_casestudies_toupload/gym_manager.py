import pandas as pd
import random
import string
from datetime import datetime, timedelta

class GymManager:
    RATE_PER_MONTH = 1000 
    
    def __init__(self):
        self.promo_details = pd.DataFrame({'promo_code': ['DIGITALU', 'TTECDIGI', 'COOLGUYS', 'HYDBAD12'],
                                         'discount_fraction': [0.59, 0.47, 0.31, 0.17]})
        self.member_details = pd.read_csv('member_details.csv')
        self.member_transaction = pd.read_csv('member_transaction.csv')
        self.gym_revenue = pd.read_csv('gym_revenue.csv')
        self.cleric_codes = ['cleric123', 'passkey456']

    def generate_random_passkey(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def get_member_info(self, mobile_number):
        member_info = self.member_details[self.member_details['mobile_number'] == mobile_number]
        if not member_info.empty:
            return member_info.iloc[0]
        return None

    def member_exists(self, mobile_number):
        return mobile_number in self.member_details['mobile_number'].tolist()

    def validate_dob(self, dob):
        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d')
            today = datetime.now()
            age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
            return 14 <= age <= 80
        except ValueError:
            return False

    def calculate_and_record_payment(self, member_info, duration_months, promo_code):
        mobile_number = member_info['mobile_number']
        if promo_code in self.promo_details['promo_code'].tolist():
            discount = self.promo_details[self.promo_details['promo_code'] == promo_code]['discount_fraction'].values[0]
        else:
            discount = 0

        amount_payable = duration_months * self.RATE_PER_MONTH * (1 - discount)
        print(f"Amount payable: {amount_payable} INR")
        passkey = input("Please enter the amount and your clerical passkey to confirm: ").strip()
        if passkey not in self.cleric_codes:
            print("Invalid passkey. Transaction aborted.")
            return

        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration_months * 30)
        self.member_transaction = self.member_transaction._append({'mobile_number': mobile_number,
                                                                'membership_startdate': start_date,
                                                                'membership_enddate': end_date,
                                                                'is_active': True}, ignore_index=True)
        self.gym_revenue = self.gym_revenue._append({'mobile_number': mobile_number,
                                                    'paydate': start_date,
                                                    'amount_paid': amount_payable}, ignore_index=True)

        print("Payment added. Membership is active.")
        self.main_menu()
    def is_active_member(self, mobile_number):
        today = datetime.now()
        member_info = self.get_member_info(mobile_number)
        if member_info is not None:
            start_date = self.get_membership_start_date(mobile_number)
            end_date = self.get_membership_end_date(mobile_number)

            return start_date <= today <= end_date
        return False

    def get_membership_start_date(self, mobile_number):
        transaction = self.member_transaction[self.member_transaction['mobile_number'] == mobile_number]
        if not transaction.empty:
            return transaction.iloc[0]['membership_startdate']
        return None

    def get_membership_end_date(self, mobile_number):
        transaction = self.member_transaction[self.member_transaction['mobile_number'] == mobile_number]
        if not transaction.empty:
            return transaction.iloc[0]['membership_enddate']
        return None
    
    def check_summary_page(self):
        print("\nCheck Summary")
        print("1. Total Member")
        print("2. Total Revenue of the Gym")
        print("3. 15 Days Renewal Member")
        choices = input("Enter your choice(s) separated by spaces: ").strip().split()

        if '1' in choices:
            total_members = len(self.member_transaction[self.member_transaction['is_active'] == True])
            print(f"Total Active Members: {total_members}")

        if '2' in choices:
            self.gym_revenue['amount_paid'] = pd.to_numeric(self.gym_revenue['amount_paid'], errors='coerce')
            total_revenue = self.gym_revenue['amount_paid'].sum()
            print(f"Total Revenue of the Gym: {total_revenue} INR")
        if '3' in choices:
            today = datetime.today()

            # Convert the 'membership_enddate' column to integers (assuming it contains hours)
            self.member_transaction['membership_enddate'] = pd.to_numeric(self.member_transaction['membership_enddate'], errors='coerce')

            # Calculate the date 15 days from today
            renewal_date_limit = today + timedelta(days=15)

            renewal_members = self.member_transaction[
                (self.member_transaction['membership_enddate'] >= today.timestamp()) &
                (self.member_transaction['membership_enddate'] <= renewal_date_limit.timestamp())
            ]

            if not renewal_members.empty:
                print("Members with membership renewal in the next 15 days:")
                for index, row in renewal_members.iterrows():
                    member_info = self.get_member_info(row['mobile_number'])
                    print(f"Name: {member_info['name']}, Mobile: {member_info['mobile_number']}")

            self.main_menu()


        # if '3' in choices:
        #     today = datetime.today()

        #     # Convert the 'membership_enddate' column to integers (assuming it contains hours)
        #     self.member_transaction['membership_enddate'] = pd.to_numeric(self.member_transaction['membership_enddate'], errors='coerce')

        #     # Calculate the date by adding the number of hours to the current date
        #     self.member_transaction['membership_enddate'] = today + pd.to_timedelta(self.member_transaction['membership_enddate'], unit='hours')

        #     # Calculate the date 15 days from today
        #     renewal_date_limit = today + timedelta(days=15)

        #     renewal_members = self.member_transaction[(self.member_transaction['membership_enddate'] >= today) &
        #                                             (self.member_transaction['membership_enddate'] <= renewal_date_limit)]

        #     if not renewal_members.empty:
        #         print("Members with membership renewal in the next 15 days:")
        #         for index, row in renewal_members.iterrows():
        #             member_info = self.get_member_info(row['mobile_number'])
        #             print(f"Name: {member_info['name']}, Mobile: {member_info['mobile_number']}")

        #     self.main_menu()

        # if '3' in choices:
        #     # today = datetime.now()
        #     today = datetime.today()
        #     self.member_transaction['membership_enddate'] = pd.to_datetime(self.member_transaction['membership_enddate'])

        #     # Assuming 'today' is a datetime.datetime object
        #     # today = datetime.today()
        #     # today = datetime.today().date()
        #     # df = pd.read_csv('your_file.csv')
        #     # df['membership_startdate'] = pd.to_datetime(today.strftime('%Y-%m-%d') + ' ' + df['membership_startdate'])
        #     renewal_members = self.member_transaction[(self.member_transaction['membership_enddate'] >= today) &
        #                                             (self.member_transaction['membership_enddate'] <= today + timedelta(days=15))]
        #     if not renewal_members.empty:
        #         print("Members with membership renewal in the next 15 days:")
        #         for index, row in renewal_members.iterrows():
        #             member_info = self.get_member_info(row['mobile_number'])
        #             print(f"Name: {member_info['name']}, Mobile: {member_info['mobile_number']}")

        # self.main_menu()

    
    def add_member_page(self):
        print("\nAdd Member")
        print("1. Reinstating a Member")
        print("2. A New Member")
        print("3. Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            self.reinstate_member()
        elif choice == '2':
            self.add_new_member()
        elif choice == '3':
            self.main_menu()
        else:
            print("Invalid choice. Please choose a valid option.")
            self.add_member_page()

    def reinstate_member(self):
        mobile_number = input("Please enter the 10-digit mobile number: ").strip()
        if not mobile_number.isdigit() or len(mobile_number) != 10:
            print("Invalid mobile number. Please enter a valid 10-digit mobile number.")
            self.reinstate_member()

        if self.member_exists(mobile_number):
            member_info = self.get_member_info(mobile_number)
            print("Member Details:")
            print(f"Mobile: {member_info['mobile_number']}")
            print(f"Name: {member_info['name']}")
            print(f"Blood Group: {member_info['blood_group']}")
            print(f"Emergency Contact Name: {member_info['emergency_contact_name']}")
            print(f"Emergency Contact Number: {member_info['emergency_contact_number']}")

            duration_months = int(input("Enter the duration of membership in months: "))
            promo_code = input("Enter the promo code (if any): ").strip().upper()

            if not self.validate_promo_code(promo_code):
                print("Invalid promo code. Please enter a valid promo code.")
                self.reinstate_member()

            self.calculate_and_record_payment(member_info, duration_months, promo_code)
        else:
            print("Member with this mobile number does not exist.")
            self.add_member_page()

    def validate_promo_code(self, promo_code):
        return promo_code in self.promo_details['promo_code'].tolist()

    def update_emergency_details(self):
        print("\nUpdate Member's Emergency Contact Details")
        mobile_number = input("Enter the mobile number of the member to update: ").strip()
        member_info = self.get_member_info(mobile_number)

        if member_info is not None:
            new_emergency_contact_name = input("Enter new emergency contact name: ").strip()
            if not new_emergency_contact_name.replace(" ", "").isalpha():
                print("Invalid emergency contact name. Name should only contain letters.")
                self.update_emergency_details()
            new_emergency_contact_number = input("Enter new emergency contact number: ").strip()
            if not new_emergency_contact_number.isdigit():
                print("Invalid emergency contact number. Please enter a valid number.")
                self.update_emergency_details()

            self.member_details.loc[self.member_details['mobile_number'] == mobile_number,
                                    ['emergency_contact_name', 'emergency_contact_number']] = \
                [new_emergency_contact_name, new_emergency_contact_number]

            print("Emergency contact details updated successfully.")
        else:
            print("Member with this mobile number does not exist.")
        self.main_menu()

    def add_new_member(self):
        print("\nAdd New Member")
        mobile_number = input("Please enter the 10-digit mobile number: ").strip()

        if not mobile_number.isdigit() or len(mobile_number) != 10:
            print("Invalid mobile number. Please enter a valid 10-digit mobile number.")
            self.add_new_member()

        if self.member_exists(mobile_number):
            print("Member with this mobile number already exists. Please use the 'Reinstate a Member' option.")
            self.add_member_page()

        name = input("Enter full name: ").strip()
        if not name.replace(" ", "").isalpha():
            print("Invalid name. Name should only contain letters.")
            self.add_new_member()

        dob = input("Enter date of birth (YYYY-MM-DD): ").strip()
        if not self.validate_dob(dob):
            print("Invalid date of birth. Age should be between 14 and 80 years.")
            self.add_new_member()

        blood_group = input("Enter blood group (A/B/O/AB +/-): ").strip().upper()
        if blood_group not in ['A', 'B', 'O', 'AB'] or not set(blood_group).issubset(['A', 'B', 'O', 'AB', '+', '-']):
            print("Invalid blood group. Please enter a valid blood group.")
            self.add_new_member()

        emergency_contact_name = input("Enter emergency contact name: ").strip()
        if not emergency_contact_name.replace(" ", "").isalpha():
            print("Invalid emergency contact name. Name should only contain letters.")
            self.add_new_member()

        emergency_contact_number = input("Enter emergency contact number: ").strip()
        if not emergency_contact_number.isdigit():
            print("Invalid emergency contact number. Please enter a valid number.")
            self.add_new_member()

        duration_months = int(input("Enter the duration of membership in months: "))
        promo_code = input("Enter the promo code (if any): ").strip().upper()

        if not self.validate_promo_code(promo_code):
            print("Invalid promo code. Please enter a valid promo code.")
            self.add_new_member()

        # Create a new member entry
        self.member_details = self.member_details._append({'mobile_number': mobile_number,
                                                          'name': name,
                                                          'blood_group': blood_group,
                                                          'emergency_contact_name': emergency_contact_name,
                                                          'emergency_contact_number': emergency_contact_number},
                                                         ignore_index=True)

        self.calculate_and_record_payment(self.get_member_info(mobile_number), duration_months, promo_code)

        print("New member added successfully.")
        self.main_menu()

    def main_menu(self):
        print("\nWelcome to the T-Gym Member Management Application")
        print("Please choose among the below options:")
        print("1. Adding New Member")
        print("2. Member Details")
        print("3. Check Summary")
        print("4. Update Member’s Emergency Contact Details")
        print("5. Exit the System")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            self.add_member_page()
        elif choice == '2':
            self.member_details_page()
        elif choice == '3':
            self.check_summary_page()
        elif choice == '4':
            self.update_emergency_details()
        elif choice == '5':
            self.save_data()
            exit(0)
        else:
            print("Invalid choice. Please choose a valid option.")

    def member_details_page(self):
        print("\nMember Details")
        mobile_number = input("Enter the mobile number of the member: ").strip()
        member_info = self.get_member_info(mobile_number)

        if member_info is not None:
            print("Member Details:")
            print(f"Mobile: {member_info['mobile_number']}")
            print(f"Name: {member_info['name']}")
            print(f"Blood Group: {member_info['blood_group']}")
            print(f"Emergency Contact Name: {member_info['emergency_contact_name']}")
            print(f"Emergency Contact Number: {member_info['emergency_contact_number']}")
            print(f"Membership Start Date: {self.get_membership_start_date(mobile_number)}")
            print(f"Membership End Date: {self.get_membership_end_date(mobile_number)}")

            more_info_choice = input("Do you want to see more details? (yes/no): ").strip().lower()
            if more_info_choice == 'yes':
                print("Additional Details:")
                if self.is_active_member(mobile_number):
                    print("Membership Status: Active")
                else:
                    print("Membership Status: Inactive")
                self.view_payment_history(mobile_number)
            else:
                self.main_menu()
        else:
            print("Member with this mobile number does not exist.")
            self.main_menu()

    def view_payment_history(self, mobile_number):
        payment_history = self.gym_revenue[self.gym_revenue['mobile_number'] == mobile_number]
        if not payment_history.empty:
            print("Payment History:")
            for index, row in payment_history.iterrows():
                print(f"Payment Date: {row['paydate']}, Amount Paid: {row['amount_paid']} INR")
        else:
            print("No payment history available for this member.")

        self.main_menu()

    def save_data(self):
        try:
            
            self.promo_details.to_csv('promo_details.csv', index=False,mode='a')
            self.member_details.to_csv('member_details.csv', index=False,mode='a')
            self.member_transaction.to_csv('member_transaction.csv', index=False,mode='a')
            self.gym_revenue.to_csv('gym_revenue.csv', index=False,mode='a')
            print("Data saved successfully.")
        except Exception as e:
            print(f"Error saving data: {str(e)}")
if __name__ == "__main__":
    gym_manager = GymManager()
    gym_manager.main_menu()

            