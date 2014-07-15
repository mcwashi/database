#ADD Glycans
""" Add glycans to the kegg_compounds database, then modify the reactions in kegg_reactions to reflect ONLY C##### values """
import psycopg2,re,sys,getopt
from libsbml import *
from collections import defaultdict
try:
    conn = psycopg2.connect("dbname='reactions' user='postgres' host='localhost' password='testing!@3'") # open that database connection  #other user snake password pyth0n! dbname='reactions'
except:
    print "Unable to connect to database"
    quit()
cur = conn.cursor()
lett=(re.compile('\([a-z0-9]\)',re.I))
# add the glycan IDs
# # print "Creating the Glycan IDs in the kegg_compounds table"
# # glycanfile=open('/home/snorris/Ubuntu One/Thesis Project/Scrapy/tutorial/tutorial/kegg_glycans/results')
# # for line in glycanfile:
# #     line=line.strip().split(':')
# #     glycanid=line[1]
# #     cpdid=line[3]
# #     if len(cpdid) > 7:
# #         multi=cpdid.strip().split(' ')
# #         for each in multi:
# #             if each.startswith('C'):
# #                 print glycanid,each
# #                 cur.execute("UPDATE kegg_compounds SET glycan_id='%s' where to_tsvector(keggcpd) @@ to_tsquery('%s');" % (glycanid,each))
# #                 conn.commit()
# #     else:
# #         print glycanid,cpdid
# #         cur.execute("UPDATE kegg_compounds SET glycan_id='%s' where to_tsvector(keggcpd) @@ to_tsquery('%s');" % (glycanid,cpdid))
# #     conn.commit()
# Create new reactions within the kegg_reactions table
mydic=defaultdict(defaultdict)
cur.execute("SELECT keggrxn,c_reaction FROM kegg_reactions;")
keggrxns=cur.fetchall()
for n in range(0,len(keggrxns)):
    #keggrxns[n][0],keggrxns[n][1]
    mydic[keggrxns[n][0]]['c_reaction']=keggrxns[n][1]
for key in mydic:
    each=mydic[key]['c_reaction']
    every=re.sub('\([0-9a-z]\)|\(.\+.\)|\(.\-.\)','',each)
    pieces=every.split()
    for items in pieces:
#             items=re.sub('\([0-9a-z]|\W|\r\)','',items)
        if re.search('G[0-9]*',items):
            cur.execute("select keggcpd from kegg_compounds where to_tsvector(glycan_id) @@ to_tsquery('%s')" % (items))
            keggid=re.sub(r'\W+','',str(cur.fetchone()))
            every=re.sub(items,keggid,every,count=1)
            keggcpd=every
            cur.execute("update kegg_reactions SET c_reactions2='%s' where to_tsvector(keggrxn) @@ to_tsquery('%s')" % (keggcpd,key))
            conn.commit()
#            print every
