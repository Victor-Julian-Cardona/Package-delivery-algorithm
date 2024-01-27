import csv
import hash_table

#function to create list of all possible addresses loading data from address csv
def create_location_list(fileName):

    final_location_list = []
    
    with open(fileName) as location_list:
        location_data = csv.reader(location_list, delimiter=',')
        for col in location_data:
            final_location_list.append(col)
    return final_location_list

#function to create table of all distances between addresses loading data from distance csv
def create_distance_list(fileName, addresses):

    distance_table = []
        
    for i in range(addresses):
            distance_table.append([])
            for t in range(addresses):
                distance_table[i].append([])


    with open(fileName) as distance_list:
        distance_data = csv.reader(distance_list, delimiter=',')
        entry_count = 0
        for row in distance_data:
            for i in range(addresses):
                distance_table[entry_count][i] = row[i]
            entry_count += 1
        
        return distance_table

#function to populate hashtable with all data from package csv
def load_data(fileName):

    hash_map = hash_table.package_hash_table()

    with open(fileName) as package_list:
        package_data = csv.reader(package_list, delimiter=',')
        for package in package_data:
            package_id = package[0]
            package_address = package[1]
            package_city = package[2]
            package_state = package[3]
            package_zip = package[4]
            package_arrival_time = package[5]
            package_weight = package[6]
            package_notes = package[7]
            status = "at the hub"

            hash_map.insert(package_id, package_address, package_city, package_state, package_zip, package_arrival_time, package_weight, package_notes, status)
    
    return hash_map