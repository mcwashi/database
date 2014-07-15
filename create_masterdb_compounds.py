#!/usr/bin/python
# create_masterdb_compounds.py
# Written By: Shaun Norris, VCU Bioinformatics MS Student
# norrissw@vcu.edu
# This script is designed to create a master table which containts all of the compound information from SEED, ChEBI, Niti(VCU) and KEGG.
import psycopg2,re,sys,getopt # psycopg2 will need to installed
from collections import defaultdict
from libsbml import *
def create_cpd_table(): # This function creates the table "compounds_master"
    cur.execute("CREATE TABLE kegg_compounds (KEGGcpd varchar PRIMARY KEY, SEEDcpd varchar, cpdID varchar, ChEBI varchar, Names varchar, Abbreviation varchar);")
    keggcpd=open("/home/snorris/Ubuntu One/Thesis Project/Scrapy/tutorial/tutorial/cpd") 
    for each in keggcpd:
        each=re.sub("\n", '',each)
        each=re.split("\t|;|:", each)
        KEGGID=each[1]
        if each[2]!='':
            KEGGshort=each[2:]
            cur.execute("INSERT INTO kegg_compounds (KEGGcpd,Abbreviation) VALUES(%s,%s)", (KEGGID,KEGGshort))
    keggcpd.close()
    conn.commit()
def addSEED(): # Add Seed Compounds to the table
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
                    cur.execute("UPDATE compounds_master SET seedcpd=%s,Names=%s where keggcpd=%s;",(SEEDID,SEEDNAME,SEEDREF[id])) #update the database
                    conn.commit()
                id=id-1
        if each[4] is '':
            print "No Kegg ID matched",SEEDREF,SEEDID
            UNKKegg=str(''.join(["unknown",str(number)]))
            cur.execute("INSERT INTO compounds_master (KEGGcpd,SEEDcpd,Names) VALUES(%s,%s,%s)",(UNKKegg,SEEDID,SEEDNAME)) #update the database
            conn.commit()
            number+=1
    seedcpd.close()
    conn.commit()
def addcompoundDB(): # Add the compounds database file to the table
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
                    cur.execute("UPDATE compounds_master SET cpdID=%s where keggcpd=%s;",(cpdDBID,cpdDBREF[id])) #update the database
                    conn.commit()
                id=id-1
        if each[4] is '':
            print "No Kegg ID matched",cpdDBREF,cpdDBID
            try:
                cur.execute("UPDATE compounds_master SET cpdID=%s where seedcpd=%s;",(cpdDBID,cpdDBID)) #update the database
            except:
                UNKKegg=str(''.join(["unknown",str(number)]))
                cur.execute("INSERT INTO compounds_master (KEGGcpd,SEEDcpd,Names) VALUES(%s,%s,%s)",(UNKKegg,cpdDBID,cpdDBName)) #update the database
                conn.commit()
                number+=1
           # cur.execute("INSERT INTO compounds_master (cpdID,Names) VALUES(%s,%s,%s);",(cpdDBID,' '.join([cpdDBName,cpDBAltName])))
    cpdDB.close()
    conn.commit()
def addChEBI(): # Add the ChEBI compounds to the table
    cur.execute("SELECT * FROM database_accession WHERE type ='KEGG COMPOUND accession';")
    chebitest=cur.fetchall()
    for each in chebitest:
        ChEBIREF=each[2]
        ChEBIID=each[1]
        for every in test:
            if each[2] == every[0]:
                cur.execute("UPDATE compounds_master SET ChEBI=%s where keggcpd=%s;",(ChEBIID,ChEBIREF))
