# -*- coding: utf-8 -*-
"""
@author: sadiuysal
"""

def cType(words):
    catAppend=open('catalog.dat', 'a+', encoding='utf-8')
    tName=words[2]
    ftoW=open(tName+'.dat', 'a+', encoding='utf-8')
    ftoW.close()
    noF=words[3]
    nLine=str(1)+tName.ljust(10)+noF #max type name 10 char
    for i in words[4:]:
        nLine+=(i.ljust(8)) #max field name 8char
    nLine=nLine.ljust(60)
    #print(nLine)
    catAppend.write(nLine)
    #print("i created")   
    catAppend.close()
           
def dType(words):
     tName=words[2]
     catR=open('catalog.dat', 'r+', encoding='utf-8')
     ftoW=open((tName+'.dat'), 'w+', encoding='utf-8')
     ftoW.close()     
     cFind=catR.read()
     nFind=list(cFind)
     i=0     
     while(i*60<len(cFind)):
         if ((cFind[1+60*i:11+60*i]==tName.ljust(10))and(cFind[0+60*i]=='1')): 
             nFind[0+60*i]='0' #update state byte
             catR.close()
             catW=open('catalog.dat', 'w+', encoding='utf-8')
             catW.write(''.join(nFind))
             catW.close()
             break
         i+=1
     catR.close()
def lType():
     catR=open('catalog.dat', 'r+', encoding='utf-8')
     cFind=catR.read()
     list=[]
     i=0
     #print(len(cFind))
     while(i*60<len(cFind)):
         if cFind[0+60*i]=='1': 
             list.append(cFind[1+60*i:11+60*i])#since assumption max. type name length=10
         i+=1
     list.sort()
     if(len(list)!=0):
         for i in list:
             #print(i)
             out.write(i+"\n")
     
     catR.close()
def fEmptyS(page): #finds empty slot
     i=0
     while(9+i*49<len(page)):
        if page[9+49*i]=='1':
             i+=1
        else:
            return i
     return 21 #max record in a page+1
def convert(page): #converts to a string
    # Converting list to string
    s=''
    for i in range(len(page)) :
        s+=page[i]    
    return(s) 
def recordSplitter(str): #splitting record fields to print
    i=0
    x=[]
    s=''
    while i*8<len(str):
        x.append(str[i*8:(i+1)*8])
        i+=1
    for j in x:
        s+=j
    return s
              
def cRecord(words):
    tName=words[2]
    ftoW=open((tName+'.dat'), 'a+', encoding='utf-8')
    ftoR=open((tName+'.dat'), 'r+', encoding='utf-8')
    ftoI=open(('Ind'+tName+'.dat'), 'a+', encoding='utf-8')
    nLine=str(1)
    for i in words[3:]:
        nLine+=(i.ljust(8)) #max field value=8 char
    nLine=nLine.ljust(49)
    i=0
    file=ftoR.read()
    if(len(file)==0):
        Pheader='0'.ljust(3)+'1'.ljust(3)+'1'.ljust(3)  #pageID+ nof records+ first empty slot
        ftoW.write((Pheader+nLine).ljust(1024))
        ftoI.write(nLine[1:9]+'$'+'0'.ljust(3)) #update index file
    else:
        while(i*1024<len(file)): #1024byte>>pagesize
            pStart=1024*i
            pEnd=1024*(i+1)
            nFile=str(convert(file))
            if(int(nFile[pStart+3:pStart+6])==20):
                i+=1
            else:
                if(int(nFile[pStart:pStart+3])!=i): #check page is new or not if new then assign a pageID
                   nFile[pStart:pStart+3]=(str(i)).ljust(3) 
                ftoI.write(nLine[1:9]+'$'+nFile[pStart:pStart+3]) #update index file (12 bytes p.key+$+pageID)
                list0=list(nFile)
                fEmpty=int(nFile[pStart+6:pStart+9])
                nofR=int(nFile[pStart+3:pStart+6])
                list0[(9+(fEmpty)*49):(9+(fEmpty+1)*49)]=nLine #update record slot                 
                #print("i changed "+nFile[(9+(fEmpty)*49):(9+(fEmpty+1)*49)]+"TO "+nLine)
                list0[pStart+3:pStart+6]=(str(nofR+1)).ljust(3) #increment #of records
                emptyS=fEmptyS(list0[pStart:pEnd]) #find new first empty slot
                #print(emptyS)
                list0[pStart+6:pStart+9]=(str(emptyS)).ljust(3)  #update empty slot 
                nFile=''.join(list0)
                ftoW.close()
                ftoR.close()
                fWrite=open((tName+'.dat'), 'w', encoding='utf-8')
                fWrite.write(nFile)
                fWrite.close()    
                break
    ftoI.close()
    ftoW.close()
    ftoR.close()

