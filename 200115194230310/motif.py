from Bio import SeqIO
from Bio import ExPASy
import requests

from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import Radiobutton
from tkinter import *
from tkinter.ttk import *
import re

window = Tk()
progress=Progressbar(window,orient=HORIZONTAL,length=500,mode='determinate')
window.title("Motif Detection Tool")
example = """>sp|P05067|A4_HUMAN Amyloid-beta A4 protein OS=Homo sapiens OX=9606 GN=APP PE=1 SV=3
MLPGLALLLLAAWTARALEVPTDGNAGLLAEPQIAMFCGRLNMHMNVQNGKWDSDPSGTK
TCIDTKEGILQYCQEVYPELQITNVVEANQPVTIQNWCKRGRKQCKTHPHFVIPYRCLVG
EFVSDALLVPDKCKFLHQERMDVCETHLHWHTVAKETCSEKSTNLHDYGMLLPCGIDKFR
GVEFVCCPLAEESDNVDSADAEEDDSDVWWGGADTDYADGSEDKVVEVAEEEEVAEVEEE
EADDDEDDEDGDEVEEEAEEPYEEATERTTSIATTTTTTTESVEEVVREVCSEQAETGPC
RAMISRWYFDVTEGKCAPFFYGGCGGNRNNFDTEEYCMAVCGSAMSQSLLKTTQEPLARD
PVKLPTTAASTPDAVDKYLETPGDENEHAHFQKAKERLEAKHRERMSQVMREWEEAERQA
KNLPKADKKAVIQHFQEKVESLEQEAANERQQLVETHMARVEAMLNDRRRLALENYITAL
QAVPPRPRHVFNMLKKYVRAEQKDRQHTLKHFEHVRMVDPKKAAQIRSQVMTHLRVIYER
MNQSLSLLYNVPAVAEEIQDEVDELLQKEQNYSDDVLANMISEPRISYGNDALMPSLTET
KTTVELLPVNGEFSLDDLQPWHSFGADSVPANTENEVEPVDARPAADRGLTTRPGSGLTN
IKTEEISEVKMDAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVVIATVIVITL
VMLKKKQYTSIHHGVVEVDAAVTPEERHLSKMQQNGYENPTYKFFEQMQN"""

def run(): ##Method ran when search button is clicked
 progress['value']=0
 content = Stxt.get('1.0', 'end-1c') ##Retriieving text from the scrolledText box

 def is_fasta(filename): ##method to parse FASTA to file returns true is input is Correct Fasta
   with open(filename, "r") as handle:
     progress['value']=10
     fasta = SeqIO.parse(handle, "fasta") ##Parcing fasta using BioPython
     progress['value']=20
     return any(fasta) ##Returning Fasta

 uniprotCheck = False

 if var.get() == 3:
  uniprotCheck = True

 proteins = []
 batch = []
 Ubatch = []
 error = []

 protein = content
 outfile = open("test2.txt","w")
 outfile.write(protein)
 outfile.close()
 isFasta = is_fasta("test2.txt")
 batch = protein.split(">")
 del batch[0]

 def checkFormat(): ##Method to check the format of all the uniprot acession codes 1 by 1
  count = 0
  errors = ""
  for f in Ubatch: ##For each uniprot code
   if bool(re.findall(r"[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}", f)): #Regex to check if the format matches a uniprot accession code
    count+=1 ##If matches counter + 1
   else:
    error.append(Ubatch.index(f)) ##If the format doesnt match add the acesson code number to the error array
    errors = ''.join(str(e) for e in error) ##Convert the error array to string to display in dialog box
 if count != len(Ubatch): ##If one or more code doesnt match the correct format
  messagebox.showinfo("Help", "Error with Accession code(s): " + errors) ##Display the message box with the specific number of the acession code
  return False
 else:
  return True

 if protein == "": ##Checking if input is empty
  messagebox.showinfo("Help", "Please enter a fasta or accession number") ##Displaying Message
 elif (is_fasta("test2.txt") is True): ##Using is_fasta to check input is valid Fasta
  " ".join(protein.split())
  protein.replace(" ", "") ##Removing Spaces for future RegEx
  progress['value']=30 ##Setting Progress bar value
 elif bool(re.findall(r"[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}", protein)): ##if the input isnt fasta, checking if the input is a uniProt Acession code
  CorrectFormat = True
  Ubatch = protein.split(" ") ##Splitting the input in the case of batch processing by " "
  progress['value']=30
 else:
  messagebox.showinfo("Help", "Incorrect Format - See help page") ##If input isnt FASTA or Acession code, dispay incorrect format message
  progress['value']=0

 outfile = open("test2.txt","w")
 outfile.seek(0)
 outfile.truncate() ##Cleaning file
 outfile.close() ##Closing File
 def fastaMatch():
  counter = 0
  for f in batch:
   if bool(re.search(r"[^P][^PKRHW]{2}[VLSWFNQ]{3}[ILTYWFN]{4}[FIY]{5}[^PKRH]{6}", f)):
    counter+=1
 if counter == 0:
   return False
 else: return True

