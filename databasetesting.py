#!/usr/bin/python
# Written By: Shaun Norris, VCU Bioinformatics MS Student
# norrissw@vcu.edu
# This script is designed to create a master table which containts all of the compound information from SEED, ChEBI, Niti(VCU) and KEGG.
import psycopg2,re # psycopg2 will need to installed
try:
    conn = psycopg2.connect("dbname='reactions' user='postgres' host='localhost' password='testing!@3'") # open that database connection  #other user snake password pyth0n! dbname='reactions'
except:
    print "Unable to connect to database"
    quit()
KEGGlong={}
cur = conn.cursor()
def createtable():
    cur.execute("CREATE TABLE newmaster (KEGGcpd varchar PRIMARY KEY, SEEDcpd varchar, cpdID varchar, ChEBI varchar, Names varchar, Abbreviation varchar);")
#   cur.execute("CREATE TABLE test2 (KEGGID varchar PRIMARY KEY, KEGGEC varchar, SEEDID varchar, SEEDEC varchar, NITIID varchar, NITIEC varchar, PalssonID varchar, PalssonEC varchar, KEGGReaction varchar, NitiReaction varchar, SEEDReaction varchar, PalssonReaction varchar, VALID varchar);")
    keggcpd=open("/home/snorris/Ubuntu One/Thesis Project/Scrapy/tutorial/tutorial/cpd")#
    for each in keggcpd:
        each=re.sub("\n", '',each)
        each=re.split("\t|;|:", each)
        KEGGID=each[1]
        if each[2]!='':
            KEGGshort=each[2]
#         if each[3:]!='':
#             for x in each[3:]:
#                 try:
#                     KEGGlong[KEGGID]+=x
#                 except:
#                     KEGGlong[KEGGID]=x
            cur.execute("INSERT INTO newmaster (KEGGcpd,Abbreviation) VALUES(%s,%s)", (KEGGID,KEGGshort))
    keggcpd.close()
    conn.commit()
def addSEED():
    number=0
    seedcpd=open("/home/snorris/Ubuntu One/Thesis Project/rxndb/ModelSEED-compounds-db.txt")
    seedcpd.readline()
    for each in seedcpd:
        each=re.split("\t",each)
        SEEDID=each[0]
        SEEDREF=each[4]
        SEEDREF=re.split("\|",SEEDREF)
        SEEDNAME=' '.join([each[1],each[2],each[3]])
        for every in test:
            id=len(SEEDREF)-1
            while id >= 0:
                if every[0]==SEEDREF[id]:
                    print "Adding multiple:", SEEDREF[id]
                    cur.execute("UPDATE newmaster SET seedcpd=%s,Names=%s where keggcpd=%s;",(SEEDID,SEEDNAME,SEEDREF[id])) #update the database
                    conn.commit()
                id=id-1
        if each[4] is '':
            print "No Kegg ID matched",SEEDREF,SEEDID
            UNKKegg=str(''.join(["unknown",str(number)]))
            cur.execute("INSERT INTO newmaster (KEGGcpd,SEEDcpd,Names) VALUES(%s,%s,%s)",(UNKKegg,SEEDID,SEEDNAME)) #update the database
            conn.commit()
            number+=1
    seedcpd.close()
    conn.commit()
def addcompoundDB():
    cpdDB=open("/home/snorris/Ubuntu One/Thesis Project/rxndb/compound_database_v2.txt")
    cpdDB.readline()
    number=0
    for each in cpdDB:
        each=re.split("\t",each)
        cpdDBID=each[0]
        cpdDBREF=each[4]
        cpdDBREF=re.split("\|",cpdDBREF)
        cpdDBName=' '.join([each[1],each[2],each[3]])
        for every in test:
            id=len(cpdDBREF)-1
            while id >= 0:
                if every[0]==cpdDBREF[id]:
                    print "Adding multiple:", cpdDBREF[id]
                    cur.execute("UPDATE newmaster SET cpdID=%s where keggcpd=%s;",(cpdDBID,cpdDBREF[id])) #update the database
                    conn.commit()
                id=id-1
        if each[4] is '':
            print "No Kegg ID matched",cpdDBREF,cpdDBID
            try:
                cur.execute("UPDATE newmaster SET cpdID=%s where seedcpd=%s;",(cpdDBID,cpdDBID)) #update the database
            except:
                UNKKegg=str(''.join(["unknown",str(number)]))
                cur.execute("INSERT INTO newmaster (KEGGcpd,SEEDcpd,Names) VALUES(%s,%s,%s)",(UNKKegg,cpdDBID,cpdDBName)) #update the database
                conn.commit()
                number+=1
           # cur.execute("INSERT INTO newmaster (cpdID,Names) VALUES(%s,%s,%s);",(cpdDBID,' '.join([cpdDBName,cpDBAltName])))
    cpdDB.close()
    conn.commit()
def addChEBI():
    cur.execute("SELECT * FROM database_accession WHERE type ='KEGG COMPOUND accession';")
    chebitest=cur.fetchall()
    for each in chebitest:
        ChEBIREF=each[2]
        ChEBIID=each[1]
        for every in test:
            if each[2] == every[0]:
                cur.execute("UPDATE newmaster SET ChEBI=%s where keggcpd=%s;",(ChEBIID,ChEBIREF))
# cur.execute("SELECT ...; DELETE FROM compounds WHERE keggcpd='';)
# # # # # Call the functions # # # # # # #
#createtable() #create the initial table and populate it with KEGG IDs
cur.execute("SELECT * FROM newmaster;")
test=cur.fetchall()
#addSEED() #add the seed database data
addcompoundDB() #add the niti database data#addChEBI() #add the ChEBI database data
addChEBI()

cur.execute("SELECT * from newmaster where keggcpd='C00001';")
print cur.fetchone()
conn.commit()
cur.close()
conn.close()