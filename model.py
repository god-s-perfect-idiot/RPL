matrix=[]			#translates ajacency matrix file into list in a list
parent={}			#parents dictionary for each node
preparent=""			#preferred parent for a node
bottleneck=[]			#lists all bottlenecks as in marking
root=0				#root node
leaf=[]				#leaf nodes
life={}				#life of each node, accepted as input
path=[]				#list of bottlenecks encountered in the paths of a parent
bots=[]				#life of bottlenecks in path[]
alpha=0				#for transmission, if not set, it runs into busy wait
eltmin=0			#elt_min for preferred parent
eltmax=0			#elt_max for preferred parent

def init():			#fn to initialise all data from i/p file
	global matrix,parent,bottleneck,root,leaf
	mat=open("matrix")
	matr=mat.readline()
	while(matr!=""):
		matr=matr.split()
		matrix.append(matr)
		matr=mat.readline()
	mat.close()
	par=open("parent")
	pare=par.readline()
	while(pare!=""):
		vector=[]
		pare=pare.split()
		k=len(pare)
		for i in range(1,k):
			vector.append(pare[i])
		parent[pare[0]]=vector
		pare=par.readline()
	par.close()
	bot=open("marking")
	bott=bot.readline()
	while(bott!=""):
		bott=bott.split()
		k=len(bott)
		if(bott[0]=="b"):
			for i in range(1,k):
				bottleneck.append(bott[i])
		elif(bott[0]=="r"):
			root=bott[1]
		elif(bott[0]=="l"):
			for i in range(1,k):
				leaf.append(bott[i])
		bott=bot.readline()	
	bot.close()

def setlife():			#read elt of all nodes
	global matrix,life
	k=len(matrix)
	for i in range(1,k+1):
		p=int(input("Life of node "+str(i)+":"))
		life[i]=p		

def objectivefn():		#objective function
	pass

def getlife(a):			#read elt from life[]
	global life
	p=life.get(int(a))
	return p	

def bninpath(a):		#finding all bottlenecks in a parents path to the root
	global parent,preparent,life,path,bots
	s=parent.get(a)
	for j in s:
		if j in bottleneck:
			path.append(j)

def preferredparent(a):		#finding the preferred parent
	global parent,preparent,life,path,bots,eltmin,eltmax
	t=parent.get(a)
	tlen=len(t)	
	for i in t:
		if i in bottleneck:		#if  parent is a bottleneck
			path.append(i)
		if(len(parent.get(str(i)))!=0):	
			bninpath(str(i))
		alpha=1
		while(alpha==0):		#busywait
			pass
		for j in path:			#getlife of all bottlenecks in path
			q=int(getlife(j))
			bots.append(q)
		eltmin=min(bots)
		m=getlife(a)
		eltmin=min(eltmin,m)
		if(eltmin>eltmax):
			eltmax=eltmin
			preparent=i
		path=[]
		bots=[]
	print(preparent)
	eltmin=0
	eltmax=0
	alpha=0

init()
setlife()
for i in range(1,len(matrix)+1):
	if(str(i)!= root and str(i) not in bottleneck):
		preferredparent(str(i))
