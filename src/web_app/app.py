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
    name = StringField('Choose a range of the flight?', validators=[DataRequired()])
    time = StringField('Choose a time for event?',  validators=[DataRequired()])
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

        # time_query = {
        #     "query":{
        #         "match_all": {}
        #     },
        #     "sort":[
        #         {
        #             "event_time": "asc" 
        #         }
        #     ],
        # }

        # name_query = {
        #     "query":{
        #         "match":{
        #             "movie_name":name
        #         }
        #     }
        # }

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
    return render_template('recent.html', form=form, hits = res)

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
    res = es.search(index="events_test", body=query_body, size=50)['hits']['hits']
    res.sort(key=lambda x:x['_source']['Date'])
    return render_template('recent.html', form=form, hits = res, month=month)
