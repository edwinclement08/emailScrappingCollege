jk = set()

f = open("emails.txt", 'r')
op = open("emails2.txt", 'w')
while 1:
    try:
        line = f.readline()
    except Exception as e:
        pass

    if line not in jk and line:
        print line
        jk.add(line)
        op.write(line )
        op.flush()