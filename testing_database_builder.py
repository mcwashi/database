# # keggrxn_file=open("/home/snorris/Ubuntu One/Thesis Project/rxndb/all_rxns")
# # for line in keggrxn_file:
# #     if line.startswith("ENTRY"):
# #         KEGGRXN=line.split()[1]
# #     elif line.startswith("NAME"):
# #         print ' '.join(line.split()[1:])
# #     elif line.startswith("DEFINITION"):
# #         print ' '.join(line.split()[1:])
# #     elif line.startswith("EQUATION"):
# #         print ' '.join(line.split()[1:])
# #     elif line.startswith("ENZYME"):
# #         print ' '.join(line.split()[1:])
# #
# # num=(re.compile('\([0-9]\)',re.I))
# # import re
# # SEEDrxn_file=open("/home/snorris/Ubuntu One/Thesis Project/rxndb/ModelSEED-reactions-db.txt")
# # SEEDrxn_file.readline()
# # for line in SEEDrxn_file.readlines():
# #     line=line.split('\t')
# #     SEEDID=line[0]
# #     NAME=line[1]
# #     ECNUMBER=re.sub("\|",' ',line[2]).lstrip()
# #     KEGGID=line[3]
# #     SEEDEQUATION=line[6]
# #     NAMED_EQUATION=line[7]
# #     THERMO=line[8]
# #     compounds=re.sub(num, '',SEEDEQUATION)
# #     compounds=re.split(" ",SEEDEQUATION)
# #     for each in compounds:
# #         if re.search('[a-zA-Z0-9]',each):
# #             cur.execute(("SELECT keggcpd from compounds_master where to_tsvector(Abbreviation) @@ to_tsquery('%s') ORDER BY keggcpd;") % each)
# #             result=re.sub(r'\W+','',str(cur.fetchone()))
# #             if result != 'None':
# #                 seedfile=seedfile.replace(each,result)
# #             else:
# #                 cur.execute(("SELECT keggcpd from compounds_master where to_tsvector(names) @@ to_tsquery('%s') ORDER BY keggcpd;") % each)
# #                 result=re.sub(r'\W+','',str(cur.fetchone()))
# #                 seedfile=seedfile.replace(each,result)
# #     C_EQUATION=seedfile
# #     print SEEDID,NAME,ECNUMBER,KEGGID,SEEDEQUATION,NAMED_EQUATION,THERMO
import psycopg2,re,sys,getopt
from libsbml import *
from collections import defaultdict
try:
    conn = psycopg2.connect("dbname='reactions' user='postgres' host='localhost' password='testing!@3'") # open that database connection  #other user snake password pyth0n! dbname='reactions'
except:
    print "Unable to connect to database"
    quit()
cur = conn.cursor() #set up the psql cursor
# cur.execute("CREATE TABLE recon_compounds (reconid varchar PRIMARY KEY, keggcpd varchar(6),chebiid varchar,Name varchar, Notes varchar, Annotation varchar);")
# state=(re.compile('\[[a-z0-9]\]',re.I))
# html=re.compile(r'<.*?>|\n')
# htmlanno=re.compile(r'<.*?>|.*rdf:resource=\"|http\:\/\/identifiers.org\/|\"\/\>|\n| |.*chebi\/')
# reader=SBMLReader()
# document=reader.readSBML('/home/snorris/Downloads/recon2.v02.xml')
# model=document.getModel()
# dic=defaultdict(defaultdict)
# for i in range(0,model.getNumSpecies()):
#     id=re.sub('^\w_|_\w$','',(model.getSpecies(i)).getId()) #need to clip out data between M_###_C
#     name=(model.getSpecies(i)).getName()
#     Notes=' '.join(re.sub(html,'',(model.getSpecies(i)).getNotesString()).strip().split('\n'))
#     Annotation=' '.join(re.sub('\/',': ',re.sub(htmlanno,' ',(model.getSpecies(i)).getAnnotationString().strip())).split())
#     if re.findall(r'\bC[0-9]{5}\b',Annotation):
#         KEGGID=''.join(re.findall(r'\bC[0-9]{5}\b',Annotation))
#     elif re.findall(r'\bC[0-9]{5}\b',Notes):
#         KEGGID=''.join(re.findall(r'\bC[0-9]{5}\b',Notes))
#     else:
#         KEGGID=''
#     if re.findall(r'CHEBI:',Annotation):
#         CHEBIID=re.search('(?<=CHEBI:)[0-9]{1,6}',Annotation)
#         CHEBIID=CHEBIID.group()
#     else:
#         CHEBIID=''
#     dic[id]['Name']=name
#     dic[id]['Keggcpd']=KEGGID
#     dic[id]['ChebiID']=CHEBIID
#     dic[id]['Notes']=Notes
#     dic[id]['Annotation']=Annotation
# for each in dic.keys():
#     cur.execute("INSERT into recon_compounds (reconid,name,keggcpd,chebiid,notes,annotation) VALUES(%s,%s,%s,%s,%s,%s)", (each,dic[each]['Name'],dic[each]['Keggcpd'],dic[each]['ChebiID'],dic[each]['Notes'],dic[each]['Annotation']))
  #  print each,dic[each]['Name'],dic[each]['Notes'],dic[each]['Annotation']
  #  chebi=(model.getSpecies(i)).NotesNotInXHTMLNamespace()
  #  searchname=re.sub(' |\(.*\)|\[.*\]|\W','_',name)
#    cur.execute(("SELECT keggcpd from compounds_master where to_tsvector(names||' '||abbreviation) @@ to_tsquery('%s') ORDER BY keggcpd;") % searchname)
#    result=re.sub(r'\W+','',str(cur.fetchone()))
#     if result == None:
#         result=name
#     else:
#         continue
#     cur.execute("UPDATE master_compounds_altered set RECONID='%s',RECON_NAME='%s' where keggcpd='%s';" % (id,name,result))
     #   cur.execute("UPDATE compounds_master SET seedcpd=%s,Names=%s where keggcpd=%s;",(SEEDID,SEEDNAME,SEEDREF[id]))# REFERENCE
     
    print "Creating SEED Reaction Table"
    count=1
    num=(re.compile('\([0-9]\)',re.I))
    lett=(re.compile('\[[a-z0-9]\]',re.I))
    cur.execute("CREATE TABLE SEED_reactions (SEED_RXNID varchar(8) PRIMARY KEY, KEGG_RXNID varchar, Name varchar, Named_Reaction varchar, C_Reaction varchar, Enzyme varchar, SEED_Reaction varchar, Thermodynamics varchar);")
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
        cur.execute("INSERT INTO SEED_reactions (SEED_RXNID,KEGG_RXNID,Name,Named_Reaction,C_Reaction,Enzyme, SEED_Reaction,Thermodynamics) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(str(key),str(dic[key]['KEGGID']),str(dic[key]['NAME']),str(dic[key]['NAMED_EQUATION']),str(dic[key]['C_EQUATION']),str(dic[key]['ECNUMBER']),str(dic[key]['SEEDEQUATION']),str(dic[key]['THERMO'])))
    conn.commit()
cur.close()
conn.close()
#                     #do some magical XML reading of RECON?