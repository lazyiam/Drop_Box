import socket
import os
import re
import hashlib
import time


port = 60000
port2=40000
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock2=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
host = ""

s.bind((host, port))
s.listen(15)

# filename = raw_input("Enter file to share:")
print 'Server listening....'

conn, addr = s.accept()
def downfun(filename,query):
    if query=="UDP":
        f = open(filename,'rb')
        l = f.read(1024)
        while (l):
            print l
            sock2.sendto(l,(host,port2))
            l = f.read(1024)
        sock2.sendto("\0",(host,port2))
        f.close()
        time.sleep(0.1)
        f=open(comm[2],'rb')
        md5=hashlib.md5()
        while True:
            data = f.read(1024)
            if not data:
                break
            md5.update(data)
        f.close()
        hashval = format(md5.hexdigest())
        f.close()
        print "sending hash"
        sock2.sendto(str(hashval),(host,port2))
        return
    else:
        f = open(filename,'rb')
        l = f.read(1024)
        while(l):
            time.sleep(0.1)
            conn.send(l)
            hashval=hashlib.md5(l).hexdigest()
            time.sleep(0.1)
            conn.send(str(hashval))
            while True:
                x = conn.recv(1024)
                if x=="correct":
                    break
                else:
                    time.sleep(0.1)
                    conn.send(l)
                    time.sleep(0.1)
                    conn.send(str(hashval))
            l=f.read(1024)
        time.sleep(0.1)
        conn.send("f&d")
        time.sleep(0.1)
        conn.send("haha")
        f.close()
        return
def indfun(comm):
    status=1
    if comm[1]=="longlist":
        ret=os.listdir(os.curdir)
        retfin = ''
        temp = os.popen('ls -l').read()
        # print temp
        lines=temp.split("\n")
        count=1
        for i in ret:
            col=lines[count].split()

            stat=os.stat(i)
            retfin += i + ' ' + str (col[5]) + ' '+ str (col[6]) + ' '+ str (col[7]) + ' ' + str(stat.st_size) + '\n'
            count+=1
        conn.send(retfin)

    elif comm[1]=="regex":
        if len(comm)!=3:
            conn.send("wrong arguements")
            status=0
            return
        ret=os.listdir(os.curdir)
        retfin= ''
        for i in ret:
            out = re.search(str(comm[2]),i)
            # stat=os.stat(i)
            # print i
            print out
            if str(out)!="None":
                retfin+= str(i) + "\n"
        if retfin=='':
            conn.send("No Match Found")
        else:
            conn.send(retfin)
    elif comm[1]=="shortlist":
        if len(comm)!=4:
            conn.send("wrong arguments")
            status=0
            return
        ret=os.listdir(os.curdir)
        temp = os.popen('ls -l').read()
        lines = temp.split("\n")

        retfin = ''
        count=1
        for i in ret:
            stat=os.stat(i)
            col=lines[count].split()
            print comm[2],comm[3], stat.st_mtime
            t1 = int(comm[2])<int(stat.st_mtime)
            t2 = int(comm[3])>int(stat.st_mtime)
            # print t1,t2
            if int(stat.st_mtime)>=int(comm[2]) and int(stat.st_mtime)<=int(comm[3]):
                retfin += i + ' ' + str(col[5]) +' '+ str(col[6]) +' '+ str(col[7]) +' ' + str(stat.st_size) + '\n'
        # print retfin
        # print "here"
        if retfin == '':
            conn.send('No files')
        else:
            conn.send(retfin)
    return status
def hashfun(comm):
    if comm[1]=="verify":
        if len(comm)!=3:
            conn.send("wrong arguements")
            # continue
        retfin=''
        stat = os.stat(comm[2])
        md5 = hashlib.md5()
        f=open(comm[2],'rb')
        while True:
            data = f.read(1024)
            if not data:
                break
            md5.update(data)
        f.close()
        # print("MD5: {0}".format(md5.hexdigest()))
        hashval = format(md5.hexdigest())
        retfin+= "checksum--> " + str(hashval) + "\n"
        retfin+= "last modified--> " + str(stat.st_mtime) + "\n"
        if retfin=='':
            conn.send("Invalid Input File")

        else:
            conn.send(retfin)
    elif comm[1]=="checkall":
        if len(comm)!=2:
            conn.send("wrong arguements")
            # continue
        retfin=''
        ret=os.listdir(os.curdir)
        for i in ret:
            hashval=hashlib.md5(i).hexdigest()
            md5 = hashlib.md5()
            f=open(i,'rb')
            while True:
                data = f.read(1024)
                if not data:
                    break
                md5.update(data)
            f.close()
            # print("MD5: {0}".format(md5.hexdigest()))
            hashval = format(md5.hexdigest())
            stat=os.stat(i)
            retfin+= "filename: " + str(i) +" "+ "checksum: "  + str(hashval)+" " + "last modify: " + str(stat.st_mtime) + "\n"
        if retfin=='':
            conn.send("No Files")
        else:
            conn.send(retfin)
    return
#change
def syncfun(filename):
    md5 = hashlib.md5()
    f = open(filename,'rb')
    while True:
        data = f.read(1024)
        if not data:
            break
            #hah
        md5.update(data)
    f.close()
    hashval = format(md5.hexdigest())
    conn.send(str(hashval))
    time.sleep(0.1)
    stat=os.stat(filename)
    temp=int(stat.st_mtime)
    conn.send(str(temp))
    return
while True:
    print "yahan"
    data = conn.recv(1024)
    if data=="exit":
        break
    comm = data.split()
    if len(comm)==0:
        conn.send("wrong args")
        continue
    if comm[0]=="index":
        status=indfun(comm)
        if status==0:
            continue

    elif comm[0]=="hash":
        hashfun(comm)
    elif comm[0]=="download":
        downfun(comm[2],comm[1])
    elif comm[0]=="check_files":
        # while True:
        time.sleep(0.1)
        inp=conn.recv(1024)
        if inp=="Done":
            print "here"
            break
        else:
            syncfun(inp)
        # conn.send("recieved")




print('Done sending')
conn.send('Thank you for connecting')
conn.close()
s.close()
