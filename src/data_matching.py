# import pandas as pd
import csv
import re

if __name__ == '__main__':
    lst = []
    all_movies_dict = {}
    school_movies_dict = {}
    with open('merge_event.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            key = re.sub(r"[^\w:]", "", row[1].strip().lower())
            if len(key) > 0:
                school_movies_dict[key] = row

    with open('outputs.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        all_movies_dict = {key: [] for key in school_movies_dict}
        for row in reader:
            key = re.sub(r"[^\w:]", "", row[0].strip().lower().replace("&", "and"))
            if key in school_movies_dict:
                all_movies_dict[key].append(row)
                






    for movie_key in all_movies_dict:

        if ':' in movie_key and len(all_movies_dict[movie_key]) == 0:
            with open('outputs.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)

                #print("2222222222222")

                for row2 in reader:
                    #print("2222222222222")

                    key = re.sub(r"[^\w:]", "", row2[0].strip().lower().replace("&", "and"))
                    if movie_key.split(':')[1] in key:
                        print(""+movie_key.split(':')[1])
                        print("!!!!!!!!!!!")
                        all_movies_dict[movie_key].append(row2)






        # for row in reader:
        #     key = re.sub(r"[^\w:]", "", row[0].strip().lower().replace("&", "and"))

        #     for movie_key in all_movies_dict:
        #         if ':' in movie_key and movie_key.split(':')[1] in key:
        #             if len(all_movies_dict[movie_key]) == 0:
        #                 all







        # for movie_key in all_movies_dict:
        #     if ':' in movie_key and movie_key.split(':')[1] in key:
        #         all_movies_dict[movie_key].append(row)

    output_dict = {}

    for k in all_movies_dict:
        output_dict[k]=[]
        if all_movies_dict[k]:
            if len(all_movies_dict[k])==1:
                output_dict[k]=all_movies_dict[k][0]
                continue
            rating=-1
            for movie in all_movies_dict[k]:
                if len(movie)<7:
                    continue
                if float(movie[6])>rating:
                    output_dict[k]=movie
                    rating=float(movie[6])
            if not output_dict[k]:
                output_dict[k]=all_movies_dict[k][0]

    for key in all_movies_dict:
        print(key)
        print(all_movies_dict[key])
        print('+++++++')

    print('=======================================')


    for key in output_dict:
        print(key)
        print(output_dict[key])
        print()
        print('------')
    print(len(output_dict))











