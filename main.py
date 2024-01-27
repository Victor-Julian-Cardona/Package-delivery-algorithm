"""Victor Cardona 001264553"""

import datetime
import time_distance_keeper

#declare while loop that repeats itself until user inputs a valid option
valid_option = False
while valid_option == False:
    #ask user if he wants to see total distance or package status
    option = input("Please enter '1' to view total distance traveled by trucks, '2' to view the status of a package at a certain time, or '3' to view the status and info at all packagegs at a certain time: ")

    #verify that user input is valid
    if option == "1" or option == "2" or option == "3":

        valid_option = True

        #if final package distance option is chosen, print final distance traveled by all trucks
        if option == "1":
            final_miles = time_distance_keeper.find_final_distance()
            print ("The total distance traveled by all trucks is: " + str(final_miles) + " miles.")
        
        #if package status option is chosen, get package id and time
        elif option == "2":

            #validate first user input is valid military time, if not, keep asking.
            #if input is valid, record input an turn into int
            valid_hours = False
            while valid_hours == False:
                hours = input("Enter hours in military time: ")
                try:
                    hours = int(hours)
                    if hours >=0 and hours <=23:
                        valid_hours = True
                    else:
                        print("Invalid input, please enter valid military hour from 0 to 23")

                except ValueError:
                    print("Invalid input, please enter valid military hour from 0 to 23")

            #validate second input is valid number of minutes, if not, keep asking.
            #if input is valid, record input an turn into int
            valid_minutes = False
            while valid_minutes == False:
                minutes = input("Enter minutes: ")
                try:
                    minutes = int(minutes)
                    if minutes >=0 and minutes < 60:
                        valid_minutes = True
                    else:
                        print("Invalid input, please enter valid number of minutes")
            
                except ValueError:
                    print("Invalid input, please enter valid number of minutes")

            #validate if third input is an integer, and if there is a package with that id, if not, keep asking
            valid_package_id = False
            while valid_package_id == False:
                package_id = input("Enter package ID to verify status: ")
                try:
                    package_id = int(package_id)
                    if package_id >= 1 and package_id <= 40:
                        valid_package_id = True
                    else:
                        print("There is no package with that ID, please enter a valid id (1 - 40)")
                except ValueError:
                    print("Please enter a valid integer")

            #print line with package status if all inputs were valid
            status  = time_distance_keeper.get_package_status(package_id, datetime.time(hours, minutes))
            print ("Package " + str(package_id) + " is " + status)
    
        elif option == "3":
            
            #validate first user input is valid military time, if not, keep asking.
            #if input is valid, record input an turn into int
            valid_hours = False
            while valid_hours == False:
                hours = input("Enter hours in military time: ")
                try:
                    hours = int(hours)
                    if hours >=0 and hours <=23:
                        valid_hours = True
                    else:
                        print("Invalid input, please enter valid military hour from 0 to 23")

                except ValueError:
                    print("Invalid input, please enter valid military hour from 0 to 23")

            #validate second input is valid number of minutes, if not, keep asking.
            #if input is valid, record input an turn into int
            valid_minutes = False
            while valid_minutes == False:
                minutes = input("Enter minutes: ")
                try:
                    minutes = int(minutes)
                    if minutes >=0 and minutes < 60:
                        valid_minutes = True
                    else:
                        print("Invalid input, please enter valid number of minutes")
            
                except ValueError:
                    print("Invalid input, please enter valid number of minutes")
            
            #print the information of all packages at a certain time
            all_statuses  = time_distance_keeper.get_all_statuses(datetime.time(hours, minutes))

    #ask user for input again if option chosen input is invalid
    else:
        print("Please enter a valid option")