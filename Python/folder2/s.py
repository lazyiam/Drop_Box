import socket
import os
import re
import hashlib

port = 60000
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = ""

s.bind((host, port))
s.listen(15)

filename = raw_input("Enter file to share:")
print 'Server listening....'

conn, addr = s.accept()
while True:
    print "yahan"
    data = conn.recv(1024)
    if data=="exit":
        break
    comm = data.split()
    if comm[0]=="index":
        if comm[1]=="longlist":
            ret=os.listdir(os.curdir)
            retfin = ''
            for i in ret:
                stat=os.stat(i)
                retfin += i + ' ' + str  (stat.st_mtime) + ' ' + str(stat.st_size) + '\n'

            conn.send(retfin)

        elif comm[1]=="regex":
            if len(comm)!=3:
                conn.send("wrong arguements")
                continue
            ret=os.listdir(os.curdir)
            retfin= ''
            for i in ret:
                out = re.search(str(comm[2]),i)
                # stat=os.stat(i)
                # print i
                print out
                if str(out)!="None":
                    retfin+= str(i)
            if retfin=='':
                conn.send("No Match Found")
            else:
                conn.send(retfin)
        elif comm[1]=="shortlist":
            if len(comm)!=4:
                conn.send("wrong arguments")
                continue
            ret=os.listdir(os.curdir)
            retfin = ''
            for i in ret:
                stat=os.stat(i)
                print comm[2],comm[3], stat.st_mtime
                t1 = int(comm[2])<int(stat.st_mtime)
                t2 = int(comm[3])>int(stat.st_mtime)
                print t1,t2
                if int(stat.st_mtime)>=int(comm[2]) and int(stat.st_mtime)<=int(comm[3]):
                    retfin += i + ' ' + str(stat.st_mtime) + ' ' + str(stat.st_size) + '\n'
            print retfin
            print "here"
            if retfin == '':
                conn.send('No files')
            else:
                conn.send(retfin)
    elif comm[0]=="hash":
        if comm[1]=="verify":
            if len(comm)!=3:
                conn.send("wrong arguements")
            retfin=''
            # for i in ret:
            #     stat = os.stat(i)
            stat = os.stat(comm[2])
            hashval = hashlib.md5(comm[2]).hexdigest()
            retfin+= "checksum--> " + str(hashval) + "\n"
            retfin+= "last modified--> " + str(stat.st_mtime) + "\n"
            if retfin=='':
                conn.send("Invalid Input File")

            else:
                conn.send(retfin)
        elif comm[1]=="checkall":
            if len(comm)!=2:
                conn.send("wrong arguements")
            retfin=''
            ret=os.listdir(os.curdir)
            for i in ret:
                hashval=hashlib.md5(i).hexdigest()
                stat=os.stat(i)
                retfin+= "filename: " + str(i) +" "+ "checksum: "  + str(hashval)+" " + "last modify: " + str(stat.st_mtime) + "\n"
            if retfin=='':
                conn.send("No Files")
            else:
                conn.send(retfin)
    elif comm[0]=="download":

        f = open(comm[2],'rb')
        l = f.read(1024)
        while (l):
            print l
            conn.send(l)
        #    print('Sent ',repr(l))
            l = f.read(1024)
        conn.send("anuj")
        f.close()

print('Done sending')
conn.send('Thank you for connecting')
conn.close()
s.close()
