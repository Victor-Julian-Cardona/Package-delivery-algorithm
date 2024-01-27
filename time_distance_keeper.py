import nearest_neighbor
import datetime
import math

#method to add distances from hub to delivery location
def add_distances(truck_load, index):

    total_distance = 0

    #specify that address1 is the hub when calculating distance of first package to be delivered in load
    #dont run loop if the distance to find is the first package
    if index == 0:
        address1_id = 0
        address2_id = nearest_neighbor.packageID_to_adressID(truck_load[0])
        total_distance = total_distance + nearest_neighbor.get_distance(address1_id, address2_id)

    
    else:
        for i in range(index):
            #specify that address1 is the hub when calculating distance of first package to be delivered in load
            if i == 0:
                address1_id = 0
                address2_id = nearest_neighbor.packageID_to_adressID(truck_load[i])

            #specify that address1 is the current package address and address2 is the next package address for all packages beyond the first one
            else:
                address1_id = nearest_neighbor.packageID_to_adressID(truck_load[i])
                address2_id = nearest_neighbor.packageID_to_adressID(truck_load[i+1])
            
            #add individual distances to addresses until reaching the package address
            total_distance = total_distance + nearest_neighbor.get_distance(address1_id, address2_id)

    #return the total distance and the address id of the last package delivered
    return total_distance, address2_id


#function to find total distance traveled round trip of a given truck load
def find_total_distance(truck_load):

    #add all distances until final package delivered in truck load
    delivery_distance = add_distances(truck_load, (len(truck_load)-1))

    #add distance to return back to hub
    total_distance = delivery_distance[0] + nearest_neighbor.get_distance(delivery_distance[1], 0)

    #return total round trip distance
    return total_distance

#method to return total distance traveled by all trucks
def find_final_distance():
    
    #define all truck loads
    first_load = nearest_neighbor.load_truck1_first()
    second_load = nearest_neighbor.load_truck2()
    third_load = nearest_neighbor.load_truck1_second()

    #find total distance traveled by each truck
    first_miles = find_total_distance(first_load)
    second_miles = find_total_distance(second_load)
    third_miles = find_total_distance(third_load)

    #sum all distances traveled
    final_miles = first_miles + second_miles + third_miles

    return final_miles

#method to calculate minutes and hours required to traverse a specified distance
def extra_time_calc(distance):
        extra_time = distance/18
        hours = math.floor(extra_time)
        extra_seconds = (extra_time - hours) * 3600
        minutes = math.ceil(extra_seconds/60)
        
        return int(hours), int(minutes)


#Method to find which load the specified package was loaded on, returns the load and the index of the package in said load
def check_package_load(package_id, first_load, second_load, third_load):

    #check fist load
    count = 0
    for id in first_load:
        if int(package_id) == int(id):
            return "first", count
        count += 1
    
    #check second load
    count = 0
    for id in second_load:
        if int(package_id) == int(id):
            return "second", count
        count += 1

    #check third load
    count = 0
    for id in third_load:
        if int(package_id) == int(id):
            return "third", count
        count += 1
        
    return "package id not found"

#method to get the delivery time of a specified package
def get_delivery_time(package_id, first_load, second_load, third_load):

    #get package load and index
    load = check_package_load(package_id, first_load, second_load, third_load)

    if load == "package id not found":
        return None

    #get time for a package found in the first load
    if load[0] == "first" and load[0]:
        extra_time = extra_time_calc(add_distances(first_load, load[1])[0])
        total_time = datetime.timedelta(hours = 8) + datetime.timedelta(hours = extra_time[0], minutes = extra_time[1])
        return total_time
            
    #get time for a package found in the second load
    if load[0] == "second":
        extra_time = extra_time_calc(add_distances(second_load, load[1])[0])
        total_time = datetime.timedelta(hours = 9, minutes = 5) + datetime.timedelta(hours = extra_time[0], minutes = extra_time[1])
        return total_time
    
    #get time for a package found in the third load
    if load[0] == "third":
        extra_time = extra_time_calc(add_distances(third_load, load[1])[0])
        total_time = datetime.timedelta(hours = 10, minutes = 30) + datetime.timedelta(hours = extra_time[0], minutes = extra_time[1])
        return total_time
    
#Create list of all package delivery times
def get_all_times(num_packages, first_load, second_load, third_load):
    
    delivery_times = []

    for i in range(1, num_packages+1):
        #get delivery timedelta for package
        delivery_time = (get_delivery_time(i, first_load, second_load, third_load))

        #if package has not been loaded append None as delivery time
        if delivery_time == None:
            delivery_times.append(None)
        
        else:
        
            # Convert timedelta to seconds
            total_seconds = delivery_time.total_seconds()
    
            # Calculate hours, minutes, and seconds
            hours = int(total_seconds // 3600)
            minutes = math.ceil(int((total_seconds % 3600) / 60))
        
            #set delivery time as time object
            delivery_time = datetime.time(hours, minutes)

            #append delivery time to delivery_times list
            delivery_times.append(delivery_time)
    
    return delivery_times

#updates all package statuses for a given time.
def update_statuses(time):

    #declare departure times for each truck load
    first_departure = datetime.time(8, 0)
    second_departure = datetime.time(9, 5)
    third_departure = datetime.time(10, 30)

    first_load = []
    second_load = []
    third_load = []

    #if specified  time is past the first truck departure, set all packages loaded on first truck to "on route"
    if time >= first_departure:
        first_load = nearest_neighbor.load_truck1_first()

    #if specified  time is past the first truck departure, set all packages loaded on second truck to "on route"
    if time >= second_departure:
        second_load = nearest_neighbor.load_truck2()

    #if specified  time is past the first truck departure, set all packages loaded on third truck to "on route"
    if time >= third_departure:
        third_load = nearest_neighbor.load_truck1_second()

    #get list of delivery times
    delivery_times = get_all_times(40, first_load, second_load, third_load)

    #if specified time is past the delivery time of a package, set that package status to "delivered"
    count = 1
    for delivered_time in delivery_times:
        if delivered_time != None and time >= delivered_time:
                nearest_neighbor.package_hash.delivered_status(int(count), delivered_time)
        count += 1

#method that returns the status of a given package at a given time
def get_package_status(id, time):

    #set all statuses based on given time
    update_statuses(time)

    #look up status of given package
    status = nearest_neighbor.package_hash.lookup(id).status

    return status

#method that prints all package statuses at a certain time
def get_all_statuses(time):

    #update all statuses
    update_statuses(time)

    #print all package is and statuses
    nearest_neighbor.package_hash.print_hash()