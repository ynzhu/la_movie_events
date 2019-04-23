from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from elasticsearch import Elasticsearch

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)
es = Elasticsearch()


class NameForm(FlaskForm):
    location = StringField('Choose a location for events?', validators=[DataRequired()])
    submit = SubmitField('Submit')
class NameForm2(FlaskForm):
    month = StringField('Which month?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    hits = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        body = {
          "query": {
            "bool": {
              "filter": {
                "range": {
                  "FlightDelayMin": {
                    "gte": name
                    }
                }
              }
            }
          }
        }

        result = es.get(index="kibana_sample_data_flights", doc_type="_doc", id="p3bBkmgBOPMEk8-zj4lv")
        res = es.search(index="kibana_sample_data_flights", body=body)

        hits = res['hits']['hits']
        
        form.name.data = ''
    return render_template('index.html', form=form, name=name, hits=hits)

@app.route('/recent', methods=['GET', 'POST'])
def recent_events():
    month = None
    query_body ={}
    res = es.search(index="events_test", body=query_body, size=100)['hits']['hits']
    res.sort(key=lambda x:x['_source']['Date'])
    form = NameForm2()
    if form.validate_on_submit():
        month = form.month.data
        query_body = {
            "query": {
                "match": {
                    "Date": month
                }
            },
        }
        res = es.search(index="events_test", body=query_body, size=50)['hits']['hits']
    res.sort(key=lambda x:x['_source']['Date']) 
    movie_info = {}
    person_id = {}

    for hit in res:
        movie_name = hit['_source']['Movie name']
        query_body_movie = {
            "query":{
                "match": {
                    "primaryTitle": movie_name
                }
            }
        }
        res_movie = es.search(index="matched_imdb", body=query_body_movie, size=1)['hits']['hits']
        movie_info[movie_name] = res_movie
    for key in movie_info:
        for ll in range(len(movie_info[key])):
            movie_info[key][ll]['_source']['directorsName'] = movie_info[key][ll]['_source']['directorsName'].replace('"', '').split(",")
            movie_info[key][ll]['_source']['directorsNconst'] = movie_info[key][ll]['_source']['directorsNconst'].replace('"', '').split(",")
            movie_info[key][ll]['_source']['actorsName'] = movie_info[key][ll]['_source']['actorsName'].replace('"', '').split(",")
            movie_info[key][ll]['_source']['actorsNconst'] = movie_info[key][ll]['_source']['actorsNconst'].replace('"', '').split(",")
            movie_info[key][ll]['_source']['writersName'] = movie_info[key][ll]['_source']['writersName'].replace('"', '').split(",")
            movie_info[key][ll]['_source']['writersNconst'] = movie_info[key][ll]['_source']['writersNconst'].replace('"', '').split(",")
            for i in range(len(movie_info[key][ll]['_source']['directorsNconst'])):
                person_id[movie_info[key][ll]['_source']['directorsName'][i]] = movie_info[key][ll]['_source']['directorsNconst'][i]
            for i in range(len(movie_info[key][ll]['_source']['actorsNconst'])):
                person_id[movie_info[key][ll]['_source']['actorsName'][i]] = movie_info[key][ll]['_source']['actorsNconst'][i]
            for i in range(len(movie_info[key][ll]['_source']['writersNconst'])):
                person_id[movie_info[key][ll]['_source']['writersName'][i]] = movie_info[key][ll]['_source']['writersNconst'][i]
    return render_template('recent.html', form=form, hits = res, movie_info = movie_info, person_id=person_id)

@app.route('/recent/<month>', methods=['GET', 'POST'])
def recent_month_events(month):
    form = NameForm2()
    query_body = {
        "query": {
            "match": {
                "Date": month
            }
        },
    }
    query_body2 = {
        "query": {
            "match": {
                "Date": month
            }
        },
    }

    res = es.search(index="events_test", body=query_body, size=50)['hits']['hits']
    res.sort(key=lambda x:x['_source']['Date'])
    # res = es.search(index="imdb", body=query_body2, size = 100)
    movie_info = {}
    person_id = {}
    for hit in res:
        movie_name = hit['_source']['Movie name']
        query_body_movie = {
            "query":{
                "match": {
                    "primaryTitle": movie_name
                }
            }
        }
        res_movie = es.search(index="matched_imdb", body=query_body_movie, size=1)['hits']['hits']
        movie_info[movie_name] = res_movie
    for key in movie_info:
        for ll in range(len(movie_info[key])):
            movie_info[key][ll]['_source']['directorsName'] = movie_info[key][ll]['_source']['directorsName'].replace('"', '').split(",")
            movie_info[key][ll]['_source']['directorsNconst'] = movie_info[key][ll]['_source']['directorsNconst'].replace('"', '').split(",")
            movie_info[key][ll]['_source']['actorsName'] = movie_info[key][ll]['_source']['actorsName'].replace('"', '').split(",")
            movie_info[key][ll]['_source']['actorsNconst'] = movie_info[key][ll]['_source']['actorsNconst'].replace('"', '').split(",")
            movie_info[key][ll]['_source']['writersName'] = movie_info[key][ll]['_source']['writersName'].replace('"', '').split(",")
            movie_info[key][ll]['_source']['writersNconst'] = movie_info[key][ll]['_source']['writersNconst'].replace('"', '').split(",")
            for i in range(len(movie_info[key][ll]['_source']['directorsNconst'])):
                person_id[movie_info[key][ll]['_source']['directorsName'][i]] = movie_info[key][ll]['_source']['directorsNconst'][i]
            for i in range(len(movie_info[key][ll]['_source']['actorsNconst'])):
                person_id[movie_info[key][ll]['_source']['actorsName'][i]] = movie_info[key][ll]['_source']['actorsNconst'][i]
            for i in range(len(movie_info[key][ll]['_source']['writersNconst'])):
                person_id[movie_info[key][ll]['_source']['writersName'][i]] = movie_info[key][ll]['_source']['writersNconst'][i]
    return render_template('recent.html', form=form, hits = res, month=month, movie_info=movie_info, person_id=person_id)

