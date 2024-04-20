import openai
import requests
import subprocess
#from openai import OpenAI
import tkinter as tk
from tkinter import scrolledtext, Menu, filedialog, Text, messagebox
import re
from CCparse import parser
from semantics import ASTSimplifier, SemanticAnalyzer



def query_chatgpt(ast):
    openai.api_key = 'Replace with api key'
    prompt = f"Process the following abstract syntax tree produced by ChatCode a newly created programming language " \
             f"You are a Syntax and semantic analyser Scan the ast for syntax and semantic errors then compile and provide the output of the program: {ast} " \
             f"Format your responses appropriately."

    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  # Use an available and supported engine
            prompt=prompt,
            temperature=0.7,
            max_tokens=150,
            n=1,
            stop=None
        )
        return response.choices[0].text.strip()
    except Exception as e:  # Consider using a more general exception if specific ones are not working
        print(f"Error querying ChatGPT: {e}")
        return None



def run_code():
    source_code = code_entry.get("1.0", tk.END)
    ast = parser.parse(source_code)
    simplifier = ASTSimplifier()
    simplified_ast = simplifier.transform(ast)
    analyzer = SemanticAnalyzer()
    analyzer.transform(simplified_ast)
    if analyzer.get_errors():
        error_messages = "\n".join(str(error) for error in analyzer.get_errors())
        output_console.config(state=tk.NORMAL)
        output_console.insert(tk.INSERT, error_messages)
        output_console.config(state=tk.DISABLED)
    else:
        response = query_chatgpt(simplified_ast.pretty())
        output_console.config(state=tk.NORMAL)
        output_console.delete(1.0, "end")
        output_console.insert(tk.INSERT, str(response))
        output_console.config(state=tk.DISABLED)


def highlight_syntax(event=None):
    for tag in ["loop_struct", "contract", "identifier", "data_type", "string"]:
        code_entry.tag_remove(tag, '1.0', tk.END)

    loop_keywords = ['if', 'then', 'else', 'for', 'do', 'while', 'end']
    contract_keywords = ['contract', 'deploy', 'emit', 'event', 'function', 'print']
    modifiers = ['public', 'private', 'return', 'returns']
    data_type_keywords = ['int', 'string', 'bool', 'address', 'var']

    all_keywords = loop_keywords + contract_keywords + modifiers + data_type_keywords
    keyword_pattern = "|".join(r"\b{}\b".format(word) for word in all_keywords)

    for match in re.finditer(keyword_pattern, code_entry.get("1.0", tk.END)):
        start, end = match.span()
        word = match.group(0)

        if word in loop_keywords:
            tag = "loop_struct"
        elif word in contract_keywords:
            tag = "contract"
        elif word in modifiers:
            tag = "identifier"
        elif word in data_type_keywords:
            tag = "data_type"
        code_entry.tag_add(tag, f"1.0+{start}c", f"1.0+{end}c")

    string_pattern = r'\".*?\"'
    for match in re.finditer(string_pattern, code_entry.get("1.0", tk.END), re.S):
        start, end = match.span()
        code_entry.tag_add("string", f"1.0+{start}c", f"1.0+{end}c")

    identifier_pattern = r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'
    for match in re.finditer(identifier_pattern, code_entry.get("1.0", tk.END)):
        start, end = match.span()
        word = match.group(0)
        if word not in all_keywords:
            code_entry.tag_add("identifier", f"1.0+{start}c", f"1.0+{end}c")

    comment_pattern = r'//.*|\#[^\n]*'
    for match in re.finditer(comment_pattern, code_entry.get("1.0", tk.END)):
        start, end = match.span()
        code_entry.tag_add("comment", f"1.0+{start}c", f"1.0+{end}c")
    number_pattern = r'\d+'
    for match in re.finditer(number_pattern, code_entry.get("1.0", tk.END)):
        start, end = match.span()
        code_entry.tag_add("number", f"1.0+{start}c", f"1.0+{end}c")


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("ChatCode File", "*.cc")])
    if file_path:
        with open(file_path, 'r') as file:
            code = file.read()
            code_entry.delete(1.0, "end")
            code_entry.insert("end", code)


def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".cc", filetypes=[("ChatCode File", "*.cc")])
    if file_path:
        code = code_entry.get(1.0, "end")
        with open(file_path, 'w') as file:
            file.write(code)


def show_about():
    messagebox.showinfo("About", "ChatCode\n Version 0.01\n Created By: University of Technology Jamaica")


def show_documentation():
    documentation_path = ''
    try:
        subprocess.run(["open", documentation_path], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def show_example_photo(photo_path):
    try:
        subprocess.run(["open", photo_path], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


root = tk.Tk()
root.title("Chat Code Powered by Open AI")

examples = Menu(root, tearoff=False)
examples.add_command(label="Http Call",command=lambda: show_example_photo("/Users/user/PycharmProjects/APL/venv/Examples/Http Call.png/"))
examples.add_command(label="If Statement", command=lambda: show_example_photo("/Users/user/PycharmProjects/APL/venv/Examples/If Statement.png/"))
examples.add_command(label="For Loop", command=lambda: show_example_photo("/Users/user/PycharmProjects/APL/venv/Examples/For Loop.png.png/"))
examples.add_command(label="Basic Arithmetic", command=lambda: show_example_photo("/Users/user/PycharmProjects/APL/venv/Examples/Basic Arithmetic.png/"))
examples.add_command(label="Contract",command=lambda: show_example_photo("/Users/user/PycharmProjects/APL/venv/Examples/Contract.png/"))

code_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
code_entry.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

code_entry.tag_configure("loop_struct", foreground="blue")
code_entry.tag_configure("contract", foreground="orange")
code_entry.tag_configure("identifier", foreground="dark red")
code_entry.tag_configure("data_type", foreground="purple")
code_entry.tag_configure("string", foreground="green")
code_entry.tag_configure("comment", foreground="grey")
code_entry.tag_configure("number", foreground="light blue")

code_entry.bind("<KeyRelease>", highlight_syntax)

run_button = tk.Button(root, text="Run Code", command=run_code)
run_button.pack(pady=5)

output_console = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=5, state=tk.DISABLED)
output_console.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

menuBar = Menu(root)
root.config(menu=menuBar)

openfile = Menu(menuBar, tearoff=False)
menuBar.add_cascade(label='Open', menu=openfile)
openfile.add_command(label='Select ChatCode File', command=open_file)

savefile = Menu(menuBar, tearoff=True)
menuBar.add_cascade(label='Save', menu=savefile)
savefile.add_command(label='Save as', command=save_file)

helpbutton = Menu(menuBar, tearoff=True)
menuBar.add_cascade(label='Help', menu=helpbutton)
helpbutton.add_command(label='About', command=show_about)
helpbutton.add_command(label='Documentation', command=show_documentation)
helpbutton.add_cascade(label='Examples', menu=examples)

root.mainloop()
