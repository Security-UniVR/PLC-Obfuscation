import re
import sys
from string import Template
import makeTemplate#it provides an ad hoc function for building a template
import argparse
variables={}
#find the first next available unused Coil register
def next_coil():
	"""this functions generates all valid output discrete registers addresses according to Modbus protocol"""
	while True:
		for i in range(100):
			for j in range(8):
				reg = [ "Q", "X", str(int(i)),".",str(int(j))]
				yield ''.join(reg)

gen = next_coil()#generator of coil registers
				
def findNextCoilReg():
	global variables
	new_reg = next(gen)
	while new_reg in variables:
		new_reg = next(gen)
	print("First available coil register ", new_reg)
	return new_reg

#find the first next available unused Input register
def next_input():
	"""this functions generates all valid input registers addresses according to Modbus protocol"""
	while True:
		for i in range(100):#100 si puo' aumentare
				reg = [ "I", "W", str(int(i))]
				yield ''.join(reg)

genIR = next_input()#generator of coil registers

				
def findNextIReg():
	global variables
	new_reg = next(genIR)
	while new_reg in variables:
		new_reg = next(genIR)
	print("First available input register ", new_reg)
	return new_reg

def add_dvariable(register, new_register, reg_type):
	""" 
	this function adds the declaration of a dependent variable.
	input original register location the variable is dipendent by,
	new_register first available register from that type,
	reg_type INT or BOOL
	"""
	global variables
	dich_var = Template('\n${name}_OBF AT %${register}: ${type};\n')
	var_string = dich_var.safe_substitute(name=variables[register], register=new_register, type=reg_type)
	variables[new_register]=variables[register]+"_OBF"
	#print(var_string)
	return var_string

def add_ivariable(new_register, reg_type):
	""" 
	this function adds the declaration of a indipendent variable.
	new_register first available register from that type,
	reg_type INT or BOOL
	"""
	global variables
	name=new_register+"_OBF"
	dich_var = Template('\n${name} AT %${register}: ${type};\n')
	var_string = dich_var.safe_substitute(name=name, register=new_register, type=reg_type)
	variables[new_register]=name
	#print(var_string)
	return var_string

def periodic(new_register, period):	
	""" 
	this function adds the declaration of an independent variable.
	new_register first available register from that type,
	reg_type INT or BOOL
	the value of the added register is based upon the period
	"""
	var_body=Template(open("templates/periodic_snap.st").read());
	new_var=new_register.replace('.','')+"_OBF"
	var_body_string = var_body.safe_substitute(new_reg=new_register, new_var=new_var, period=int(period))

	variables[new_register]=new_var
	print(var_body_string)
	return var_body_string;
	
def random(register, new_register):	
	""" 
	this function adds the declaration of an independent variable.
	new_register first available register from that type,
	reg_type INT or BOOL
	the value of the added register is random
	"""
	var_body=Template(open("templates/random_snap.st").read());
	new_var=new_register.replace('.','')+"_OBF"
	var_body_string = var_body.safe_substitute(dep_register=variables[register],new_reg=new_register, new_var=new_var)

	variables[new_register]=new_var
	print(var_body_string)
	return var_body_string;


def clone(register):	
	body = Template('${name}_OBF := ${name};')
	body_string = body.safe_substitute(name=variables[register])
	return body_string;

def complement(register):
	body = Template('${name}_OBF := NOT(${name});')
	body_string = body.safe_substitute(name=variables[register])
	return body_string;
	
def conditional(register, list_guard, new_reg):
	print("list_guard",list_guard)

	#-c IW1 "<=79" -c  IW1 ("IW1" "<=40" OR this "") coppia che va in OR
	"""r, con=list_guard[0]
	if con=="NOT":
		c="(NOT("+variables[r]+"))"
	else:	
		c="("+variables[r]+con+")"""
	first=True
	c=""
	for r, con in list_guard:
		r=r.replace("this",new_reg)
		con=con.replace("this", new_reg)#a easy way to manage this, TODO it better!

		if not first:
				c+=" AND "

		if con.startswith("["):#TODO perahps the usage of square brackets is not the best, with the ( does not work
			con=con[1:len(con)-1].split(",")
			firstO=True
			c+="("#opening OR block
			for i in range(0,len(con)-1,2):
				if not firstO:
					c+="OR"
				
				rO,cO=con[i],con[i+1]
				print("CO RO",cO)
				c+="("+variables[rO]+cO+")"
				firstO=False
			c+=")"#closing OR parenthesis
		elif con=="NOT":	
			c+="(NOT("+variables[r]+"))"
		else:
			c+=" ("+variables[r]+" "+con+")"
		first=False
	body = Template('${name}_OBF :=  ${guard};')
	body_string = body.safe_substitute(name=variables[register], guard= c)#was =guard)
	return body_string;