def dRecord(words):
    tName=words[2]
    pKey=words[3]
    ftoI=open(('Ind'+tName+'.dat'), 'r+', encoding='utf-8')
    ftoR=open((tName+'.dat'), 'r+', encoding='utf-8')
    oldF=ftoR.read()
    newF=list(oldF)  #to be able to change content
    oldI=ftoI.read() #read
    newI=list(oldI)
    pageID=0  #######################################
    i=0
    while(i*12<len(oldI)):
        if(oldI[12*i:12*i+9]==pKey.ljust(8)+'$'):
            pageID=int(oldI[12*i+9:12*i+9+3])
            newI[12*i:12*(i+1)]=''.ljust(12) #update index file (12 bytes p.key+$+pageID)
            break
        else:
            i+=1
    i=0
    pStart=1024*pageID
    pEnd=1024*(pageID+1)
    while(pStart+9+49*i<pEnd):
        if(oldF[pStart+9+49*i+1:pStart+9+49*i+1+8]==pKey.ljust(8)):
            newF[pStart+9+49*i:pStart+9+49*(i+1)]=''.ljust(49) #delete record
            #print(tName+" deleted record >>"+oldF[pStart+9+49*i:pStart+9+49*(i+1)])
            nofR=int(oldF[pStart+3:pStart+6])
            newF[pStart+3:pStart+6]=(str(nofR-1)).ljust(3) #update number of records
            emptyS=fEmptyS(newF[pStart:pEnd]) #find new first empty slot
            newF[pStart+6:pStart+9]=(str(emptyS)).ljust(3)  #update empty slot
            break
        else:
            i+=1
    #print(tName +"  "+ pKey)        
    #print("old index " + oldI)
    #print("new  index "+ convert(newI))
    ftoR.close()
    ftoI.close()
    ftoWI=open(('Ind'+tName+'.dat'), 'w+', encoding='utf-8')
    ftoWI.write(''.join(newI)) #write new index file
    ftoWI.close()
    ftoW=open((tName+'.dat'), 'w+', encoding='utf-8')
    ftoW.write(''.join(newF)) #write new file
    ftoW.close()
    
def uRecord(words):
    tName=words[2]
    pKey=words[3]
    nLine=str(1)
    for i in words[3:]:
        nLine+=(i.ljust(8)) #max field value=8 char
    nLine=nLine.ljust(49)
    ftoI=open(('Ind'+tName+'.dat'), 'r+', encoding='utf-8')
    ftoR=open((tName+'.dat'), 'r+', encoding='utf-8')
    oldF=ftoR.read()
    newF=list(oldF)  #to be able to change content
    oldI=ftoI.read() #read
    pageID=0  #######################################
    i=0
    while(i*12<len(oldI)): #finds pageID from indexfile
        if(oldI[12*i:12*i+9]==words[3].ljust(8)+'$'):
            pageID=int(oldI[12*i+9:12*i+9+3])
            break
        else:
            i+=1
    i=0
    pStart=1024*pageID
    pEnd=1024*(pageID+1)
    while(pStart+9+49*i<pEnd): #start byte of the records to last record
        if(oldF[pStart+9+49*i+1:pStart+9+49*i+1+8]==pKey.ljust(8)):
            newF[pStart+9+49*i:pStart+9+49*(i+1)]=nLine #update record
            #print(tName+" old record >>"+oldF[pStart+9+49*i:pStart+9+49*(i+1)]+" updated record >>"+nLine)
            break
        else:
            i+=1
    ftoR.close()
    ftoI.close()
    ftoW=open((tName+'.dat'), 'w+', encoding='utf-8')
    ftoW.write(''.join(newF)) #write new file
    ftoW.close()
