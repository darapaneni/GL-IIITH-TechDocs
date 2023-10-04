# -*- coding: utf-8 -*-
"""
This app is to correct "Spelling and Grammer" in a given sentence.
 
"""

from gingerit.gingerit import GingerIt

from flask import Flask, request,render_template,redirect

app = Flask(__name__)
 
@app.route("/")
def sent():
    if request.method == "GET":
        return render_template("g.html")
    else:
        
        if not request.form["SENT"]:
            return redirect("/")

        
  
 
@app.route("/sent_correct", methods=["GET","POST"])
def sent_correct():
    if request.method == 'POST':
        text = request.form["SENT"]
        parser = GingerIt()
        print(parser.parse(text)['corrections'])
        result=parser.parse(text)['result']
        return render_template('g.html', output1=result)
        

app.run()
	
