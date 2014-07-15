#!/usr/bin/python
#reactionfixer.py
import psycopg2,re
try:
    conn = psycopg2.connect("dbname='reactions' user='postgres' host='localhost' password='testing!@3'")
except:
    print "didn't work"
    #other user snake password pyth0n! dbname='reactions'
reactions={}
state=(re.compile('\[[a-z0-9]\]',re.I))
cur = conn.cursor()
def SEEDrxns():
   # seedfile=open("/home/snorris/Ubuntu One/Thesis Project/rxndb/ModelSEED-reactions-db.txt",'r')
   # seedfile.readline() #get rid of the header
    seedfile="3hhcoa <==> h2o + hx2coa"
    compounds=re.split(" ",seedfile)
    print compounds
    for each in compounds:
        if re.search('[a-zA-Z0-9]',each):
            cur.execute(("SELECT keggcpd from compounds_master where to_tsvector(Abbreviation) @@ to_tsquery('%s') ORDER BY keggcpd;") % each)
            result=re.sub(r'\W+','',str(cur.fetchone()))
            if result != 'None':
                seedfile=seedfile.replace(each,result)
            else:
                cur.execute(("SELECT keggcpd from compounds_master where to_tsvector(names) @@ to_tsquery('%s') ORDER BY keggcpd;") % each)
                result=re.sub(r'\W+','',str(cur.fetchone()))
                seedfile=seedfile.replace(each,result)
    print seedfile
#     for lines in seedfile:
#         lines=re.split("\t",lines)
#         reactions=re.split(" ",lines[6])
#         SEEDrxnID=line[0]
#         print reactions
#         for compound in reactions:
#             if compound.startswith('cpd'):
#                 compound=re.sub(state,'',compound)
#                 cur.execute(("SELECT keggcpd from seed_compounds where to_tsvector(seedcpd) @@ to_tsquery('%s');") % compound)
#                 reaction[SEEDrxnID]=cur.fetchone()
        
SEEDrxns()
conn.commit()
cur.close()
conn.close()