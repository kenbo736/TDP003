# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from data import *

app = Flask(__name__)
db = load('data.json')

@app.route('/')
def home():
    exempel_project = get_project(db, 3)
    #count_project = get_project_count(db)
    #tech_used = get_techniques(db)
    #tech_stats = get_technique_stats(db)
    return render_template('index.html', exempel_project = exempel_project)

@app.route('/list', methods=["GET", "POST"])
def list():
    search_list = search(db, sort_by = 'start_date', sort_order = 'desc')
    technique_list = get_techniques(db)
    if request.method == 'GET':
            return render_template('list.html', project_list = db, search_list = search_list,
                                    technique_list = technique_list)
    else:
        searchfields = request.form.getlist("searchfields")
        if len(searchfields) == 0:
                searchfields = None
        sort_order2=request.form['sort_order']
        search2=request.form['search']
        sort_by2=request.form['sort_by']
        # NY! låter användaren komma åt alla tekniker
        techniques2=request.form.getlist('teknik')
        # NY! Renderar även alla tekniker nu (techniques)
        return render_template('list.html', project_list = search(db, search=search2,
                                sort_order = sort_order2, sort_by = sort_by2, techniques=techniques2, search_fields=searchfields), technique_list = technique_list)

@app.route('/techniques', methods = ["GET", "POST"])
def techniques():
    search_list = search(db, techniques=None)
    techniques = get_techniques(db)
    if request.method == 'GET':
            return render_template('techniques.html', techniques=techniques, technique_list = db,
                                    search_list = search_list)
    else:
        search2=request.form['search']
        return render_template('techniques.html', technique_list=search(db, search =search2))

@app.route('/<technique_id>')
def technique_page(technique_id):
        techniques = get_techniques(db)
        if technique_id in techniques:
                return render_template('techniques.html', techniques = techniques,
                search = search(db, sort_by='start_date', sort_order='desc',
                techniques = [technique_id], search = None, search_fields = None))
        else:
                return render_template('error.html')

@app.route('/project/<project_id>')
def project_page(project_id):
    for p in db:
        if str(p['project_no']) == project_id:
            project = get_project(db, int(project_id))
            return render_template('project.html', project = project)
    return render_template('error.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404

@app.errorhandler(400)
def page_not_found(error):
    return render_template('error.html'), 400

@app.errorhandler(500)
def other(error):
    return render_template('error.html'), 500

if __name__ == "__main__":
    app.port=5000
    app.run(debug=True)
