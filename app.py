from flask import Flask, render_template, request
from aiml import Kernel
from py2neo import Graph
import os
from nlp_part import NER,autospell,sent_tokenize,analyze_sentiment,get_definition,pos_tag,get_stopwords
from Web_Scraping import scrape_wikipedia

my_bot = Kernel()
app = Flask(__name__)
graph = Graph("bolt://localhost:7687",auth=("neo4j","12345678"))

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        global uemail
        uemail = request.form.get('your_email')
        passw = request.form.get('your_pass')
        print(uemail,passw)
        email=graph.run(f"MATCH(n:USERS{{email: \"{uemail}\", password: \"{passw}\"}}) return n.email")
        print(email)
        emails=list(email)
        print(emails[0][0])
        if uemail == emails[0][0]:
            return render_template("home.html")
    return render_template('login.html')
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('pass')
        re_password = request.form.get('re_pass')
        if password==re_password:
            graph.run(f"MERGE(n:USERS{{name: \"{name}\", email: \"{email}\", password: \"{password}\"}})")
            return render_template("login.html")
    return render_template('signup.html')

        
@app.route("/registartion")
def sign_up():
    return render_template('signup.html')

@app.route('/bot')
def bot():
    return render_template('home.html')

my_bot = Kernel()
def load_aiml_files():
    aiml_directory = "D:\Chat_Bot\data"
    aiml_files = [os.path.join(aiml_directory, file) for file in os.listdir(aiml_directory) if file.endswith(".aiml")]
    for aiml_file in aiml_files:
        my_bot.learn(aiml_file)
load_aiml_files()
def chat_bot(message):
    try:
        response = my_bot.respond(message)
        if response == "unknown":
            print("bot ",response)
            response = None
    except Exception as e:
        print("Error:", e)
        response = None
    return response

@app.route("/get")
def get_bot_response():
    response=''
    query = request.args.get('msg')
    query = autospell(query)
    quries = sent_tokenize(query)
    print(quries)
    for query in quries:
        #response=response+''+analyze_sentiment(query)
        names = NER(query)
    for name in names:
        graph.run(f"merge(n:PERSON{{name: \"{name}\"}})")
        r = chat_bot(query)
        print("bot ",r)
        if r:
            response= response+ " " + r
        else:
            tags_for_wordnet = pos_tag(get_stopwords(query))
            for tag in tags_for_wordnet:
                if tag[1].startswith('N'):
                    wordnet_response = get_definition(tag[0])    
                    if wordnet_response:
                        response = response + '' + wordnet_response
                    else:
                        web_response = scrape_wikipedia(query)
                        if web_response:
                            response = response +''+ web_response
    if response:
        return (str(response))
    else:
        return (str(":)"))


if __name__ == "__main__":
    app.run(debug ="True",host='0.0.0.0', port='5000')