def sRecord(words):
    tName=words[2]
    pKey=words[3]
    record=[pKey]
    ftoIn=open(('Ind'+tName+'.dat'), 'a+', encoding='utf-8') #in case there in no index file
    ftoIn.close()
    ftoRe=open((tName+'.dat'), 'a+', encoding='utf-8')  # in case there is no such type.dat file
    ftoRe.close()
    ftoI=open(('Ind'+tName+'.dat'), 'r+', encoding='utf-8') #then read index file
    ftoR=open((tName+'.dat'), 'r+', encoding='utf-8') 
    oldF=ftoR.read()
    oldI=ftoI.read() #read
    pageID=0  #######################################
    i=0
    while(i*12<len(oldI)):#finds pageID from indexfile
        if(oldI[12*i:12*i+9]==words[3].ljust(8)+'$'):
            pageID=int(oldI[12*i+9:12*i+9+3])
            break
        else:
            i+=1
    i=0
    pStart=1024*pageID
    pEnd=1024*(pageID+1)
    while(pStart+9+49*i<pEnd): #start byte of the records to last record
        if(oldF[pStart+9+49*i+1:pStart+9+49*i+1+8]==pKey.ljust(8)):  #checks pKey equality
            record=oldF[pStart+9+49*i+1:pStart+9+49*(i+1)] #split record fields
            #print(recordSplitter(record))
            out.write(recordSplitter(record)+"\n")
            break
        else:
            i+=1
    ftoR.close()
    ftoI.close()

def lRecords(words):
    records=[]
    tName=words[2]
    ftoRe=open((tName+'.dat'), 'a+', encoding='utf-8')
    ftoRe.close()
    ftoR=open((tName+'.dat'), 'r+', encoding='utf-8')
    oldF=ftoR.read()
    i=0
    while(1024*i<len(oldF)): #checks file size
        page=oldF[1024*i:1024*(i+1)]
        if (page[3:6]!=''):
            if(int(page[3:6])!=0):  #checks number of records byte 
                j=0
                while(9+49*j<1024):                
                    if page[9+49*j]=='1':
                        record=page[9+49*j+1:9+49*(j+1)]
                        records.append([int(record[:8]),record]) #split record fields to sort
                    j+=1
        
        i+=1
    records.sort(key=itemgetter(0), reverse=False)
    #records.sort()   #sort it
    if(len(records)!=0):
        for r in records:
            out.write(r[1]+"\n")#write it to output
            #print(r[1])
    
    ftoR.close()
    

#catAppend0=open('catalog.dat', 'w', encoding='utf-8')
import sys
from operator import itemgetter

out=open(sys.argv[2], "a+")
with open(sys.argv[1], "r+") as f:
    for line in f:
        words=(line.split())
        opr=words[:2]
        if(opr==['create','type']):
            cType(words)
        elif opr==['delete','type']:
            dType(words)
        elif opr==['list','type']:
            lType()
        elif opr==['create','record']:
            cRecord(words)
        elif opr==['delete','record']:
            dRecord(words)
        elif opr==['update','record']:
            uRecord(words)
        elif opr==['search','record']:
            sRecord(words)
        elif opr==['list','record']:
            lRecords(words)
        else :            
            print("Unknown operation")
            
#catAppend0.close()




