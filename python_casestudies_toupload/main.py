from gym_manager import GymManager
from promo_manager import PromoManager

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

if __name__ == "__main__":
    
    gym_manager = GymManager()
    gym_manager.main_menu()
    gym_manager.save_data()  

