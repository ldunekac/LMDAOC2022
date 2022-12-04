import re
c=[[int(x)for x in re.split(',|-',l)]for l in open('a').readlines()]
print(sum((x[0]>=x[2]and x[1]<=x[3])or(x[2]>=x[0]and x[3]<=x[1])for x in c),sum((x[0]<=x[2]<=x[1])or(x[2]<=x[0]<=x[3])for x in c))