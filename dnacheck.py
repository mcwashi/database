import sys,re
fh = open(sys.argv[1],'r')
nucleotides={'dna':re.compile('^[acgtn]*$',re.I)}

for each in fh.readlines():
    each=each.rstrip()
    each=each.strip(' ')
    print each,
    if nucleotides['dna'].search(each):
        continue
    else:
        newstr=str(each)
        newstr=newstr.replace("A","")
        newstr=newstr.replace("C","")
        newstr=newstr.replace("G","")
        newstr=newstr.replace("T","")
        newstr=newstr.replace("N","")
        print newstr