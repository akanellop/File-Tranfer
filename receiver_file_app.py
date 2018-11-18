from server import *

def Main():
    #find address
    arg='ip route list'
    p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    data = p.communicate()
    sdata = data[0].split()
    my_address = sdata[ sdata.index('src')+1 ]
    
    lenghtofpacket = int(raw_input("Length of Packet (len): ")) #Length of packets that we want to read
    buffsize = int(raw_input("Enter Storage Size (available slots of received packet length): ")) #Storage unit size
    
    #Starting this side of the app with initialization (returns port for connection)
    fd, port = netpipe_rcv_open(my_address, buffsize)
    if fd == -1:
        print ("Open failed")
        return
    
    #Print socket information 
    print "========================="
    print "Port Number: ", port
    print "IP Address: ", my_address
    print "========================="

    #Creates file and reads data from storage until getting "EOF"
    #(works for 1 file)
    while True:
        (fd, buf) = netpipe_read(fd, lenghtofpacket)
        if fd == -1:
            print "Read Failed"
            return
        
        buftype,chunk = buf

        if buftype == 'S':
            #String data is used for managing the data and file manipulation
            chunk = chunk.decode('utf-8')
            if chunk == "EOF":
                f.close()
                break
            else:
                f = open("new_"+chunk,'wb')
        else:
            #in case datatype is Data we write in the file
            f.write(chunk)

    fd = netpipe_rcv_close(fd)
    if fd != -1:
        print("Close failed")
        return

if __name__ == "__main__":
	Main()
