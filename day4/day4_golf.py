import re
i=[[int(x)for x in re.split(',|-',l)]for l in open('a').readlines()]
print(sum(c<=a and b<=d for a,b,c,d in i),sum(a<=c<=b or c<=a<=d for a,b,c,d in i))