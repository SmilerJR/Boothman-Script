# Copyright 2022 Boothman Script
# Founder N
# New Owners = Josh, Davis
from sys import setrecursionlimit
import re
import json
from os.path import isfile
import py_compile
from time import time, sleep
setrecursionlimit(100)
start = time()
class Lexical_analysis:
    def __init__(self, source):
        self.source = source
        self.pos    = -1
        self.ch     = ""
        self.ident  = ""
        self.integ  = ""
    def consume(self):
        self.pos += 1
        self.ch = self.source[self.pos] if self.pos < len(self.source) else None
    def peek(self):
        if self.pos + 1 < len(self.source): return self.source[self.pos+1]
    def token_stream(self):
        #get first char
        self.consume()
        ################################
        def check():                   #
            if self.ident:             #
                ret = self.ident       #
                self.ident= ""         #
                return ["id", ret]     #
            elif self.integ:           #
                ret = self.integ       #
                self.integ = ""        #
                return ["int", ret]    #
        ################################
        #while EOF not reached
        while self.ch != None:
            # {start skip comments
            if self.ch == "/" and self.peek() == "/":
                while self.ch != "\n":
                    self.consume()
            # }end skip comments

            # {start skip spaces/tabs/newlines
            elif self.ch in " \t\n":
                _ = check()
                if _: yield _
            # }end skip spaces/tabs/newlines

            # {start find operators
            elif self.ch in "-=+*!:;/%&|<>,{}()[]@":
                _ = check()
                if _: yield _
                if self.ch == ":" and self.peek() == ":":
                    yield ["op", "."]
                    self.consume()
                else:
                    yield ["op", self.ch]
            # }end find operators

            # {start find identifiers
            elif re.match("[a-zA-Z_#]", self.ch):
                self.ident += self.ch
            # }end find identifiers

            # {start find integers
            elif re.match("[0-9.]", self.ch):
                self.integ += self.ch
            # }end find integers

            # {start find strings
            elif self.ch == "\"":
                _ = check()
                if _: yield _
                self.consume()
                string = ""
                while self.ch != "\"":
                    string += self.ch
                    self.consume()
                yield ["string", string]
            # }end find strings
            self.consume()
    # {debugging function (print all token_types and values)
    def debug(self):
        print(*list(self.token_stream()), sep="\n")
    # }

