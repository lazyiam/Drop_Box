import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = ""
port = 60000

s.connect((host, port))
# while 1:
#     s.send("Hello server!")
# f = open('received_file', 'a+')
print 'file opened'
while True:
    inp=raw_input("prompt>>")
    s.send(inp)
    spc=inp.split()
    if inp=="exit":
        break
    elif spc[0]=="download":
        # if spc[1]=="UDP":
        #     f = open(spc[2],'w+')
        #     print " downloading"
        #
        #     while True:
        #         data = s.recv(1024)
        #         temp=data.split("\n")
        #         last=len(temp)
        #         if temp[last-1]=="anuj":
        #             print "Download succesfull"
        #             break
        #         f.write(data)
        #     f.close()
        f = open(spc[2],'w')
        print " downloading"
        while True:
            data = s.recv(1024)
            # print('data=%s\n', (data))
            print data
            print "recieved one chunk!!!!!!!!!!!!!!!!!!!!!"
            temp=data.split("\n")
            # print temp
            last=len(temp)
            if temp[last-1]=="anuj":
                lent=len(data)
                data[lent-4]="\0"
                f.write(data)
                print "Download succesfull"
                break
        f.close()
    else:
        data=s.recv(1024)
        if not data:
            continue
        print data


# f.close()
print('Successfully get the file')
s.close()
print('connection closed')
