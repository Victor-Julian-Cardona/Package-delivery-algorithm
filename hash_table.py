import Package

#Define class hash table to hold all package information
class package_hash_table:
    table = []

    #Constructor that declares a list of 10 lists
    def __init__(self, capacity=10):
        self.table == []
        for i in range(capacity):
            self.table.append([])

    #method that returns hash key for a given package_id
    def generate_key(self, id):
        key = int(id) % len(self.table)
        return key
    
    #method that inserts package into hash table
    def insert(self, id, address, city, state, zip, deadline, weight, notes, status):

        new_package = Package.Package(id, address, city, state, zip, deadline, weight, notes, status)

        bucket = self.generate_key(id)
        bucket_list = self.table[bucket]
        bucket_list.append(new_package)

    #method that looks up all package information of a given package_id  
    def lookup(self, id):
        key = self.generate_key(id)

        for package in self.table[key]:
            if int(package.id) == id:
                return package
    
    #method that changes status of given package_id to: "on route"
    def on_route_status(self, id):
        key = self.generate_key(id)

        for package in self.table[key]:
            if package.id == id:
                package.status = "on route"
    
    #method that changes status of given package_id to "delivered at: given time""
    def delivered_status(self, id, time):
        key = self.generate_key(id)

        for package in self.table[key]:
            if int(package.id) == id:
                package.status = "delivered at: " + str(time)

    #method to print all packages in hash table
    def print_hash(self):
        for i in range(10):
            for package in self.table[i]:
                print("Id: " + package.id + " Address: " + package.address + " City: " + package.city + " State: " + package.state + " Zip: " + package.zip + " Deadline: " + package.deadline + " Weight: " + package.weight + " Status: " + package.status)

