from client import *

def Main():
    #take connection info for other side
    port = int(raw_input("Enter Port Number: "))
    address = raw_input("Enter IP Address: ")
    print "==========================="
    lengthofpack = int(raw_input("Enter Length of Packet (max = 1024): "))
    buffsize = int(raw_input("Enter Storage Size (available slots of packet length): "))
    print "=============================="
    
    #Starting this side of app with initialization and first handshake
    fd = netpipe_snd_open(address,port,buffsize)
    if fd == -1:
        print ("Open failed")
        return

    filename = raw_input("Enter name of file to be sent: ")
    print "==========================="
    
    #send name of file for opening in receiver side
    buf = ['S', filename]
    length = lengthofpack - sys.getsizeof(fd) - sys.getsizeof(buf[0])
    fd = netpipe_snd_write(fd, buf, length)
    
    #open file to start reading data
    f = open(filename,'rb')
    
    #send data 
    buf[0] = 'D'
    while True:
        buf[1] = f.read(length)
        if buf[1] == '':
            break
        fd = netpipe_snd_write(fd, buf,length)
        
    #send "EOF" for closing file in receiver side
    buf[0] = 'S'
    buf[1] = "EOF"
    fd = netpipe_snd_write(fd, buf,length)
    f.close()


    fd = netpipe_snd_close(fd)
    if fd == 0:
        print("Close failed")
        return


if __name__ == "__main__":
    Main()
