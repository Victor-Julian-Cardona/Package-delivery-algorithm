#Create package class to be able to access individual package components
class Package:
        def __init__(self, id, address, city, state, zip, deadline, weight, notes, status):
            self.id = id
            self.address = address
            self.city = city
            self.state = state
            self.zip = zip
            self.deadline = deadline
            self.weight = weight
            self.notes = notes
            self.status = status
    
        #function to print package info instead of package class instance
        def __str__(self):
            return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.id, self.address, self.city, self.state, self.zip, self.deadline, self.weight, self.notes, self.status)
        

             
    