def main():
	log_file=open("log.txt","a")
	global variables
	parser = argparse.ArgumentParser(description="Tool for automatic obfuscations of  PLC user programs written in the standard language ST 61131-3")
	parser.add_argument('-i', '--input', help="path of the genuine user program")
	parser.add_argument('-o', '--obfuscation', help="clone, conditional, complement, periodic, physical, random" )
	parser.add_argument('-r', '--register', help="required if the obfuscation depends upon a register, specify the modbus register name, i.e. QX0.0")
	parser.add_argument('-t', '--output', help="path of the output obfuscated user program")
	parser.add_argument('-p', '--period', help ="required for periodic obfuscation, it is the time in number of seconds the register value stays True/False")
	parser.add_argument('-c', '--condition', nargs=2, action='append', help="required for conditional obfuscation, the dependent register name, and the quoted condition, i.e. IW0 \">=40\" or in case of OR conditions a list with register names and conditions, i.e. [IW0, \">=40\", QX0.0, \"\"]. For the case of a coil register that can be 1 or 0, the condition is respectively empty string or NOT")		

	#parser.add_argument('-v', '--verbose',dest='verbose', action='store_true')#for future use
	args = parser.parse_args()

	input_filename=args.input
	obfuscation=args.obfuscation
	register=args.register
	if args.obfuscation =="periodic":# in ["periodic","random"]:
		period=args.period


	conditions=None
	if args.obfuscation =="conditional":
		conditions = parser.parse_args().condition
		for reg,cond in conditions:
   			 print ("---->",reg,cond)
	
	output_filename=args.output

	#for certain obfuscations we have extra arguments

	aux_ext_functions=''#this is needed for example for random obfuscation
	var_string=''
	aux_functions=''
	statements=''
	#build variables that is a dictionary with register and corresponding variable name:
	for l in  open(input_filename):
		l=l.strip()
		l=l.replace(' ','')
		m=re.search("(.*)AT\%(.{3,5}):",l)
		if m != None:
			variable_name=m.group(1)
			tmp_register=m.group(2)
			if tmp_register not in variables:
				variables[tmp_register] = variable_name 		
	print(variables)

	new_reg=findNextCoilReg();#find the first next available unused Coil register
	#print(new_reg)

	if obfuscation=="physical":
		new_input_reg=findNextIReg()
		var_string=add_ivariable(new_input_reg, "INT")
		print(var_string)
		
	
	elif obfuscation=="clone":
		print("Making a clone of ",register,"containing ",variables[register])
		var_string=add_dvariable(register, new_reg,"BOOL");	
		statements=clone(register)
		print("var_string: ", var_string)
		print("statement: ", statements)
	
	elif obfuscation=="complement":
		print("Making a complement of ",register,"containing ",variables[register])
		var_string=add_dvariable(register, new_reg,"BOOL");
		statements=complement(register)	
	elif obfuscation=="conditional":
		
		var_string=add_dvariable(register, new_reg,"BOOL");	
		statements=conditional(register, conditions,new_reg) #conditions is a couple register condition, all must be in AND
		print("var_string: ", var_string)
		print("statement: ", statements)

	
	elif obfuscation=="periodic":
		print("Making a new register ",new_reg," that changes periodically")
		aux_functions=periodic(new_reg,period)

	elif obfuscation =="random":
		print("Making a new register ",new_reg," that changes randomly")
		aux_functions=random(register,new_reg)#, period)
		aux_ext_functions=open("templates/random_f_snap.st").read()
	else:
		print("No valid obfuscation choosen")

	log_file.write(new_reg+"\n")
	log_file.close()
	makeTemplate.makeMainTemplate(input_filename)
	
	source_code =Template(open("templates/Template_"+input_filename).read())#source_code along with parts thare are placeholders to be filled in
	out=open(output_filename,'w+')
	print(aux_ext_functions)
	if var_string!='':
		var_string="VAR\n"+var_string+"\nEND_VAR"
	var_string=var_string
	source_code_obf = source_code.safe_substitute(	AUXILIARIES_EXT_FUNCTIONS=aux_ext_functions,		NEW_VARIABLES_DECLARATION	=var_string, NEW_AUXILIARIES_FUNCTIONS=aux_functions,NEW_CONDITIONAL_STATEMENTS=statements)

		
		
	out.write(source_code_obf)
	print(variables)
	
if __name__=="__main__":
	main()



