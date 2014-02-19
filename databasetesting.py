import psycopg2
try:
    conn = psycopg2.connect("dbname='reactions' user='postgres' host='localhost' password='testing!@3'")
except:
    print "didn't work"
    #other user snake password pyth0n! dbname='reactions'
cur = conn.cursor()
cur.execute("CREATE TABLE test (id serial PRIMARY KEY, KEGGID varchar, Reaction varchar);")
cur.execute("INSERT INTO test (KEGGID,Reaction) VALUES(%s,%s)", (1,"a + b <=> c"))
cur.execute("SELECT * FROM test;")
print cur.fetchone()
conn.commit()
cur.close()
conn.close()