from sys import *

word = ""
com = ""
ag = []
code = []
var = []
state = ""

for c in list(open(argv[1],"r").read()):
	word += c	
		
	
	if com != "":
		if c == ";":
			ag.append(word.replace(";",""))
			word = ""	
		if c == "\n":
			cline = []
			cline.append(com.replace("\n",""))
			for c in ag:
				cline.append(c)
			code.append(cline)
			ag.clear()
			com = ""
	else:	
		if c == " ":
			com = word.replace(" ","")
			word = ""

	if word == "END":
		break
		

for c in code:
	if state == "if":
		if c[0] == "ENDIF":
			state = ""
		else:
			continue
	if c[0] == "PRINT":
		n = 0
		st = ""
		for i in c:
			if n != 0:
				if i[0] == "#":
					if i[1].isdigit(): 
						v = int(i[1])+1
					else:
						v = 1
					for j in var:					
						if j[0] == i.replace("#","").replace(str(v-1),""):
							st += str(j[v])
				else:
					st += i
			n += 1
		print(st)
	if c[0] == "VAR":
		list = []
		n = 0
		for i in c:
			if n != 0:
				list.append(i)
			n += 1
		if c[2] == "#READ":
			inp = input(c[3])
			var.append([c[1],inp])
		else:
			var.append(list)
	if c[0] == "IF":
		if c[1] == "EQUAL":
			inp1 = ""
			inp2 = ""
			if c[2][0] == "#":
				if c[2][1].isdigit(): 
					v = int(i[1])+1
				else:
					v = 1
				for j in var:					
					if j[0] == c[2].replace("#","").replace(str(v-1),""):
						inp1 = j[v]
			else:
				inp1 = c[2]
			if c[3][0] == "#":
				if c[3][1].isdigit(): 
					v = int(i[1])+1
				else:
					v = 1
				for j in var:					
					if j[0] == c[3].replace("#","").replace(str(v-1),""):
						inp2 = j[v]
			else:
				inp2 = c[3]				
			if inp1 != inp2:
				state = "if"
			
	if c[0] == "END":
		break
		
