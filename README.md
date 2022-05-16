# MADE BY N
# ADDED TO GITHUB AND UPDATED BY JOSH
# WITH HELP FROM DAVIS

# Boothman-Script
BoothmanScript is the best programming language ever made
It aims to make you slam your keyboard and shout "ITS WALTER" in rage - styll
This guide will help you learn how to use BoothmanScript and not be bad.


# ABOUT
As previously mentioned, BoothmanScript is the best language ever made.
BoothmanScript is built ontop of python, and "compiles" your code back into python bytecode, which can be executed directly by python.


# GETTING STARTED

# INSTALLATION
To install BoothmanScript, there a few steps you must do.
## INSTALLATION STEPS  
1. Unzip the boothmanscript.zip file to a new folder you will remember

2. double click "boothc.py" to generate the __pycache__ folder.

3. double click src/main.booth and set it to always open in notepad - optional but saves time

BoothmanScript should now be installed.

# RUNNING YOUR FIRST FILE
go into the src folder and add your code to the folder call your file "main

# FIRST STEPS
## THE MAIN FUNCTION
In boothmanscript, the first thing that is executed is the main function
this is where your code will go, and may branch off to call other user-defined functions
To define the main function, you must tell boothmancript it is a function, using the "fn" keyword.
```
fn main() do
   //your code goes here
end
```
// means the rest of the line past the 2 slashes will be a comment, and will be ignored by the compiler

## CREATING VARIABLES 
Sometimes in our program, we may want the computer to remember something that we can use later.
To do this, we can use a variable. Variables are changable things the computer can remember.
Defining a keyword is done by using the "let" keyword, followed by the name, = and a value.
```
let number = 50;
```
If we wanted to reference the value of our number variable, we could just call its name, like so:
```
println(number);
```
This would be the same as typing "println(50);".
Also notice how every line except from "end" and "do" starts with a semicolon.
The semicolon tells the compiler that our line is done and can move onto the next line of code.

## INCLUDING FILES#
Including a file is a useful feature in boothmanscript. It allows to have multiple files in a project that link into one file.
Including a file will copy all of the code in the file sepcified and place it in the file including it.
>"my_file.booth":

```
let my_number = 100;
```
>"main.booth":

```
#include "my_file"; //copies all the code in "my_file.booth"

println(my_number);
```

Files included can also include more files, nestings includes.
Note that files to be included should be placed in the src folder.
Files in the main folder of boothmanscript are still able to be included, but they are usually used for libraries built into the language.

## DATA TYPES
Each variable has a type. The type tells the compiler how to use that variable correctly.
There are 4 main types of data types in boothmancript:
