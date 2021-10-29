"""
#
# Ihop, Island HOPper for TravelWare Pacific Ocean
#
# 26.10.2021 VN/ViWare
#
"""

class CustomerHops:
    """
    # class CustomerHops
    #
    # One customers hop transports as a list for the whole route
    # Includes no sanity checking. If that would be required, can be added.
    # Hops with no preference marked as ANY
    # Keeps track for compulsory hops
    # Keeps track whether customer is made satisfied with at least one preferred hop included in the final route.
    # Takes a nosedive when it becomes evident there will be no suitable itinerary
    """
    itsCompulsory=False # If only one hop specified for customer, it's compulsory then
    itsSatisfied=False # Customer will be satisfied, if one hop is a match.
    itsHopTransports={} # Customers transports over each hop. ANY if no preference given
    
    def __init__(self, inputLine, nofHops):
        self.itsLine=inputLine
        self.itsNofHops=nofHops
        self.itsHopTransports=dict(onehop.strip().split(' ') for onehop in self.itsLine.split(','))
        if len(self.itsHopTransports)==1: self.itsCompulsory=True
        # Fill in sparse matrix
        for hop in range(self.itsNofHops):
            self.itsHopTransports.update({str(hop):self.itsHopTransports.get(str(hop),'ANY')})
        
        
    def isSatified(self):
        return self.itsSatisfied
    
        
    def __str__(self):
        return str(self.itsHopTransports) + (" Compulsory!" if self.itsCompulsory else " Not Compulsory!") + ("Satisfied" if self.itsSatisfied else " Not Satisfied")
    
# All routelines as list of single RouteLine objects
class AllCustomerHops:
    """
    # All routelines as list of single RouteLine objects
    """
    itsCustomerHops=[]

    def __init__(self):
        itsCustomerHops=[]
        
    def areSatisfied(self):
        for customerHop in self.itsCustomerHops:
            print(customerHop.isSatified())
        
    def __str__(self):
        return '\n'.join(str(p) for p in self.itsCustomerHops)

    
class Itinerary:
    """
    # Itinerary itself with suitable methods
    """
    
    def __init__(self, allCustomerHops):
        self.itsAllCustomerHops=allCustomerHops
        self.itsItinerary={}
        self.itsAlreadyHasCompulsory=[] # If a compulsory transport has been honored by a previous customer
        self.itsCustomerWished=[] # Is this wished already by a customer
        
    def pickTransport(self,hop):
        self.itsAlreadyHasCompulsory.append(False);
        self.itsCustomerWished.append(False);
        self.itsAlreadyHasCompulsory[hop]=False;
        self.itsItinerary[str(hop)]='by-sea'
        
        for customerhop in self.itsAllCustomerHops.itsCustomerHops: # This hop through all customers
            # Pick up the transport for this hop. by-sea initially. Replace with compulsory one if one comes by. If yet another compulsory appears,give up.
            if customerhop.itsCompulsory:
                if customerhop.itsHopTransports.get(str(hop))!='ANY': # Compulsory has only one other than ANY, remember. More elegant solution preferred by OO
                    if self.itsAlreadyHasCompulsory[hop]: sys.exit('NO ITINERARY'); # Also here a more elegant solution would be required
                    self.itsAlreadyHasCompulsory[hop]=True
                    self.itsItinerary[str(hop)]=customerhop.itsHopTransports.get(str(hop))
                    self.itsCustomerWished[hop]=True;
                    customerhop.itsSatisfied=True
                                                               
            # Update this hop's transport if appropriate
            if self.itsAlreadyHasCompulsory[hop]==False: # Only update if there wasn't a compulsory one for a previouscustomer
                if customerhop.itsHopTransports.get(str(hop))!='ANY':
                    if self.itsCustomerWished[hop]==False and customerhop.itsSatisfied==False:
                        self.itsItinerary[str(hop)]=customerhop.itsHopTransports.get(str(hop))
                        self.itsCustomerWished[hop]=True;
                        customerhop.itsSatisfied=True
            
            # If this customers transport is the one already selected for this hop in itinenary, customer will be satisfied
            if customerhop.itsHopTransports.get(str(hop)).startswith(self.itsItinerary[str(hop)][0:1]): customerhop.itsSatisfied=True
        
    def __str__(self):
        return ''.join(hop+" "+self.itsItinerary[hop]+', ' for hop in self.itsItinerary)[:-2]

#
# Main program
#
import sys    
print("\n\nIhop, Island HOPper for TravelWare Pacific Ocean\n\n")

nofLines=0
allCustomerHops=AllCustomerHops()

# Read input to an AllCustomerHops object.
with open('input.txt', 'r') as infile:
    nofHops=int(infile.readline())
    nofCustomers=int(infile.readline())
    for line in infile:
        allCustomerHops.itsCustomerHops.append(CustomerHops(line, nofHops))
        
# Try finding satisfactory initinerary
itinerary=Itinerary(allCustomerHops)
# Hop by hop
for hop in range(nofHops):
    itinerary.pickTransport(hop)

print(itinerary)

allCustomerHops.areSatisfied()