if uniprotCheck == True and checkFormat() == True: ##If acession code button has been checked and if all the values(whole batch) have the correct format
   for x in Ubatch: ##For each value in the batch
     fullURL = "https://www.uniprot.org/uniprot/" + x + ".fasta" ##Creating a uniProt URL using the acession code
     result = requests.get(fullURL) ##Retrieving results from the URL
     progress['value']=30
     if result.ok: ##If result is valid continue
      progress['value']=70
      text = result.text
      text.replace(" ", "") ##Removing Spaces for searching using RegEx
      " ".join(text.split())
      batch.append(text) ##Appending to list
     else:
      messagebox.showinfo("Help", "Error! Check internet connection or see help guide!") ##If results fail display error message

number = 0
def printOut(fasta): ##Method for displaying Results
   number = 0
   progress['value']=80
   if fastaMatch(fasta) == True: ##Checking for a match in each individual sequence
    for m in re.finditer(r"(?=([^P][^PKRHW]{2}[VLSWFNQ]{3}[ILTYWFN]{4}[FIY]{5}[^PKRH]{6}))", fasta): ##for each match in the fasta, regex search using lookahead asertion
     number+= 1
     if number > 1: ##if printing the second results add a space
      output.insert(INSERT,'\n')
     pt = fasta[:m.start(1)] ##splitting the start of the sequence for printing later
     pt2 = fasta[m.end(1):] ##splitting the end of the sequence for printing later
     red = "red" ##Setting Colour for printing later
     green = "green" ##Setting Colour for printing later
     print(m.group(1))
     output.tag_configure(red, foreground=red) ##setting color for tag
     output.tag_configure(green, foreground=green)

     output.insert(INSERT,"Motif Number: ", number) ##Printing motif number for each protein in case of multiple per sequence
     output.insert(INSERT, number)
     output.insert(INSERT,'\n')
     output.insert(INSERT,"Start Position: ")
     output.insert(INSERT, m.start(1) + 1) ##displaying/Inserting the position of the start of the motif + 1 to account for indexing

     output.insert(INSERT,'\n')
     output.insert(INSERT,"End Position: ")
     output.insert(INSERT, m.end(1) + 1) ##Displaying the end postion of the motif + 1 to account for the index at 0
     output.insert(INSERT,'\n')
     output.insert(INSERT, "Motif: ")
     output.insert(INSERT, m.group(1)) ##Displaying the full motif seperate from the sequence
     output.insert(INSERT,'\n')
     output.insert(INSERT,"Full sequence: ")

     output.insert(INSERT, pt, ("green")) ##inseting the start of the sequence upto the start of the motif in green
     output.insert(INSERT, m.group(1),("red")) ##inserting the motif in red
     output.insert(INSERT, pt2,("green")) ##inseting the end of the motif in green to produce the full colour coded sequence
     output.insert(INSERT,'\n')
     progress['value']=100
   else:
     output.insert(INSERT, "No Match found!") ##If no match for the specific seqence is found display no match found
     output.insert(INSERT,'\n')

