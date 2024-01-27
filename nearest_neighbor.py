import math
import data_loader
import hash_table

#Create package hash table to be used to keep track of packages and their status
package_hash = data_loader.load_data('Packages.csv')

#Create list of addresses to be used for reference when calculating distances and comparing addresses
address_list = data_loader.create_location_list("Address List.csv")

#Create table of distances between addresses to be used when
distance_list = data_loader.create_distance_list("Distances.csv", 27)

#return id of a single given address
def get_address_id(address):

    count = 0
    address_id = None

    for current_address in address_list:
        if [address] == current_address:
            address_id = count
        count += 1
    
    #return addresses where errors occurr
    if address_id == None:
        address_id = 1
        print([address])

    return address_id


#return distance between two given location ids
def get_distance(address1_id, address2_id):

    if distance_list[address1_id][address2_id] != "":
        distance = distance_list[address1_id][address2_id]

    else:
        distance = distance_list[address2_id][address1_id]

    distance = float(distance)
    return distance

#return address id of a given package id
def packageID_to_adressID(package_id):
    address_id  = get_address_id(package_hash.lookup(int(package_id)).address)
    return address_id


#make sublist of pacakges
def make_sublist(sublist_ids):

    paired_sublist = []

    for id in sublist_ids:
        sublist_package = package_hash.lookup(int(id))
        paired_sublist.append(sublist_package)

    return paired_sublist

#Check sublist for an eligible package to load and update package in hash table
def nearest_sublist_package(sublist, curr_address_id):

    global normal_sublist
    global package_hash

    #check if there are packages in the sublist
    if len(sublist) > 0:
        min_distance = math.inf
        #check which sublist package to deliver next with greedy algorithm
        for package in sublist:
            #check if sublist package is ready to be delivered in the current truck
            package_distance = get_distance(curr_address_id, get_address_id(package.address))
            if package_distance < min_distance:

                #record information of chosen package
                min_distance = package_distance
                min_id = package.id
                chosen_package = package
        
        #remove chosen package from sublist and update package status in hash table
        sublist.remove(chosen_package)
        package_to_load = min_id
        package_hash.on_route_status(min_id)
        
        #return package to load id
        return package_to_load
    
    #return false if sublist was empty
    else:
        return False

#Create sublist of packages that can be on either truck at any time
normal_list = [2, 4, 5, 7, 10, 11, 12, 17, 22, 23, 24, 26, 27, 33, 34, 35, 39]
normal_sublist = make_sublist(normal_list)

#load truck 1 to depart at 8:00
def load_truck1_first():

    global normal_sublist
    global package_hash

    final_load = []

    #Specify which packages should be loaded on truck 1 at 8:00am
    initial_load = [1, 13, 14, 15, 16, 19, 20, 21, 29, 30]
    initial_load_sublist = make_sublist(initial_load)
    curr_address_id = 0
    loading = True

    #load packages specific to truck 1 at 8:00 in order using greedy algorithm
    while loading:

        package_to_load = nearest_sublist_package(initial_load_sublist, curr_address_id)

        if package_to_load != False:
            final_load.append(package_to_load)
            curr_address_id = packageID_to_adressID(package_to_load)

        else: loading  = False
    
    #load packages from normal packages sublist using greedy algorithm until truck is full
    while len(final_load) < 16:
        package_to_load = nearest_sublist_package(normal_sublist, curr_address_id)

        if package_to_load != False:
            final_load.append(package_to_load)
            curr_address_id = packageID_to_adressID(package_to_load)
        else:
            return final_load
    
    return final_load

#load truck 2 to depart at 9:05 when late packages arrive at hub
def load_truck2():

    global normal_sublist
    global package_hash

    final_load = []

    #Create sublist of packages that must be delivered on truck 2 and depart at 9:05am
    initial_load = [3, 6, 8, 18, 25, 28, 31, 32, 36, 37, 38, 40]
    initial_load_sublist = make_sublist(initial_load)
    curr_address_id = 0
    loading = True

    #Load packages that must be delivered on truck 2 at 9:05 in order with greedy algorithm
    while loading:

        package_to_load = nearest_sublist_package(initial_load_sublist, curr_address_id)

        if package_to_load != False:
            final_load.append(package_to_load)
            curr_address_id = packageID_to_adressID(package_to_load)

        else: loading  = False
    
    #add packages from normal list using greedy algorithm until truck is full
    while len(final_load) < 16:
        package_to_load = nearest_sublist_package(normal_sublist, curr_address_id)

        if package_to_load != False:
            final_load.append(package_to_load)
            curr_address_id = packageID_to_adressID(package_to_load)
        else:
            return final_load
    
    return final_load

#load truck1 at 10:30 after first trip
def load_truck1_second():

    global normal_sublist
    global package_hash

    final_load = []
    curr_address_id = 0

    #add package 9 with the wrong address to the normal list of packages to be delivered
    #this second load will departafter the correct address is known therefore packcage 9 can be delivered
    normal_sublist.append(package_hash.lookup(9))

    #load packages from normal packages sublist using greedy algorithm until truck is full or there are no more packages to be delivered
    while len(final_load) < 16:
        package_to_load = nearest_sublist_package(normal_sublist, curr_address_id)

        if package_to_load != False:
            final_load.append(package_to_load)
            curr_address_id = packageID_to_adressID(package_to_load)
        else:
            return final_load
    
    return final_load