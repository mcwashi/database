import sys,re
# import psycopg2 # database functions - use to populate and search against the database
#from collections import defaultdict
cpddic={}
cpd_KID=["h2o","hx2coa","3hhcoa"] # Next step is to get these values from the files...
listy=["c00001","c05271","c05268"]
cpd=(re.compile('\[[a-z0-9]\]',re.I))
kid=(re.compile('c\d{5}',re.I))
cpdkid=(re.compile('|'.join(cpd_KID),re.I))
kegeqn=[]
def populatedictionary(): #initialize a dictionary that contains that data we want to work with
    num=int(0)
    for each in cpd_KID:
        cpddic[each]=listy[num]
        num+=1
def readfile(file):
    try:
        reactionsrc=open(file,'r')
    except:
        print "Unable to open reactions file. Please check the path and filename then try again. (ERROR 1)"
        quit()
    for rxn in reactionsrc.readlines():
        line=rxn.strip()
        #if re.search('(?=\w+\[)\w+', line) != None:
        line = re.sub(cpd, '',line)
        for value in cpddic.keys():
            line = (re.sub(value,cpddic.get(value) ,line,re.I))
        line=line.lstrip(': ')
        line=line.replace('<==>','<=>')
        kegeqn.append(line)
    return kegeqn

# line=line[:line2.start()]+line[line2.end():]#try:
#    file=sys.argv[1]
#except:
#    print "Filename no provided. Usage: script.py filename"
#    quit()
source="/home/snorris/Ubuntu One/ThesisProject/reactions"
populatedictionary()
readfile(source)
if set(kegeqn[0])==set(kegeqn[1]):
    print "true"