var = 0
for x in batch: ##Looping through all sequences
  if fastaMatch(x) == True: ##If any matches are found in one of the sequences
   var+=1 ##Counter variable + 1

  if var != 0: ##If any matches are found
     newwin = Toplevel(window) ##Create new display window
     display = Label(newwin, text="Results:")
     display.pack()
     output = scrolledtext.ScrolledText(newwin,width=89,height=30) ##Creating a scrolledText region for output results
     output.pack()
     proteinCount = 0
     progress['value']=40

     for f in batch: ##for each sequence
      proteinCount+= 1
      if proteinCount > 1:
         output.insert(INSERT, '\n')
         output.insert(INSERT, "Sequence Number: ") ##Insert sequence number for multiple sequence in one batch
         output.insert(INSERT, proteinCount)
         output.insert(INSERT, '\n')
         printOut(f) ##Calling print out function to display the results for sequence "f"

     else:
       messagebox.showinfo("Help", "No Match Found") ##If no matches are found in any of the sequence display no match found box
       progress['value']=0

############GUI#############

image = PhotoImage(file="logo6.png")
label = Label(image=image, borderwidth=0)
label.grid(column=0, row=0, padx=0, pady=10)

lbl = Label(window, text="Input Protein Sequence or UniProt Acession code below:", font = ('ariel',13,'bold'))
lbl.configure(background = 'white')
lbl.grid(column=0, row=1, padx=0, pady=10)

def sel(): ##Method to check if the UniProt Acession code button is toggled.
 if var.get() == 1:
  checkBatch = True
 else: checkBatch = False

var = IntVar()

R3 = Radiobutton(window, text="Acession Code", variable=var, value=3,command=sel)

R3.grid(column=0, row=4, padx=0, pady=5)

Stxt = scrolledtext.ScrolledText(window,width=89,height=10)
Stxt.grid(column=0, row=5,padx=10, pady=10)

global click
click = 1

def clear_entry(event, Stxt): ##method to delete the placeholder_text when user clicks in input box
 global click
 if click == 1: ##Checking if its first click
  Stxt.delete(1.0, END)
  click+=1

placeholder_text = 'Input one or more protein sequences to search by inputing FASTA format or by clicking the "Acession Code" button and inputting UniProt Acession codes! Then click search seqeuence. '
Stxt.insert(INSERT, placeholder_text)

Stxt.bind("<Button-1>", lambda event: clear_entry(event, Stxt))

def clickExample(): ##Method to insert example FASTA when the button is clicked
 Stxt.delete(1.0, END) ##Clears the input box of placeholder_text
 Stxt.insert(INSERT, example) ##Inserts example

def help1():
 messagebox.showinfo("Help", "'Input one or more protein sequences to search by inputing FASTA format or by clicking the Acession Code button and inputing UniProt Acession codes! Then click search seqeuence. - See help guide at www.motifdetectiontool.com/help")

help=PhotoImage(file="icon2.png")

B1 = Button(window,width=3, text = "?", command = help1)
B1.grid(column=1, row=1,padx=0, pady=10)
B1.config(image=help)

btn = Button(window,width=93,text="Search sequence", command=run)
btn.grid(column=0, row=6,padx=0, pady=10)

btnExample = Button(window,width=93,text="Load Example Search", command=clickExample)
btnExample.grid(column=0, row=7,padx=0, pady=3)
progress.grid(column=0, row=8,pady=50)

window.geometry('800x580')
window.configure(background = 'white')
window.resizable(width=FALSE, height=FALSE)

window.mainloop()