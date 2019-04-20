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
          "query":{
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