@app.route('/person/<nconst>', methods=['GET', 'POST'])
def person_page(nconst):
    res = None
    movie_result_list = []
    tconst_movie = {}
    person_id = {}

    query_body = {
        "query": {
            "match": {
                "nconst": nconst
            }
        }
    }


    res = es.search(index="persons",body=query_body,size=1)['hits']['hits']
    tconst_list = res[0]['_source']['knownForTitles'].split(",")
    for tconst in tconst_list:
        query_body_movie = {
            "query": {
                "match": {
                    "tconst": tconst
                }
            }
        }
        res_movie = es.search(index="imdb",body=query_body_movie,size=1)['hits']['hits']
        for ll in range(len(res_movie)):
            res_movie[ll]['_source']['directorsName'] = res_movie[ll]['_source']['directorsName'].replace('"', '').split(",")
            res_movie[ll]['_source']['actorsName'] = res_movie[ll]['_source']['actorsName'].replace('"', '').split(",")
            res_movie[ll]['_source']['writersName'] = res_movie[ll]['_source']['writersName'].replace('"', '').split(",")
            res_movie[ll]['_source']['actorsNconst'] = res_movie[ll]['_source']['actorsNconst'].replace('"', '').split(",")
            res_movie[ll]['_source']['directorsNconst'] = res_movie[ll]['_source']['directorsNconst'].replace('"', '').split(",")
            res_movie[ll]['_source']['writersNconst'] = res_movie[ll]['_source']['writersNconst'].replace('"', '').split(",")
            for i in range(len(res_movie[ll]['_source']['directorsNconst'])):
                person_id[res_movie[ll]['_source']['directorsName'][i]] = res_movie[ll]['_source']['directorsNconst'][i]
            for i in range(len(res_movie[ll]['_source']['actorsNconst'])):
                person_id[res_movie[ll]['_source']['actorsName'][i]] = res_movie[ll]['_source']['actorsNconst'][i]
            for i in range(len(res_movie[ll]['_source']['writersNconst'])):
                person_id[res_movie[ll]['_source']['writersName'][i]] = res_movie[ll]['_source']['writersNconst'][i]
            movie_result_list.append(res_movie[ll])
            tconst_movie[tconst] = res_movie[ll]
    return render_template('person.html', person_info=res, movie_list = movie_result_list, tconst_movie = tconst_movie, person_id = person_id)

@app.route('/location', methods=["GET", "POST"])
def find_location():
    location = None
    hits = None
    movie_info = {}
    person_id ={}
    form = NameForm()
    if form.validate_on_submit():
        location = form.location.data
        body = {
          "query": {
              "match": {
                  "Location": location
              }
          }
        }

        hits = es.search(index="events_test", body=body, size=50)['hits']['hits']
        movie_info = {}
        person_id = {}

        for hit in hits:
            movie_name = hit['_source']['Movie name']
            query_body_movie = {
                "query":{
                    "match": {
                        "primaryTitle": movie_name
                    }
                }
            }
            res_movie = es.search(index="matched_imdb", body=query_body_movie, size=1)['hits']['hits']
            movie_info[movie_name] = res_movie
        for key in movie_info:
            for ll in range(len(movie_info[key])):
                movie_info[key][ll]['_source']['directorsName'] = movie_info[key][ll]['_source']['directorsName'].replace('"', '').split(",")
                movie_info[key][ll]['_source']['directorsNconst'] = movie_info[key][ll]['_source']['directorsNconst'].replace('"', '').split(",")
                movie_info[key][ll]['_source']['actorsName'] = movie_info[key][ll]['_source']['actorsName'].replace('"', '').split(",")
                movie_info[key][ll]['_source']['actorsNconst'] = movie_info[key][ll]['_source']['actorsNconst'].replace('"', '').split(",")
                movie_info[key][ll]['_source']['writersName'] = movie_info[key][ll]['_source']['writersName'].replace('"', '').split(",")
                movie_info[key][ll]['_source']['writersNconst'] = movie_info[key][ll]['_source']['writersNconst'].replace('"', '').split(",")
                for i in range(len(movie_info[key][ll]['_source']['directorsNconst'])):
                    person_id[movie_info[key][ll]['_source']['directorsName'][i]] = movie_info[key][ll]['_source']['directorsNconst'][i]
                for i in range(len(movie_info[key][ll]['_source']['actorsNconst'])):
                    person_id[movie_info[key][ll]['_source']['actorsName'][i]] = movie_info[key][ll]['_source']['actorsNconst'][i]
                for i in range(len(movie_info[key][ll]['_source']['writersNconst'])):
                    person_id[movie_info[key][ll]['_source']['writersName'][i]] = movie_info[key][ll]['_source']['writersNconst'][i]
        form.location.data = ''
    return render_template('index.html', form=form, location=location, hits=hits, movie_info=movie_info, person_id=person_id)