class Syntax_analysis(Lexical_analysis):
    def __init__(self, source):
        super().__init__(source)
    def parse_tokens(self):
        final_code = ""
        tokens = list(self.token_stream()) + [["", ""],["",""],["",""],["",""]]
        i = 0
        tabs = 0
        in_stream = False
        while i < len(tokens):
            TType  = tokens[i][0]
            TValue = tokens[i][1]
            if TValue == "fn":
                final_code += f"def {tokens[i+1][1]}"
                i += 1

            elif TValue == "let" or TValue == "typedef":
                pass

            elif TValue in ["u", "i"] and tokens[i+1][1] in ["8","16","32","64"]:
                final_code += "int"
                i += 1

            elif TValue == "else" and tokens[i+1][1] == "if":
                final_code += "elif"
                i += 1

            elif TValue == "true": final_code += "True "

            elif TValue == "false": final_code += "False "

            elif TValue == "drop":
                final_code += "del"

            elif TValue == "struct" or TValue == "namespace": final_code += "class "

            elif TValue == "use" or TValue == "using":
                final_code += f"import {tokens[i+1][1]}"
                i += 1

            elif TValue == "<" and tokens[i+1][1] == "<":
                if in_stream:
                    final_code += "+"
                else:
                    final_code += "("
                    in_stream = True
                i += 1

            elif TValue == ">" and tokens[i+1][1] == ">":
                if in_stream:
                    final_code += "+"
                else:
                    final_code += "("
                    in_stream = True
                i += 1

            elif TValue == "endl":
                final_code += "'\\n'"

            elif TValue == "std" and tokens[i+1][1] == "." and tokens[i+2][1] == "endl":
                final_code += "'\\n'"
                i += 2
            
            elif TValue == "+" and tokens[i+1][1] == "+":
                final_code += "+=1"
                i += 1

            elif TValue == "void" or TValue.lower() == "null":
                final_code += "None"
    
            elif TValue == "#include":
                if isfile("lib/"+tokens[i+1][1]):
                    with open("lib/"+tokens[i+1][1], "r") as f:
                        print("[boothc] include lib/"+tokens[i+1][1])
                        new = Syntax_analysis(f.read())
                        final_code += new.parse_tokens()
                        i += 1
                elif isfile("src/"+tokens[i+1][1]):
                    with open("src/"+tokens[i+1][1], "r") as f:
                        print("[boothc] include src/"+tokens[i+1][1])
                        new = Syntax_analysis(f.read())
                        final_code += new.parse_tokens()
                        i += 1
                else:
                    if isfile("lib/"+tokens[i+1][1]+".booth"):
                        with open("lib/"+tokens[i+1][1]+".booth", "r") as f:
                            print("[boothc] include lib/"+tokens[i+1][1])
                            new = Syntax_analysis(f.read())
                            final_code += new.parse_tokens()
                            i += 1
                    elif isfile("src/"+tokens[i+1][1]+".booth"):
                        with open("src/"+tokens[i+1][1]+".booth", "r") as f:
                            print("[boothc] include src/"+tokens[i+1][1])
                            new = Syntax_analysis(f.read())
                            final_code += new.parse_tokens()
                            i += 1
                    else:
                        input(f"[boothc] stderr: could not find file named {tokens[i+1][1]}")
                        raise FileNotFoundError(f"could not find file named {tokens[i+1][1]}")

            elif TValue == "}" or TValue == "end":
                final_code += "\n"
                tabs -= 1
                for _ in range(tabs):
                    final_code += "    "

                        
            elif TValue == "{" or TValue == "do":
                final_code += ":\n"
                tabs += 1
                for _ in range(tabs):
                    final_code += "    "
                if tokens[i+1][1] == "}" or tokens[i+1][1] == "end":
                    final_code += "pass"

            elif TType == "id" and tokens[i+1][0] in "idintstring" or TType == "id" and tokens[i+1][1] == "!":
                final_code += f"{TValue} "

            elif TValue == ";":
                if in_stream:
                    final_code += ")"
                    in_stream = False
                final_code += "\n"
                for _ in range(tabs):
                    final_code += "    "

            elif TValue == "!" and tokens[i+1][1] != "=":
                final_code += f"not {tokens[i+1][1]}"
                i += 1

            elif TType == "string":
                final_code += repr(TValue)
            else:
                if TValue:
                    final_code += TValue
            i += 1
        return final_code

with open(".booth.config", "r") as f:
    config = json.load(f)
autorun = config["autorun"]
version = config["version"]
print("[boothc] version: "+version+"\n")

with open("src/main.booth", "r") as f:
    x = Syntax_analysis("namespace stndrd {\n    pass\n}\nstd=stndrd();\n"+f.read())
code = x.parse_tokens()+"\nif __name__ == \"__main__\":\n    main()"
print("[boothc] finished Lexical Analysis")
print("[boothc] finished Syntax Analysis")
print("Analyzed in "+str(round(time()-start, 3))+"s")

debug = False

if debug:
    print("Debug output:\n\n")
    print(code) #print code parsed to python
else:
    print("[boothc] DEBUG=false OUT=\"__pycache__/\"")
    import base64
    code  = base64.b64encode(code.encode("ascii")).decode("ascii")
    with open("out.booth.IL", "w+") as f:
        f.write(f"from base64 import b64decode as VhjvberhbvKHV;Jb436jb456jkUuB345='{code}';JHbrejkbLKNERH=exec;JHbrejkbLKNERH(VhjvberhbvKHV(Jb436jb456jkUuB345.encode('ascii')).decode('ascii'));print('\\nprocess finished with exit code 0');input('Press ENTER to return')")
    py_compile.compile("out.booth.IL")
    print("Successfully compiled to __pycache__ folder")
    if not isfile("__pycache__/double click the other file!"):
        with open("__pycache__/double click the other file!", "w") as f:
            pass
    if autorun:
        with open("out.booth.IL", "r") as f:
            print("Running..\n\n")
            exec(f.read())
            exit()
input("Press ENTER to return")
