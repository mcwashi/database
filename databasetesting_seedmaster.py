import psycopg2,re
try:
    conn = psycopg2.connect("dbname='reactions' user='postgres' host='localhost' password='testing!@3'")
except:
    print "didn't work"
    #other user snake password pyth0n! dbname='reactions'
KEGGlong={}
cur = conn.cursor()
def createtable():
    print "Creating Table..."
    cur.execute("CREATE TABLE seed_compounds (KEGGcpd varchar, SEEDcpd varchar, cpdID varchar, ChEBI varchar, Names varchar);")
    #cur.execute("CREATE TABLE test2 (KEGGID varchar PRIMARY KEY, KEGGEC varchar, SEEDID varchar, SEEDEC varchar, NITIID varchar, NITIEC varchar, PalssonID varchar, PalssonEC varchar, KEGGReaction varchar, NitiReaction varchar, SEEDReaction varchar, PalssonReaction varchar, VALID varchar);")
    keggcpd=open("/home/snorris/Ubuntu One/Thesis Project/Scrapy/tutorial/tutorial/cpd")#
    for each in keggcpd:
        each=re.sub("\n", '',each)
        each=re.split("\t|;|:", each)
        KEGGID=each[1]
        if each[2]!='':
            KEGGshort=each[2]
        if each[3:]!='':
            for x in each[3:]:
                try:
                    KEGGlong[KEGGID]+=x
                except:
                    KEGGlong[KEGGID]=x
        for every in test:
            print every[0]
            if KEGGID==every[0]:
           # cur.execute("UPDATE master_compounds SET cpdID=%s where keggcpd=%s;",(KEGGID,individual))
                continue
            else:
                try:
                    cur.execute("INSERT INTO seed_compounds (KEGGcpd,Names) VALUES(%s,%s)", (KEGGID,' '.join([KEGGlong[KEGGID],KEGGshort])))
                    print "Adding: ",KEGGID
                except:
                    continueme
    #    except:
       #     cur.execute("INSERT INTO seed_compounds (KEGGcpd,ShortName) VALUES(%s,%s)", (KEGGID,KEGGshort))
    keggcpd.close()
    conn.commit()
def addSEED():
    print "Populating SEED data"
    seedcpd=open("/home/snorris/Ubuntu One/Thesis Project/rxndb/ModelSEED-compounds-db.txt")
    seedcpd.readline()
    for each in seedcpd:
        each=re.split("\t",each)
        SEEDID=each[0]
        SEEDREF=each[4]
        SEEDREF=re.split("\|",SEEDREF)
        SEEDNAME=re.sub("\|"," ",each[3])
        SEEDALL=' '.join([each[1],each[2],SEEDNAME])
        for individual in SEEDREF:
            if individual !='':
                cur.execute("INSERT INTO seed_compounds (KEGGcpd,SEEDcpd,Names) VALUES(%s,%s,%s)", (individual, SEEDID, SEEDALL))
            else:
                cur.execute("INSERT INTO seed_compounds (SEEDcpd,Names) VALUES(%s,%s)", (SEEDID,SEEDALL))
               # print "Something went wrong with:",SEEDREF,SEEDID
               # cur.execute("INSERT INTO master_compounds (KEGGcpd,ShortName) VALUES(%s,%s)", (KEGGID,KEGGshort))
        # for every in test:
        #    for individual in SEEDREF:
         #       if every[0] == individual:
                    #cur.execute("UPDATE master_compounds SET seedcpd=%s where keggcpd=%s;",(SEEDID,individual)) #update the database
          #      else:
           #         print individual," not found"
    seedcpd.close()
    conn.commit()
def addcompoundDB():
    print "Starting Compound DB merge"
    cpdDB=open("/home/snorris/Ubuntu One/Thesis Project/rxndb/compound_database_v2.txt")
    cpdDB.readline()
    for each in cpdDB:
        each=re.split("\t",each)
        cpdDBID=each[0]
        cpdDBREF=each[4]
        cpdDBREF=re.split("\|",cpdDBREF)
        for every in test:
            for individual in cpdDBREF:
                if every[0] == individual:
                    cur.execute("UPDATE seed_compounds SET cpdID=%s where keggcpd=%s;",(cpdDBID,individual))
              #  else:
            #        print individual," not found"
    cpdDB.close()
    conn.commit()
def addChEBI():
    print "Starting ChEBI Merge"
    cur.execute("SELECT * FROM database_accession WHERE type ='KEGG COMPOUND accession';")
    chebitest=cur.fetchall()
    cur.execute("SELECT * FROM compounds;")
    chebicpd=cur.fetchall()
    for each in chebitest:
        ChEBIREF=each[2]
        ChEBIID=each[1]
        for every in test:
            if each[2] == every[0]:
                cur.execute("UPDATE seed_compounds SET ChEBI=%s where keggcpd=%s;",(ChEBIID,ChEBIREF))
            else:
                for other in chebicpd:
                    ChEBIname=other[1]
                    ChEBIIDs=other[0]
                    cur.execute("INSERT INTO seed_compounds (ChEBI,names) VALUES(%s,%s);",(ChEBIIDs,ChEBIname))
# cur.execute("SELECT ...; DELETE FROM compounds WHERE keggcpd='';)
# # # # # Call the functions # # # # # # #

cur.execute("SELECT * FROM seed_compounds;")
test=cur.fetchall()
#createtable() #create the initial table and populate it with KEGG IDs
#addSEED() #add the seed database data
#addcompoundDB() #add the niti database data
addChEBI() #add the ChEBI database data

cur.execute("SELECT * from master_compounds where keggcpd='C00001';")
print cur.fetchone()
conn.commit()
cur.close()
conn.close()