import ssdp

class SSDPProtocol(ssdp.SimpleServiceDiscoveryProtocol):

    locations = {}
    def get_locations(self):
        return self.locations

    def response_received(self, response, addr):
        #Store Locations
        locationHeader = response.get_header('LOCATION')
        USN = response.get_header('USN')
        if locationHeader and USN:
            self.locations[USN[1]] = locationHeader[1]

    def request_received(self, request, addr):
        #Not Implemented
        print(request, addr)