

   def makeReceipt(self,message,client):
      #!/usr/bin/python
      filename=self.currentExperimentPath+'/files/names.txt'
      file = open(filename,'r')
      subjectString=file.read()
      file.close() 

      names=[]
      for k in subjectString.split("\n"):
         start=k.find(")")
         names.append(k[start+3:].title())
      names=names+["",""]
      totalSubjects=len(names)
      print names

      y=9.5
      delt=min(.4,float(9)/totalSubjects)
      nameString=""
      j=0

      sortedSubs=[]
      for sid in self.data['subjectIDs']:
         sortedSubs.append([self.data[sid].desk,sid])
      sortedSubs.sort()
      totalForExperiment=0
      for k in sortedSubs:
         subjectID=k[1]
         j=j+1
         if self.data[subjectID].desk=="default":
            nameString=nameString+"\\node at (.75in,%.02fin) {%s};\n"%(y-float(delt)/2,"")
         else:
            nameString=nameString+"\\node at (.75in,%.02fin) {%s};\n"%(y-float(delt)/2,self.data[subjectID].desk)

         if self.data[subjectID].name=="Not On List" or self.data[subjectID].name=="default":
            nameString=nameString+"\\node at (2.5in,%.02fin) {%s};\n"%(y-float(delt)/2,"")
         else:
            nameString=nameString+"\\node at (2.5in,%.02fin) {%s};\n"%(y-float(delt)/2,self.data[subjectID].name)
         totalPoints=self.data[subjectID].totalPayoffs
         totalPay=int(totalPoints*self.data['exchangeRate']+self.data[subjectID].quizEarnings+self.data[subjectID].bonusPay+5+.99)
         totalForExperiment=totalForExperiment+totalPay
         print "totalForExperiment",totalForExperiment
         nameString=nameString+"\\node at (7.5in,%.02fin) {\$%s};\n"%(y-float(delt)/2,totalPay)
         y=y-delt
         nameString=nameString+"\\draw (.5in,%.02fin) -- (8in,%.02fin);\n"%(y,y)
         # this=[]
         # this.append(subjectID)
         # this.append(self.data[subjectID].connectionStatus)
         # this.append(self.data[subjectID].name)
         # this.append(self.data[subjectID].desk)
         # this.append("%s"%(self.data[subjectID].status['page']))
         # if hasattr(self,'currentPeriods'):
         #    this.append("%s"%(self.currentPeriods[subjectID]))
         # else:
         #    this.append("NA")
         # this.append("%s"%(self.data[subjectID].totalPayoffs))
         # totalPoints=self.data[subjectID].totalPayoffs
         # totalPay=totalPoints*self.data['exchangeRate']+self.data[subjectID].quizEarnings
         # this.append("$5+%.02f+%s=%.02f"%(totalPay,self.data[subjectID].bonusPay,totalPay+self.data[subjectID].bonusPay+5))
      bottom=y

      #nameString=nameString+"\\draw (%.02f,%.02f) rectangle (%.02f,%.02f);"%()

      string="""
      \\pagestyle{empty}
      \\begin{tikzpicture}[remember picture,overlay,shift={(current page.south west)}]
          %\\node at (4.25in,10.75in) {\\bf Human Subjects Log};

      \\node [text width=7in] at (4.25in,10.25in) {``I hereby certify that the account is just and correct, that the amount stated was legally \\ due, after allowing all just credits, and the the amount stated has been PAID IN FULL.''};



          \\node at (.75in,9.75in) {Desk};
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
          \\node at (7in,10.75in) {{\\bf Date:} DATEHERE};
          \\node [yshift=-.25in] at (6.5in,BOTTOMHEREin) {{\\bf Total Payment:} \$TOTALPAYMENTHERE};
          NAMESHERE

      \\end{tikzpicture}
      """

      string=string.replace("NAMESHERE",nameString)
      string=string.replace("BOTTOMHERE","%.02f"%(bottom))
      string=string.replace("TOTALPAYMENTHERE","%s"%(totalForExperiment))
      string=string.replace("DATEHERE",time.strftime("%m/%d/%Y",time.localtime(time.time())))




      doc=MyPyTex.Document()
      doc.body=string
      doc.type='plain'#minimal,plain,picture
      doc.filename=self.currentExperimentPath+'/files/receipt.tex'
      doc.update()
      doc.compile()
      doc.open() 