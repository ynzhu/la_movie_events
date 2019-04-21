# import pandas as pd
import csv
import codecs

if __name__ == '__main__':
    output_dict = {}
    # title_basics_dict = {}
    with open('title_basics.tsv', 'r', encoding='utf-8-sig') as tsvfile:
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        for row in reader:
            if row['titleType'] in ['movie', 'short']:
                # title_basics_dict[row['tconst']] = [row['primaryTitle'], row['startYear'], row['genres']]
                output_dict[row['tconst']] = [row['primaryTitle'], row['startYear'], row['genres'], [], [], [],
                                              row['tconst'], [], [], []]

    print('stage 1 done.')

    nconst_name_dict = {}
    with open('name_basics.tsv', 'r', encoding='utf-8-sig') as tsvfile:
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        for row in reader:
            nconst_name_dict[row['nconst']] = row['primaryName']

    print('stage 2 done.')

    with open('title_principals.tsv', 'r', encoding='utf-8-sig') as tsvfile:
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        for row in reader:
            if row['tconst'] in output_dict and row['nconst'] in nconst_name_dict:
                if 'director' in row['category']:
                    output_dict[row['tconst']][3].append(nconst_name_dict[row['nconst']])
                    output_dict[row['tconst']][7].append(row['nconst'])
                elif 'writer' in row['category']:
                    output_dict[row['tconst']][4].append(nconst_name_dict[row['nconst']])
                    output_dict[row['tconst']][8].append(row['nconst'])
                elif 'actress' in row['category'] or 'actor' in row['category']:
                    output_dict[row['tconst']][5].append(nconst_name_dict[row['nconst']])
                    output_dict[row['tconst']][9].append(row['nconst'])

    print('stage 3 done.')

    with open('title_ratings.tsv', 'r', encoding='utf-8-sig') as tsvfile:
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        for row in reader:
            if row['tconst'] in output_dict:
                output_dict[row['tconst']].append(row['averageRating'])

    print('stage 4 done.')

    with open('final_outputs.csv', 'w+', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        for key in output_dict:
            for k in range(3, 6):
                output_dict[key][k] = ','.join(output_dict[key][k])
            for k in range(7, 10):
                output_dict[key][k] = ','.join(output_dict[key][k])
            w.writerow(output_dict[key])

    print('all done.')

    # with open('title_crew.tsv') as tsvfile:
    #     reader = csv.DictReader(tsvfile, dialect='excel-tab')
    #     for row in reader:
    #         if row['tconst'] in output_dict:
    #             if 'directors'
