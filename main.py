#!/usr/bin/env python3
import os

from flask import Flask, render_template, request, jsonify
import requests
import json
import datetime



def create_app(config=None):
    app = Flask(__name__)
    
    @app.route('/search', methods=['POST']) 
    def search_type():
        #Get Timestamp today and now
        time_stamp = str(datetime.datetime.now())

        #text input
        search_input = request.form['search_input']

        #Search Type (Language/Topic)
        search_type = request.form['search_type']

        url = requests.get('https://api.github.com/search/repositories?q='+search_type+ ':'+search_input)

        data = json.loads(url.content)

        if 'errors' in data:
            return jsonify(data['errors']),400

        items_list = data['items']

        display_data = []
        report_result = []

        for item in items_list:
            display_data.append(
            {
                'url': item['html_url'],
                'name': item['name']
            })

            report_result.append(item['name'])

        generate_report(search_input,search_type,time_stamp,report_result)

        return render_template('search_result.html', data=display_data)
        
    @app.route("/")
    def index():
        return render_template('index.html')


    return app

def generate_report(search_input, search_type, time_stamp, report_result):
        
    with open("Admin_Report.txt","ab") as myfile:

        myfile.write(('Timestamp    : ' +time_stamp+ '\n').encode())
        myfile.write(('Search Input : ' +search_input+ '\n').encode())
        myfile.write(('Search Type  : ' +search_type+ '\n').encode())
        myfile.write(('Results      : ' +str(report_result)+ '\n').encode())
        myfile.write(('\n').encode())

        myfile.close()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="127.0.0.1", port=port)
