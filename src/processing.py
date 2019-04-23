#coding:utf-8
import json
import os
import sys
import csv
from elasticsearch import Elasticsearch

def events_data_clean():
	with open('./data/merge_event.csv','w') as f:
		f.write("Event name , Movie name , Date , Time , Location , Link ")
		f.write("\n")
		#pass

	with open('./data/usc_events.csv','r') as csvfile:
		#time 
		for line in csvfile:
			ls = line.split(",")
			schedule = ls[2].replace(".","").lower()

			date_process = schedule.split(" ")

			date = date_process[0] + "-" + date_process[1] + "-" + date_process[3]

			date = date.capitalize()
			#print(date)
			index1 = schedule.find("pm")
			index2 = schedule.find("am")
			#print(str(index1)+" "+str(index2))

			status = 0
			if index1 > -1 or index2 > -1:
				status = 1
				index3 = schedule.find(":")
				if schedule[index3-2].isdigit():
					time = schedule[index3-2:index3+3]
				else:
					time = schedule[index3-1:index3+3]

				if index1 > -1:
					time = time + "pm"
				if index2 > -1:
					time = time + "am"
			else:
				time = ""
			with open('./data/merge_event.csv','a') as f:
				f.write(ls[0] + "," + ls[1] + "," + date + "," + time + "," + ls[3] + "," + ls[4] + "\n")
		
		#print(list(csvfile))
		#print("\n")
	with open('./data/ucla_events.csv','r') as csvfile:
		for line in csvfile:
			ls = line.split(",")
			schedule = ls[2]
			date_process = schedule.split("-")[0].split(" ")
			date = date_process[0] + "-" + date_process[1] + "-" + date_process[3]
			time = schedule.split("-")[1]
			with open('./data/merge_event.csv','a') as f:
				f.write(ls[0] + "," + ls[1] + "," + date + "," + time + "," + ls[3] + "," + ls[4] + "\n")

def events_merge():
  	pass

def data_match():
  	pass

def post_to_es():
    es = Elasticsearch()
    with open('./data/merge_event.csv','r') as merged:
        merged = list(merged)
        # print(merged)
        headers = merged[0].replace("\n", "").strip().split(",")
        print(headers)
        for line in range(len(merged[1:])):
            if merged[1:][line].strip():
                py_dict = {}
                columns = merged[1:][line].replace("\n", "").strip().split(",")
                for i in range(len(headers)):
                    py_dict[headers[i].strip()] = columns[i].strip()
                # print(py_dict)
                res = es.index(index="events_test", doc_type="events", id=line, body=py_dict)
                print(res)
def post_to_es_person():
    es = Elasticsearch()
    with open('/Users/WEI/Downloads/name.basics.tsv','r') as names:
        names = list(names)
        headers = names[0].replace("\n", "").split("\t")
        names = names[1:]
        for i in range(len(names)):
            py_dict = {}
            columns = names[i].replace("\n", "").split("\t")
            for j in range(len(headers)):
                py_dict[headers[j].strip()] = columns[j].strip()
            res = es.index(index="persons", doc_type="person", id=i, body=py_dict)
            print(res)

def post_to_es_imdb():
    es = Elasticsearch()
    with open('/Users/WEI/Downloads/final_outputs.tsv','r') as names:
        names = list(names)
        headers = ["primaryTitle", "startYear",  "genres", "directorsName", "writersName",
        "actorsName", "tconst", "directorsNconst", "writersNconst", "actorsNconst", "rating"]
        for i in range(len(names)):
            py_dict = {}
            columns = names[i].replace("\n", "").split("\t")
            for j in range(len(headers)):
                py_dict[headers[j].strip()] = columns[j].strip()
            res = es.index(index="imdb", doc_type="imdb_complete", id=i, body=py_dict)
            print(res)

def post_to_es_matched():
    es = Elasticsearch()
    with open('/Users/WEI/Downloads/usc_ucla_imdb_tyk.tsv','r') as names:
        names = list(names)
        headers = ["primaryTitle", "startYear",  "genres", "directorsName", "writersName",
        "actorsName", "tconst", "directorsNconst", "writersNconst", "actorsNconst", "rating"]
        for i in range(len(names)):
            # print(names[i].replace("\n", "").split("\t"))
            # print(len(names[i].replace("\n", "").split("\t")))
            py_dict = {}
            columns = names[i].replace("\n", "").split("\t")
            # print(columns)
            for j in range(len(headers)):
                py_dict[headers[j].strip()] = columns[j].strip()
            res = es.index(index="matched_imdb", doc_type="imdb", id=i, body=py_dict)
            print(res)
if __name__ == "__main__":
    # post_to_es()
    # post_to_es_imdb()
    post_to_es_matched()
