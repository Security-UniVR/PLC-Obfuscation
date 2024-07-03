#### PLC-Obfuscation
### Memory Obfuscation (by adding) REgisters (MORE)
More is a  Python command line tool for automatic obfuscations of  PLC user programs written in the standard language [ST 61131-3](https://webstore.iec.ch/publication/4552). The supported obfuscations strategies are introduced in (Cozza et al., [2023](https://dl.acm.org/doi/fullHtml/10.1145/3600160.3605081)) and detailed in to_appear.

The tool takes in input the following information: (i) the genuine user program, (ii) the desired obfuscation with eventual parameters, (iii) eventual dependencies between genuine and spurious registers. The tool will  return the obfuscated user program, including (i) declarations of auxiliary functions, (ii) declarations of spurious registers and auxiliary variables, and (iii) the core of the obfuscated  user program  dealing with the introduced spurious registers. 

### Installation
[Python 3.x version](https://www.python.org/downloads/). Standard installation required.

### Usage
``` 
usage: more.py [-h] [-i INPUT] [-o OBFUSCATION] [-r REGISTER] [-t OUTPUT] [-p PERIOD] [-c CONDITION CONDITION]

Tool for automatic obfuscations of PLC user programs written in the standard language ST 61131-3

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        path of the genuine user program
  -o OBFUSCATION, --obfuscation OBFUSCATION
                        clone, conditional, complement, periodic, physical, random
  -r REGISTER, --register REGISTER
                        required if the obfuscation depends upon a register, specify the modbus register name, i.e. QX0.0.
  -t OUTPUT, --output OUTPUT
                        path of the output obfuscated user program
  -p PERIOD, --period PERIOD
                        required for periodic obfuscation, it is the time in number of seconds the register value stays True/False
  -c CONDITION CONDITION, --condition CONDITION CONDITION
                        required for conditional obfuscation, the dependent register name, and the quoted condition, i.e. IW0 ">=40" or in case of OR
                        conditions a list with register names and conditions, i.e. [IW0, ">=40", QX0.0, ""]. For the case of a coil register that can
                        be 1 or 0, the condition is respectively empty string or NOT.
                        The register name can be "this" if the condition refers to the just created register

```

In order to run the obfuscation strategies presented in the papers, given for example an input ST file named plc1.st, the tool must be called as follows.


To add a coil cloning a genuine register, i.e. QX0.0:
``` 
python3 more.py -i plc1.st -o clone -r QX0.0 -t plc1_obf.st
```
To add a coil complementing a genuine register, i.e. QX0.0:
``` 
python3 more.py -i plc1.st -o complement -r QX0.0 -t plc1_obf.st
```
To add a coil that each p seconds switches its value between True and False:
``` 
python3 more.py -i plc1.st -o periodic -p 100 -t plc1_obf.st
```
To add a coil that randomically switches its value between True and False the 10\% of the time when the value of the given register is True:
 ``` 
python3 more.py -i plc1.st -o random  -r QX0.0 -t plc1_obf.st
``` 
This obfuscation can be dependent, if we specify a register as the given value, or independent, thus it will be time dependent, as for periodic obfuscation.

To add the declaration of a spurious input register:
``` 
python3 more.py -i plc1.st -o physical -t plc1_obf.st
```
This obfuscation strategy requires to implement or simulate also a physical system that will send data to the input register.

To add a Coil that depends upon a given spurious or genuine input register, this option can be used for different obfuscations presented in the paper, i.e. for simulate a fake pump that it is True half of the time one other pump is True:
```
python3 more.py -i plc1.st -r IW0 -o conditional -c IW0 ">60" -c  IW0 "<80" -c QX0.0 "" -t out.st
```
or to add the behaviour of a filling pump to a new spurious input register:
```
python3 more.py -i plc1.st -r IW1 -o conditional -c  IW1 "<=35" -c  IW1 [IW1,"<=4",this," "] -t out.st
```
