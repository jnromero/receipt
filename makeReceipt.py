#!/usr/bin/python
from optparse import OptionParser
import sys
import os 
from pythonLatex import MyPyTex
from pythonLatex import latexCompile



parser = OptionParser()

short="-c"
longer="--compile"
destination="compile"
default="n"
info="do you want to automatically compile the document, either y or n"
parser.add_option(short,longer,dest=destination,default=default,help=info)

short="-f"
longer="--file"
destination="file"
default="names.txt"
info="this is the path to the names.txt file, which should just be a txt file with the names on separate lines with a number and a parenthesis in from.  For example, the first line of the txt file should be '1) First Last' and the second line should be '2) First Last'"
parser.add_option(short,longer,dest=destination,default=default,help=info)

short="-o"
longer="--output"
destination="output"
default="receipt.tex"
info="this is the path to the output tex file, or if you just put 'text', it will just output the tex code."
parser.add_option(short,longer,dest=destination,default=default,help=info)

short="-n"
longer="--number"
destination="number"
default="24"
info="total number of subjects on the receipt"
parser.add_option(short,longer,dest=destination,default=default,help=info)

(options, args) = parser.parse_args()



def loadFile(options):
  file = open(options.file,'r')
  fileData=file.read()
  file.close() 
  return fileData


def parseFile(options):
  fileString=loadFile(options)
  names=[]
  for k in fileString.split("\n"):
  	start=k.find(")")
  	names.append(k[start+3:].title())
  names=names+int(options.number)*[""]
  totalSubjects=len(names)

  y=9.5
  delt=min(.4,float(9)/totalSubjects)
  nameString=""
  j=0
  for k in names:
    j=j+1
    nameString=nameString+"\\node at (.75in,%.02fin) {%s};\n"%(y-float(delt)/2,j)
    nameString=nameString+"\\node at (2.5in,%.02fin) {%s};\n"%(y-float(delt)/2,k)
    y=y-delt
    nameString=nameString+"\\draw (.5in,%.02fin) -- (8in,%.02fin);\n"%(y,y)

  bottom=y

  string="""
  \\pagestyle{empty}
  \\begin{tikzpicture}[remember picture,overlay,shift={(current page.south west)}]
      %\\node at (4.25in,10.75in) {\\bf Human Subjects Log};

  \\node [text width=7in] at (4.25in,10.25in) {``I hereby certify that the account is just and correct, that the amount stated was legally \\ due, after allowing all just credits, and the the amount stated has been PAID IN FULL.''};



      \\node at (.75in,9.75in) {\#};
      \\node at (2.5in,9.75in) {Subject};
      \\node at (5.5in,9.75in) {Signature};
      \\node at (7.5in,9.75in) {Payment};
      \\draw (.5in,10in) rectangle (8in,BOTTOMHEREin);
      \\draw (.5in,9.5in) -- (8in,9.5in);
      \\draw (1in,10in) -- (1in,BOTTOMHEREin);
      \\draw (4in,10in) -- (4in,BOTTOMHEREin);
      \\draw (7in,10in) -- (7in,BOTTOMHEREin);

      \\node at (1.5in,10.75in) {{\\bf Investigator:} Julian Romero};
      \\node at (4.5in,10.75in) {{\\bf Experiment:} Repeated Games};
      \\node at (7in,10.75in) {{\\bf Date:} 11/07/2016 (2)};
      \\node at (6.5in,.25in) {{\\bf Total Payment:} \$};
      NAMESHERE

  \\end{tikzpicture}
  """

  string=string.replace("NAMESHERE",nameString)
  string=string.replace("BOTTOMHERE","%.02f"%(bottom))
  return string

def makeTexDocument(option):
  string=parseFile(options)
  if options.output=="text":
    print string
  else:
    doc=MyPyTex.Document()
    doc.body=string
    doc.type='plain'#minimal,plain,picture
    doc.filename=os.path.abspath(options.output)
    doc.update()
    if options.compile=="y":
      doc.compile()
      doc.open() 

makeTexDocument(options)
