import snap7

def connection(ip='10.10.1.50', rack=0, slot=1):

    client = snap7.client.Client()
    client.connect(ip, rack, slot)
    client.get_connected()

    return client
    