# # # # # # # # # # # # # Define the Reaction Tables Functions # # # # # # # # # # # # # # # # # # # # #
def create_rxn_table():
    try:
        cur.execute("CREATE TABLE kegg_reactions (KEGGrxn varchar PRIMARY KEY, Name varchar, Named_Reaction varchar, C_Reaction varchar, Enzyme varchar, Pathway varchar, RxnPair varchar, Orthology varchar);")
        conn.commit()
        keggrxn_file=open("/home/snorris/Ubuntu One/Thesis Project/rxndb/all_kegg_rxns")
        dic=defaultdict(defaultdict)
        for line in keggrxn_file.readlines():
            if line.startswith("ENTRY"):
                KEGGRXN=line.split()[1]
                dic[KEGGRXN]
            if line.startswith("NAME"):
                try:
                    dic[KEGGRXN]['NAMES']+=' '.join(line.split()[1:])
                except:
                    dic[KEGGRXN]['NAMES']=' '.join(line.split()[1:])
            else:
                try:
                    dic[KEGGRXN]['NAMES']+=''
                except:
                    dic[KEGGRXN]['NAMES']=''
            if line.startswith("DEFINITION"):
                try:
                    dic[KEGGRXN]['NAMED_REACTION']+=' '.join(line.split()[1:])
                except:
                    dic[KEGGRXN]['NAMED_REACTION']=' '.join(line.split()[1:])
            else:
                try:
                    dic[KEGGRXN]['NAMED_REACTION']+=''
                except:
                    dic[KEGGRXN]['NAMED_REACTION']=''
            if line.startswith("EQUATION"):
                try:
                    dic[KEGGRXN]['C_REACTION']+=' '.join(line.split()[1:])
                except:
                    dic[KEGGRXN]['C_REACTION']=' '.join(line.split()[1:])
            else:
                try:
                    dic[KEGGRXN]['C_REACTION']+=''
                except:
                    dic[KEGGRXN]['C_REACTION']=''
            if line.startswith("RPAIR"):
                try:
                    dic[KEGGRXN]['RPAIR']+=' '.join(line.split()[1:])
                except:
                    dic[KEGGRXN]['RPAIR']=' '.join(line.split()[1:])
            else:
                try:
                    dic[KEGGRXN]['RPAIR']+=''
                except:
                    dic[KEGGRXN]['RPAIR']=''
            if line.startswith("ENZYME"):
                try:
                    dic[KEGGRXN]['ENZYME']+=' '.join(line.split()[1:])
                except:
                    dic[KEGGRXN]['ENZYME']=' '.join(line.split()[1:])
            else:
                try:
                    dic[KEGGRXN]['ENZYME']+=''
                except:
                    dic[KEGGRXN]['ENZYME']=''
            if line.startswith("PATHWAY"):
                try:
                    dic[KEGGRXN]['PATHWAY']+=' '.join(line.split()[1:])
                except:
                    dic[KEGGRXN]['PATHWAY']=' '.join(line.split()[1:])
            else:
                try:
                    dic[KEGGRXN]['PATHWAY']+=''
                except:
                    dic[KEGGRXN]['PATHWAY']=''
            if line.startswith("ORTHOLOGY"):
                try:
                    dic[KEGGRXN]['ORTHOLOGY']+=' '.join(line.split()[1:])
                except:
                    dic[KEGGRXN]['ORTHOLOGY']=' '.join(line.split()[1:])
            else:
                try:
                    dic[KEGGRXN]['ORTHOLOGY']+=''
                except:
                    dic[KEGGRXN]['ORTHOLOGY']=''
        for every in dic:
            cur.execute("INSERT INTO kegg_reactions (KEGGrxn,Name,Named_Reaction,C_Reaction,Enzyme,Pathway,RxnPair,Orthology) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(every,dic[every]['NAMES'],dic[every]['NAMED_REACTION'],dic[every]['C_REACTION'],dic[every]['ENZYME'],dic[every]['PATHWAY'],dic[every]['RPAIR'],dic[every]['ORTHOLOGY']))
        conn.commit()
    except:
        print "Kegg Reactions Table Already exists... Continuing..."   
             
def create_seed_rxn(): #this appears to be terribly slow, likely due to ineffecincy... perhaps a future version can speed this process up, and also handle the reactions with no referenced keggID better.
# One possiblity would be to use SQL language to have it return an error when the foreign key is invalidated, then we could search for the pieces of that reaction to see if just perhaps it is not referenced or not referenced correctly
# try:
    count=1
    num=(re.compile('\([0-9]\)',re.I))
    lett=(re.compile('\[[a-z0-9]\]',re.I))
    cur.execute("CREATE TABLE SEED_reactions (SEED_RXNID varchar PRIMARY KEY, KEGG_RXNID varchar REFERENCES kegg_reactions(keggrxn), Name varchar, Named_Reaction varchar, C_Reaction varchar, Enzyme varchar, SEED_Reaction varchar, Thermodynamics varchar);")
    cur.execute("CREATE TABLE SEED_reactions_nokegg (SEED_RXNID varchar PRIMARY KEY, KEGG_RXNID varchar, Name varchar, Named_Reaction varchar, C_Reaction varchar, Enzyme varchar, SEED_Reaction varchar, Thermodynamics varchar);")
    dic=defaultdict(defaultdict)
    SEEDrxn_file=open("/home/snorris/Ubuntu One/Thesis Project/rxndb/ModelSEED-reactions-db.txt")
    SEEDrxn_file.readline()
    for line in SEEDrxn_file.readlines():
        line=line.split('\t')
        SEEDID=line[0]
        if line[1] is not None:
            dic[SEEDID]['NAME']=line[1]
        else:
            dic[SEEDID]['NAME']='Null'   
        if line[2] is not None:
            dic[SEEDID]['ECNUMBER']=re.sub("\|",' ',line[2]).lstrip()
        else:
            dic[SEEDID]['ECNUMBER']='Null'
        if re.search('R[0-9]',line[3]):
            dic[SEEDID]['KEGGID']=line[3]
        else:
            dic[SEEDID]['KEGGID']=''.join(['unknown',str(count)])
            count+=1
        if line[6] is not None:
            dic[SEEDID]['SEEDEQUATION']=line[6]
        else:
            dic[SEEDID]['SEEDEQUATION']='Null'
        if line[7] is not None:
            dic[SEEDID]['NAMED_EQUATION']=line[7]
        else:
            dic[SEEDID]['NAMED_EQUATION']='Null'
        if line[8] is not None:
            dic[SEEDID]['THERMO']=line[8]
        else:
            dic[SEEDID]['THERMO']='Null'
        compounds=re.sub(num, '',dic[SEEDID]['SEEDEQUATION'])
        compounds=re.sub(lett,'',compounds)
        comps=re.split(" ",compounds)
        for each in comps:
            if re.search('cpd[a-zA-Z0-9]',each):
                cur.execute(("SELECT keggcpd from compounds_master where to_tsvector(seedcpd) @@ to_tsquery('%s') ORDER BY keggcpd;") % each)
                result=re.sub(r'\W+','',str(cur.fetchone()))
                if result != 'None':
                    compounds=compounds.replace(each,result,1)
                else:
                    cur.execute(("SELECT keggcpd from compounds_master where to_tsvector(names) @@ to_tsquery('%s') ORDER BY keggcpd;") % each)
                    result=re.sub(r'\W+','',str(cur.fetchone()))
                    compounds=compounds.replace(each,result,1)
        if compounds is not None:
            dic[SEEDID]['C_EQUATION']=compounds
        else:
            dic[SEEDID]['C_EQUATION']='Null'
    for key in dic:
        if re.search('unknown[0-9]',str(dic[key]['KEGGID'])):
            cur.execute("INSERT INTO SEED_reactions_nokegg (SEED_RXNID,KEGG_RXNID,Name,Named_Reaction,C_Reaction,Enzyme, SEED_Reaction,Thermodynamics) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(str(key),str(dic[key]['KEGGID']),str(dic[key]['NAME']),str(dic[key]['NAMED_EQUATION']),str(dic[key]['C_EQUATION']),str(dic[key]['ECNUMBER']),str(dic[key]['SEEDEQUATION']),str(dic[key]['THERMO'])))
        else:
            cur.execute("select KEGGrxn from kegg_reactions where to_tsvector(KEGGrxn) @@ to_tsquery('%s');" % str(dic[key]['KEGGID']))
            exists=re.sub(r'\W+','',str(cur.fetchone()))
            if exists is not None and re.search('R[0-9]',exists):
                cur.execute("INSERT INTO SEED_reactions (SEED_RXNID,KEGG_RXNID,Name,Named_Reaction,C_Reaction,Enzyme, SEED_Reaction,Thermodynamics) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(str(key),str(dic[key]['KEGGID']),str(dic[key]['NAME']),str(dic[key]['NAMED_EQUATION']),str(dic[key]['C_EQUATION']),str(dic[key]['ECNUMBER']),str(dic[key]['SEEDEQUATION']),str(dic[key]['THERMO'])))
            else:
                cur.execute("INSERT INTO SEED_reactions_nokegg (SEED_RXNID,KEGG_RXNID,Name,Named_Reaction,C_Reaction,Enzyme, SEED_Reaction,Thermodynamics) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(str(key),str(dic[key]['KEGGID']),str(dic[key]['NAME']),str(dic[key]['NAMED_EQUATION']),str(dic[key]['C_EQUATION']),str(dic[key]['ECNUMBER']),str(dic[key]['SEEDEQUATION']),str(dic[key]['THERMO'])))
    conn.commit()
#     except:
#         print "SEED Reaction Table already exists... continuing"

def create_niti_rxn():
    nitifile=open("/home/snorris/Ubuntu One/Thesis Project/rxndb/RxnDb01_24_2013.txt")
    cur.execute("CREATE TABLE NITI_Reactions (NITI_RXN_ID varchar PRIMARY KEY, KEGG_RXN_ID varchar REFERENCES kegg_reactions(keggrxn), Name varchar, Named_Reaction varchar, C_Reaction varchar, Pathway varchar, Enzyme varchar, Thermodynamics varchar);")
    for line in nitifile:
        line=line.split('\t')
        NITI_RXN_ID=line[0]
        NAME=line[1]
        THERMO=line[2]
        PATHWAY=line[3]
        ECNUMBER=line[4]
        NAMED_REACTION=line[5]
        #KEGG_RXN_ID='' QUERY?!?
        compounds=re.sub(lett,'',NAMED_REACTION)
        compounds=re.sub("\:",'',compounds)
        comps=re.split(" ",compounds)
        for each in comps:
            if re.search('[a-zA-Z0-9\_]',each):
                    cur.execute(("SELECT keggcpd from compounds_master where to_tsvector(names) @@ to_tsquery('%s') ORDER BY keggcpd;") % each)
                    result=re.sub(r'\W+','',str(cur.fetchone()))
                    if result is not None:
                        compounds=compounds.replace(each,result,1)
                    else:
                        reader=SBMLReader()
                        document=reader.readSBML('/home/snorris/Downloads/recon2.v02.xml')
                        model=document.getModel()
                        for i in range(0,model.getNumSpecies()):
                            id=(model.getSpecies(i)).getId()
                            name=(model.getSpecies(i)).getName()
                            if re.search(comps,id):
                                compounds=compounds.replace(each,name,1)
                        #do some magical XML reading of RECON?
            C_REACTION=compounds
            print C_REACTION
        
# def create_reactionstxt():
    #continue
# def create_transportrxn():
   # continue
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# cur.execute("SELECT ...; DELETE FROM compounds WHERE keggcpd='';)
# # # # # # # Database connection information # # # # # # # #
try:
    conn = psycopg2.connect("dbname='reactions' user='postgres' host='localhost' password='testing!@3'") # open that database connection  #other user snake password pyth0n! dbname='reactions'
except:
    print "Unable to connect to database"
    quit()
cur = conn.cursor() #set up the psql cursor
# # # # # Call the functions # # # # # # #
def compounds():
    create_cpd_table() #create the initial table and populate it with KEGG IDs
    cur.execute("SELECT * FROM compounds_master;")
    test=cur.fetchall()
    addSEED() #add the seed database data
    addcompoundDB() #add the niti database data#addChEBI() #add the ChEBI database data 
    addChEBI()
# TO DO: Create the reaction tables #
def reactions():
#   create_rxn_table() #create the kegg reactions table
    create_seed_rxn()
#     create_niti_rxn()
#     create_reactionstxt()
#     create_transportrxn()

# Main argument which defines the help and options available to run the script
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hcr",["compounds","reactions"])
    except getopt.GetoptError:
        print 'create_masterdb.py -c to create compound tables and -r to create reactions table'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: create_masterdb.py is a script created to create psql tables \n -c to create compound tables\n -r to create reactions table'
            sys.exit()
        elif opt in ("-c", "--compounds"):
            print "Creating Compound Tables"
            compounds()
        elif opt in ("-r", "--reactions"):
            print "Creating Reactions Tables"
            reactions()

if __name__ == "__main__":
    main(sys.argv[1:])
# cur.execute("SELECT * from compounds_master where keggcpd='C00001';") can be deleted, for testing only.
# print cur.fetchone() # can be deleted, for testing only
conn.commit()
cur.close()
conn.close()