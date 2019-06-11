from sys import *
import importlib

word = ""
com = ""
ag = []
code = []
compiledcode = []
var = []
state = ""
uses = []
funcs = []
word = ""
com = ""
cancontinue = False
def checkfuncs(c):
	for f in funcs:
		if f[0] == c[0]:
			return True
	return False
	
def read(f):		
	global word
	global com
	for c in list(open(f,"r").read()):
	
		if c == "\t":
			pass
		elif c == " " and word == "": 
			pass
		else:
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

read(argv[1])

for c in code:
	if c[0] == "JOIN":
		read(c[1] + ".b")

for c in code:
	if state == "readfunc":
		if c[0] == "ENDPROC":
			state = ""
			funcs.append(list)
		else:
			sublist = []
			n = 0
			for d in c:
				if d != "": sublist.append(d)
			list.append(sublist)
	else:
		if c[0] == "PROC":
			list = []
			list.clear()
			list.append(c[1])
			state = "readfunc"
			
for c in code:	
	if c[0] == "PROC":
		state = "ignorefunc"
		
	if state == "ignorefunc":
		if c[0] == "ENDPROC":
			state = ""
		else: continue
	else:
		for f in funcs:
			if c[0] == f[0]:
				n = 0
				for sf in f:
					list = []
					if n > 0:
						n2 = 0
						for ssf in sf:
							if n2 > 0:
								if ssf[0] == "#" and ssf[1].isdigit():
									list.append(c[int(ssf[1])+1])
								else:
									list.append(ssf)
							else:
								list.append(ssf)
							n2 += 1
						compiledcode.append(list)
					n += 1
		compiledcode.append(c)

		
print(str(compiledcode))
print("")
number = 0
loopn = 0


while True:
	try:
		c = compiledcode[number]
	except IndexError:
		break
	if checkfuncs(c): 
		number += 1
		continue
	if state == "if":
		if c[0] == "ENDIF":
			state = ""
		elif c[0] == "ELSE":
			state = ""
		else:
			number += 1
			continue
	if state == "notif":
		if c[0] == "ELSE":
			state = "if"
	if state == "break":
		number += 1
		if c[0] == "ENDLOOP":
			state = ""
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
		if c[1] == "EQUAL":
			if inp1 != inp2: 
				state = "if"
			else:
				state = "notif"
		if c[1] == "MORE":
			if int(inp1) <= int(inp2): 
				state = "if"
			else:
				state = "notif"
		if c[1] == "LESS":
			if int(inp1) >= int(inp2): 
				state = "if"
			else:
				state = "notif"
	if c[0] == "OP":
		inp2 = ""
		n = 0
		n2 = 0
		if c[2][0] == "#":
			if c[2][1].isdigit(): 
				v = int(i[1])+1
			else:
				v = 1
			for j in var:					
				if j[0] == c[2].replace("#","").replace(str(v-1),""):
					break
				n += 1
				n2 = v
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
		if c[1] == "EQUAL": var[n][n2+1] = inp2
		if c[1] == "ADD": var[n][n2+1] = str(int(var[n][n2+1]) + int(inp2))
		if c[1] == "SUB": var[n][n2+1] = str(int(var[n][n2+1]) - int(inp2))
	if c[0] == "MAKEUSEOF":
		uses.append(importlib.import_module("lib." + c[1]))
	if c[0] == "ENDLOOP":
		loopn = 0
		nu = number - 1
		for i in range(number):
			if compiledcode[nu][0] == "ENDLOOP": loopn += 1
			if compiledcode[nu][0] == "LOOP": loopn -= 1
			if loopn < 0: 
				number = nu - 1
				break
			nu -= 1
	if c[0] == "BREAK":
		state = "break"	
	if c[0] == "DELVAR":
		for v in var:
			if v[0] == c[1]:
				var.remove(v)
	for u in uses:
		u.df(c,var)
	number += 1
		