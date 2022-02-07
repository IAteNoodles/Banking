#The interface to interact with the apis.
if __name__ == '__main__':
    print("Welcome to the Bank API")
    print("Enter the number of the function you want to use:")
    print("1: Help")
    print("2: Login")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        print("Help:")
        print("This is the help page of the Bank API.")
        #TODO: Add more help pages.
    elif choice == 2:
        print("This is the User login page")
        print("Are you a user? (y/n)")
        choice = input("Enter your choice: ")
        if choice == "y":
            user_id = input("Enter your id: ")
            password = input("Enter your password: ")
            from Banking_.API.Users import User
            current_login_object = User(user_id, password)
        elif choice == "n":
            #To access the login page of a staff, one must know the secret key provided only to the staff.
            secret = "15c35469c06da2482fce9a249537f255d8c057ce9beea39926a394efc8696a1f3376c54a1315bc0b2d48715e21ab42bd2eeb85ba50e2b11c90e8f9dcc5f4191b"
            key = input("Enter the secret key")
            if key == secret:
                print("This is the staff login page")
                staff_id = input("Enter your id: ")
                password = input("Enter your password: ")
                from Banking_.API.Staffs import Staff
                current_login_object = Staff(staff_id, password)
            else:
                print("Invalid secret key")
                print("Exiting...")
        else:
            print("Invalid choice")
            print("Exiting...")