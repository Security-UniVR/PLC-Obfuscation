import re
import sys
from string import Template

def makeMainTemplate(input_filename):
	output_name="templates/Template_"+input_filename
	out=open(output_name,"w")
	print("sono qui")
	lines = open(input_filename).readlines()
	i=0
	#find the last occurence of END_VAR
	for l in lines:
		i=i+1
		l=l.strip()
		m=re.search("END_VAR",l)
		if m != None:
			line_end_var=i#no break, I need the last occurrence of end_var
		m=re.search("END_PROGRAM",l)
		if m!= None:
			line_end_program=i#here I could use a breakhttp://rdossena.altervista.org/Corso-LaTeX/Corso-LaTeX-Professionisti.pdf
			break
	out.write("\n${AUXILIARIES_EXT_FUNCTIONS}\n");
	for l in lines[0:line_end_var]:
		#l=l.strip()
		out.write(l)
	out.write("\n${NEW_VARIABLES_DECLARATION}\n")

	out.write("\n${NEW_AUXILIARIES_FUNCTIONS}\n")
	for l in lines[line_end_var+1:line_end_program-1]:
		out.write(l) #l.strip())
	out.write("\n${NEW_CONDITIONAL_STATEMENTS}\n")

	for l in lines[line_end_program-1:]:
		out.write(l)#strip non serve se scrivo su file l.strip())
	out.close()

def main():
	input_filename = sys.argv[1]
	makeMainTemplate(input_filename)
if __name__=="__main__":
	main()
