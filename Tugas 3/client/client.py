import sys
import socket
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 9000)
print >> sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
namafile=["pll4.jpg"]

try:
    print "Opt: 1. List Image 2. Request Image 3. Send Image 4. Close"
    while True:
        req = raw_input('>')
        sock.send(req)
        if(req == '1'):
            msg = sock.recv(1024)        
            print msg
        elif(req== '2'):
            namanya = raw_input('nama file > ')
            sock.send(namanya)
            counter = sock.recv(32)
            print counter
            if(counter == '1'):
                while True:
                    data = sock.recv(32)
                    if(data[0:5]=="START"):
                        print data[12:]
                        fp = open(data[12:],'wb+')
                        ditulis=0
                    elif(data[0:6]=="FINISH"):
                        print data[0:6]
                        fp.close()
                        break
                    elif(data[0:3]=="END"):
                        print data[0:3]
                        break
                    else:
                        print "blok ", len(data), data[0:10]
                        fp.write(data)
            else :
                print "nama tidak ada"
            
        elif(req=='3'):
            nama = raw_input('nama file > ')
            sock.send("START {}" . format(nama))
            size = os.stat(nama).st_size
            fp = open(nama,'rb')
            k = fp.read()
            kirim=0
            for x in k:
                sock.send(x)
                kirim = kirim + 1
                print "\r send {} of {} " . format(kirim,size)
            fp.close()
            sock.send("FINISH")
            sock.send("END")
        elif(req=='4'):
            break
finally:
    print >> sys.stderr, 'closing socket'
    sock.close()