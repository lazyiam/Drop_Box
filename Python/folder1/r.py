import socket
import hashlib
import time
import os
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock2=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
host = ""
sock2.bind((host, 40000))
port = 60000
port2 = 40000
#an
s.connect((host, port))
# while 1:
#     s.send("Hello server!")
# f = open('received_file', 'a+')
# print 'file open'
last_update=time.time()
def downfil(filename,typeq):
    if typeq=="UDP":
        f = open(filename,'wb+')
        print "downloading"
        while True:
            data, adr = sock2.recvfrom(1024)

            last=len(data)

            if data[last-1]=="\0":
                f.write(data[:-1])
                f.close()

                f = open(filename,'rb')
                md5 = hashlib.md5()
                while True:
                    data = f.read(1024)
                    if not   data:
                        break
                    md5.update(data)
                f.close()
                # # print("MD5: {0}".format(md5.hexdigest()))
                hashval = format(md5.hexdigest())
                # print "hashval=",hashval
                hashrec, adr =sock2.recvfrom(1024)
                print "hasrec=",hashrec
                if str(hashrec)==str(hashval):
                    print "Download successfull"
                else:
                    print "nahi hua"
                f.close()
                break
            else:
                f.write(data)
    # else
    else:
        f = open(filename,'wb+')
        print " downloading"
        while True:
            # print 'In true'
            data = s.recv(1024)
            print 'recieved'
            print data
            last=len(data)
            hashrec = s.recv(1024)
            hashval = str(hashlib.md5(data).hexdigest())

            print "hashval=",hashval
            print "hashrec=",hashrec
            if str(hashval) == str(hashrec):
                # time.sleep(0.1)
                s.send("correct")
                print "correct chunk"
                # time.sleep(0.1)

            else:
                # time.sleep(0.1)
                if hashrec!="haha":
                    s.send("error")
                    print "incorrect chunk"
                # time.sleep(0.1)
                    continue
                else:
                    s.send("correct")
                    print "correct chunk"



            if len(data)==1:

                f.close()
                break
            if  data[last-1] == '' or data=="f&d" :
                print 'EOF'
                # tm = s.recv(1024)
                # f.write(data)
                f.close()
                break
            f.write(data)
    return
def hashfun(filename):
    md5= hashlib.md5()
    f=open(filename,'rb')
    while True:
        data = f.read(1024)
        if not data:
            break
        md5.update(data)
    f.close()
    hashval = format(md5.hexdigest())
    return str(hashval)
flag=0
while True:
    if time.time()-last_update>3 :
        print "checking files"
        files = os.listdir(os.curdir)
        for m in files:
            i=str(m)
            time.sleep(0.1)
            s.send("check_files")
            time.sleep(0.1)
            s.send(i)
            hashrec=s.recv(1024)
            hashi=hashfun(i)
            stat=os.stat(i)
            recmtime=s.recv(1024)
    	    # print "recmtime=",recmtime
            # print "myfile=",int(stat.st_mtime)
            if hashi!=hashrec and (int(stat.st_mtime) < int(recmtime)):
                time.sleep(0.1)
                print "upadated:",i
                se="download UDP"+" "+str(i)
                s.send(se)
                downfil(i,"UDP")
                time.sleep(0.1)
        # s.send("check_files")
        # time.sleep(0.1)
        # s.send("Done")
        last_update=time.time()

        # s.recv()
    else:
        inp = raw_input("prompt>>")
        if not inp :
            print "Enter Command"
        else:
            spc=inp.split()
            if spc[0]=="download"  or spc[0]=="index" or spc[0]=="hash" or inp=="exit":
                s.send(inp)
                if inp=="exit":
                    break
                elif spc[0]=="download":
                    downfil(spc[2],spc[1])
                # flag=0

                    # f.close()
                else:
                    data=s.recv(1024)
                    if not data:
                        continue
                    print data
            else:
                print "wrong command"


# f.close()
print('Successfully get the file')
s.close()
print('connection closed')
