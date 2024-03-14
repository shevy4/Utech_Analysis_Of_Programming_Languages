University of Technology, Jamaica
Faculty of Engineering and Computing
School of Computing and Information Technology
Analysis of Programming Languages (CIT4004)
Semester 2 – 2023/2024

Design a programming language that interfaces with a large language (LLM) model
like OpenAI’s ChatGPT or Google’s Bard, etc, is deployed on a cloud platform such as
Microsoft’s Azure, etc, and which demonstrates at least 5 characteristics of a good
programming language that you have studied in this class.
This project requires your group to develop a new programming language based on the
principles you have learned in this class. Your group will build a compiler or interpreter for
your language, and your language must feature a natural language interface allowing natural
language input, as well as cloud deployment enabling access to your language over the
internet.
Your language must perform lexical, syntactic and semantic analysis, and must incorporate the
results of the semantic analysis into the core logic of your compiler/interpreter, and allow the
resulting target code to be executed. Your programming language must feature at least five (5)
of the characteristics of a good programming language that you studied in class. The grammar
of your language can be specified in regular CFG, BNF, EBNF, or PEG formats. You are free to
use any development language of your choice, and you may also use compiler development
tools such as LEX/YACC (generates C code), FLEX/BISON (generates C/C++ code), JLEX/CUP
(generates Java code), Jack (generates Java code), PLY (generates Python code), or similar
tools.
You may use OpenAI’s ChatGPT, Google’s Bard or a similar LLM to perform natural language
processing for your language. You may also use Microsoft’s Azure or similar platform to deploy
your language on the cloud. Note that you have free student access to certain elements of the
Microsoft Azure platform once you log in using your UTech credentials

Required
To complete this project successfully, you should:
 Produce a project report containing the components listed below in the grading scheme.
 Develop an executable that performs lexical, syntactic and semantic analysis on input
source code written in your programming language
 Provide users with a natural language interface to your programming language
 Generate executable target code
 Allow your programming language to be accessed and/or deployed on the cloud
 Upload your project report, source code and working application code to the project
assignment space on the course portal
 Make a 7 minute presentation on your project to the class in the allotted tutorial time
At a minimum, the syntax for your programming language must allow programmers to write
source code that assigns values to identifiers, computes arithmetic expressions, performs
conditional branching or conditional execution of statements depending on the value of
identifiers, and displays the value of identifiers.
The semantics for your programming language must include appropriate interpretation of
identifier declarations and assignments, arithmetic expressions, conditional
execution/conditional branching, type checking, and scope rules.
 Language Design: Your group should define a programming language with a clear syntax
and grammar. Your programming language interface should support the following features:
 Allow basic control structures (sequence, selection, iteration)
 Allow use of identifiers, keywords and reserve words
 Allow for scope and binding
 Integration with LLM: Your chosen LLM (i.e. ChatGPT, Bard, etc.) must be integrated into
your project, using the relevant APIs or libraries provided by the LLM to receive lexically,
syntactically and semantically correct text inputs from the LLM
 User-Friendly Interface: Create a user-friendly command-line, mobile, web, graphical or
Text to Speech/Speech to Text interface that allows users to write source code in your
language and execute the target code easily.
 Cloud Deployment: Use Microsoft Azure (or similar platform) to host your
compiler/interpreter and make it securely accessible to users.
 Error Handling: Include error handling, lexical, syntax and semantics validation for user
supplied source code, and interaction with the LLM. Provide informative error messages to
users.
 Documentation: Prepare clear documentation explaining how to use your custom designed
programming language and the interface you created.
APL Group Project Page 2 of 4
 Examples and Tutorials: Include sample code and tutorials to help programmers get started
with writing programs in your programming language.
Bonus Marks
You can provide a secure execution environment for running code, mitigating security
vulnerabilities. You can also extend your programming language with additional features such a
functions, complex data structures, libraries and others
