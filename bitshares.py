import requests
import re
from bs4 import BeautifulSoup as bs
from time import sleep
import urllib
import math

miners=[]
stats=[]
f_w=open("bitshare.txt",'a')

for j in range(97427,100000):
	page='http://185.208.208.184:5000/get_block?block_num='+str(31349459-j)
	page=requests.get(page)
	html = page.text
	i = html.find('"witness":')
	i1 = html.find('"witness_signature"')
	miner=html[i+12:i1-6]
	
	print(j)
	f_w.write(miner+' , ')
	if miner not in miners:
		miners.append(miner)
		stats.append(1)
	else:
		k=miners.index(miner)
		stats[k]=stats[k]+1

		
print(miners)
print (stats)	

stats.sort(reverse=True)
sum_stats=sum(stats)

for i in range(len(stats)):
	stats[i]=float(stats[i])/float(sum_stats)

sum_=0; num_3=0; num_5=0;
for i in range(len(stats)):
	sum_=sum_+stats[i]
    
	if (num_3==0) and (sum_>=0.333333333333333333):
		num_3=i 

	if (num_5==0) and (sum_>=0.5):
		num_5=i
		break

print(num_3,num_5)

entropy_3=0; entropy_5=0; entropy=0;
for i in range(num_3+1):
    entropy_3=entropy_3-stats[i]/(sum(stats[:num_3]))*math.log(stats[i]/sum(stats[:num_3]),2);

for i in range(num_5+1):
    entropy_5=entropy_5-stats[i]/(sum(stats[:num_5]))*math.log(stats[i]/sum(stats[:num_5]),2);
	
for i in range(len(stats)):
    entropy=entropy-stats[i]*math.log(stats[i],2);


A=0; B=0; C=0;
power_5=stats[:num_5]; power_3=stats[:num_3];

for i in range(len(stats)):
    for j in range(len(stats)):
        A=A+abs(stats[i]-stats[j])
        if (i<=num_5) and (j<=num_5):
            B=B+abs(stats[i]-stats[j])

        if (i<=num_3) and (j<=num_3):
            C=C+abs(stats[i]-stats[j])

Gini_100=A/2/len(stats)/sum(stats);
Gini_50=B/2/num_5/sum(stats[:num_5-1]);
Gini_30=C/2/num_3/sum(stats[:num_3-1]);


f_w.write("number="+str(len(stats))+"  gini="+str(Gini_100)+"  entropy="+str(entropy)+ \
"  number="+str(num_5)+"  gini="+str(Gini_50)+"  entropy="+str(entropy_5)+ \
"  number="+str(num_3)+"  gini="+str(Gini_30)+"  entropy="+str(entropy_3)+'\n')

f_w.close()	