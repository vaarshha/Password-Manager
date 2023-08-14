from modules import *


def main():
	
	password = input("Main password:")
	
	if verify_pass(password):
		db_obj = database()
		db_obj.check_validity()
		choice = input("A. To add pass B. To retrieve \nC.Update 4.Delete: ")
		if choice == 'A':
			add_pass(db_obj)
		elif choice=='B':
			retrieve_pass(db_obj)
		elif choice == 'C':
			update_password(db_obj)
		elif choice=='D':
			delete_pass(db_obj)
		else:
			print("Invalid option")
		db_obj.close_connection()
	else:
		print("Invalid password")
	

if __name__ == "__main__":
	main()


	
