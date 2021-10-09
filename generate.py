import csv
import json
from datetime import datetime

def get_gender(gender):
    if gender == 'moški':
        return 'm'
    return 'f'

def get_int_property(row, prop):
    if row[prop] == '':
        return 0
    return int(row[prop].split('.')[0])

def get_int_properties(row, prefix='', postfix='', has_both=False):
    male = int(row[f'{prefix}_male_{postfix}'].split('.')[0])
    female = int(row[f'{prefix}_female_{postfix}'].split('.')[0])
    both = int(row[f'{prefix}_both_{postfix}'].split('.')[0]) if has_both else 0
    total = male + female + both
    output = {
        'male': male,
        'female': female,
        'total': total
    }
    if has_both:
        output['both'] = both
    return output

def get_seconds_from_time(row_id, time):
    try:
        return int(time.split(':')[0]) * 60 + int(time.split(':')[1])
    except:
        print(f'ERROR IN ROW {row_id}!!!')
        return -1

def get_guest_data(row_id, row, guest_number):
    number_of_questions = int(row[f'g{guest_number}_questions']) if row[f'g{guest_number}_questions'] != '' else -1
    number_of_interruptions = int(row[f'g{guest_number}_interruptions']) if row[f'g{guest_number}_interruptions'] != '' else -1
    return {
        'guest_number': guest_number,
        'gender': get_gender(row[f'g{guest_number}_gender']),
        'location': row[f'g{guest_number}_location'].strip(),
        'topic': row[f'g{guest_number}_topic'],
        'seconds': get_seconds_from_time(row_id, row[f'g{guest_number}_time']),
        'role': row[f'g{guest_number}_role'],
        'number_of_questions': number_of_questions,
        'number_of_interruptions': number_of_interruptions
    }   

def get_report_data(row, report_number):
    return {
        'author_gender': get_gender(row[f'r{report_number}_author']),
        'guests': get_int_property(row, f'r{report_number}_guests'),
        'guests_women': get_int_property(row, f'r{report_number}_guests_women'),
        'guests_men':  get_int_property(row, f'r{report_number}_guests') - get_int_property(row, f'r{report_number}_guests_women'),
        'randos': get_int_property(row, f'r{report_number}_randos'),
        'randos_women': get_int_property(row, f'r{report_number}_randos_women'),
        'randos_men': get_int_property(row, f'r{report_number}_randos') - get_int_property(row, f'r{report_number}_randos_women'),
        'topic': row[f'r{report_number}_topic']
    }

shows = []


with open('odmevi.csv', 'r') as infile:
    reader = csv.DictReader(infile)
    for i, row in enumerate(reader):
        show = {
            'row': i + 2,
            'date': datetime.strptime(row['date'], '%m/%d/%Y').strftime('%Y-%m-%d'),
            'host_gender': get_gender(row['host_gender']),
            'intro': {
                'mentions': get_int_properties(row, 'intro', 'mentions'),
                'stars': get_int_properties(row, 'intro', 'stars', has_both=True)
            },
            'number_of_guests': get_int_property(row, 'number_of_guests'),
            'guests': [get_guest_data(i + 2, row, i) for i in range(1, get_int_property(row, 'number_of_guests') + 1)],
            'number_of_reports': get_int_property(row, 'number_of_reports'),
            'reports': [get_report_data(row, i) for i in range(1, get_int_property(row, 'number_of_reports') + 1)]
        }
        shows.append(show)

with open('data.json', 'w') as outfile:
    json.dump(shows, outfile)

# Export to neo
from neo4j import GraphDatabase

neo4j_driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'banana'))

def save_show(tx, show):
    result = tx.run('''
            MERGE (s:Show {row: $row})
            SET s.date = $date
            SET s.host_gender = $host_gender
            SET s.number_of_guests = $number_of_guests
            SET s.number_of_reports = $number_of_reports
            SET s.intro_female_mentions = $intro_female_mentions
            SET s.intro_male_mentions = $intro_male_mentions
            SET s.intro_female_stars = $intro_female_stars
            SET s.intro_male_stars = $intro_male_stars
            SET s.intro_both_stars = $intro_both_stars
        ''',
        row=show['row'],
        date=show['date'],
        host_gender=show['host_gender'],
        number_of_guests=show['number_of_guests'],
        number_of_reports=show['number_of_reports'],
        intro_female_mentions=show['intro']['mentions']['female'],
        intro_male_mentions=show['intro']['mentions']['male'],
        intro_female_stars=show['intro']['stars']['female'],
        intro_male_stars=show['intro']['stars']['male'],
        intro_both_stars=show['intro']['stars']['both'],
    )
    return result.single()

def save_and_connect_guest(tx, show, guest):
    result = tx.run('''
        MERGE (g:Guest {guest_id: $guest_id})
        SET g.gender = $gender
        SET g.location = $location
        SET g.topic = $topic
        SET g.seconds = $seconds
        SET g.role = $role
        SET g.number_of_questions = $number_of_questions
        SET g.number_of_interruptions = $number_of_interruptions

        WITH g
        MATCH (s:Show {row: $row})
        MERGE (s)-[:HOSTS]->(g)
        ''',
        guest_id=f'{show["row"]}_{guest["guest_number"]}',
        row=show['row'],
        gender=guest['gender'],
        location=guest['location'],
        topic=guest['topic'],
        seconds=guest['seconds'],
        role=guest['role'],
        number_of_questions=guest['number_of_questions'],
        number_of_interruptions=guest['number_of_interruptions']
    )
    return result.single()

def save_and_connect_report(tx, show, report):
    result = tx.run('''
        MERGE (r:Report {report_id: $report_id})
        SET r.author_gender = $author_gender
        SET r.number_of_guests = $number_of_guests
        SET r.number_of_female_guests = $number_of_female_guests
        SET r.number_of_male_guests = $number_of_male_guests
        SET r.number_of_randos = $number_of_randos
        SET r.number_of_female_randos = $number_of_female_randos
        SET r.number_of_male_randos = $number_of_male_randos
        SET r.topic = $topic

        WITH r
        MATCH (s:Show {row: $row})
        MERGE (s)-[:CONTAINS]->(r)
        ''',
        report_id=f'{show["row"]}_{report["number"]}',
        row=show['row'],
        author_gender=report['author_gender'],
        number_of_guests=report['guests'],
        number_of_female_guests=report['guests_women'],
        number_of_male_guests=report['guests_men'],
        number_of_randos=report['randos'],
        number_of_female_randos=report['randos_women'],
        number_of_male_randos=report['randos_men'],
        topic=report['topic']
    )

    return result.single()

with neo4j_driver.session() as session:
    for show in shows:
        # save show
        session.write_transaction(save_show, show)
        for guest in show['guests']:
            session.write_transaction(save_and_connect_guest, show, guest)
        for i, report in enumerate(show['reports']):
            report['number'] = i
            session.write_transaction(save_and_connect_report, show, report)


# TODO
# - koliko vprašanj boš dobil glede na to katerega spola si ti/voditelj na minuto pogovora

# - katere teme so bile najbolj featurane v tem času
#   - koliko časa je dobila tema
#   - koliko gostov je govorilo o neki temi
#   - koliko minut je na katero temo govoril kateri spol

# - ali tvoj spol napoveduje tvojo lokacijo?

# - ali spol voditelja napoveduje spole v introju
