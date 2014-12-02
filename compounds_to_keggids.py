#!/usr/bin/env python
# Written By: Shaun Norris - VCU Bioinformatics Graduate Program
# This script is designed to parse a file containing the biochemical reactions occuring in an organism and translate them in to their keggIDs
'''
To Do:
Effciency may be improved by using a dictionary.

'''
### Imports ###
import psycopg2, re, sys

### Constants/Variables ###
rxn_file = open(sys.argv[1],'r')
rxn_lines = rxn_file.readlines()
rxn_file.close()
org_name = str(sys.argv[1].split('.')[0])
print org_name
outfile = open(org_name,'w')
newcpd = None
### Database Connection ###
try: # try to establish a connetion
  conn = psycopg2.connect("user=snorris password=L0v3l1fE dbname=reactions")
  cur = conn.cursor()
except psycopg2.Error, e:
  print "error", e
  sys.exit(1)
  
### Main program ###

for line in rxn_lines:
    line = line.split('\t')
    reactions = line[3]
    if reactions == "Equation":
        continue
    else:
        reactions = reactions.split(' ')
        newreaction = ''
        for index in range(0,len(reactions)):
            if re.search('\[\w\]|\:|\<|\>|\=|\(|\)|\s|\+',reactions[index]):
               newreaction += reactions[index]
            else:
                cur.execute("select keggcpd from kegg_compounds where to_tsvector(names) @@ to_tsquery('%s') ORDER BY keggcpd;" % reactions[index])
                newcpd = re.sub(r'\W','',str(cur.fetchone()))
                #print reactions[index],newcpd
                newreaction += newcpd
                cur.execute("select keggcpd,names,abbreviation from kegg_compounds where to_tsvector(names) @@ to_tsquery('%s') ORDER BY keggcpd;" % reactions[index])
                fullinfo = cur.fetchall()
                print reactions[index],newcpd,fullinfo
    print reactions, newreaction, str(fullinfo)