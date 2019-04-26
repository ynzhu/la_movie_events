from PyPDF2 import PdfFileReader
import re
from elasticsearch import Elasticsearch

path = "./data/academy_awards.pdf"
es = Elasticsearch()
# path = "/Users/WEI/Documents/INF558/Lectures/1_558-intro(1).pdf"

with open(path, 'rb') as f:
    pdf = PdfFileReader(f)
    content = ""
    years = list(map(lambda x: str(x), list(range(1970,2019))))
    year_movie = {}
    num_of_pages = pdf.getNumPages()
    print(num_of_pages)
    for i in range(num_of_pages):
        page = pdf.getPage(i)
        content += page.extractText()
    for i in range(len(years)):
        if i != len(years)-1:
            index_start = content.find(years[i])
            index_end = content.find(years[i+1])
            year_movie[years[i]] = content[index_start:index_end].split("\n")
        else:
            index_start = content.find(years[i])
            year_movie[years[i]] = content[index_start:].split('\n')
    for year in years:
        filtered_list = list(filter(lambda x: "{" not in x ,year_movie[year]))
        filtered_list_2 = []
        for i in range(len(filtered_list)):
            if "(" in filtered_list[i]:
                category = filtered_list[i].split("(")[0]
            else:
                category = filtered_list[i]
            if bool(re.match(r'[A-Z\s]+$', category)):
                continue
            else:
                if "!--!" in category:
                    filtered_list_2.append(category.split("!--!")[0])
                elif "!" in category:
                    filtered_list_2.append(category.split("!")[0])
                elif "{" in category:
                    continue
                else:
                    filtered_list_2.append(category)
        year_movie[year] = list(set(filter(lambda x: x != "", filtered_list_2)))
    print(year_movie['1979'])
    id_counter = 1
    for year in years:
        for movie in year_movie[year]:
            py_dict = {
                "movie_name" : movie,
                "year": year
            }
            if movie == "Alien":
                print(movie)
            res = es.index(index="oscar", doc_type="movie_year", id=id_counter, body=py_dict)
            id_counter += 1
        