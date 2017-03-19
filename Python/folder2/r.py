import socket
import hashlib
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = ""
port = 60000

s.connect((host, port))
# while 1:
#     s.send("Hello server!")
# f = open('received_file', 'a+')
# print 'file opened'
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
        f = open(spc[2],'wb+')
        print " downloading"
        while True:
            data = s.recv(1024)
            # print('data=%s\n', (data))
            # print data
            # print "recieved one chunk!!!!!!!!!!!!!!!!!!!!!"
            # temp=data.split("\n")
            # print temp

            last=len(data)

            if data[last-1]=="\0":
                f.write(data[:-1])
                f.close()

                f = open(spc[2],'rb')
                md5 = hashlib.md5()
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    md5.update(data)
                f.close()
                # # print("MD5: {0}".format(md5.hexdigest()))
                hashval = format(md5.hexdigest())
                # print "hashval=",hashval
                hashrec=s.recv(1024)
                print "hasrec=",hashrec
                if str(hashrec)==str(hashval):
                    print "Download succesfull"
                else:
                    print "nahi hua"
                f.close()
                break
            else:
                f.write(data)

        # f.close()
    else:
        data=s.recv(1024)
        if not data:
            continue
        print data


# f.close()
print('Successfully get the file')
s.close()
print('connection closed')
