import json
from collections import Counter
import pprint

pp = pprint.PrettyPrinter(indent=2)

def get_host_report(shows):
    male_hosted_shows = [show for show in shows if show['host_gender'] == 'm']
    female_hosted_shows = [show for show in shows if show['host_gender'] == 'f']
    print(f'Vseh oddaj: {len(shows)}')
    print(f'Moških voditeljev: {len(male_hosted_shows)}')
    print(f'Ženskih voditeljic: {len(female_hosted_shows)}')

def get_intro_report(shows):
    all_mentions = sum([show['intro']['mentions']['total'] for show in shows])
    all_male_mentions = sum([show['intro']['mentions']['male'] for show in shows])
    all_female_mentions = sum([show['intro']['mentions']['female'] for show in shows])

    average_mentions = all_mentions / len(shows)
    average_male_mentions = all_male_mentions / len(shows)
    average_female_mentions = all_female_mentions / len(shows)

    print(f'Povprečno št. omenjenih v introju: {average_mentions} (vseh: {all_mentions})')
    print(f'Povprečno št. omenjenih moških v introju: {average_male_mentions} (vseh: {all_male_mentions})')
    print(f'Povprečno št. omenjenih žensk v introju: {average_female_mentions} (vseh: {all_female_mentions})')

def get_guest_report(shows):
    number_of_all_guests = sum(show['number_of_guests'] for show in shows)
    number_of_male_guests = sum([len([guest for guest in show['guests'] if guest['gender'] == 'm']) for show in shows])
    number_of_female_guests = sum([len([guest for guest in show['guests'] if guest['gender'] == 'f']) for show in shows])

    average_guests = number_of_all_guests / len(shows)
    average_male_guests = number_of_male_guests / len(shows)
    average_female_guests = number_of_female_guests / len(shows)

    location_counter = Counter()

    for show in shows:
        for guest in show['guests']:
            location_counter[guest['location']] += 1

    print(f'Povprečno št. gostov: {average_guests} (vseh: {number_of_all_guests})')
    print(f'Povprečno št. moških gostov: {average_male_guests} (vseh: {number_of_male_guests})')
    print(f'Povprečno št. ženskih gostov: {average_female_guests} (vseh: {number_of_female_guests})')
    print(f'Lokacije:')
    for location in location_counter.most_common(5):
        print(f'{location[0]}: {location[1]}')

def get_report_report(shows):
    number_of_all_reports = sum(show['number_of_reports'] for show in shows)
    number_of_male_authors = sum([len([report for report in show['reports'] if report['author_gender'] == 'm']) for show in shows])
    number_of_female_authors = sum([len([report for report in show['reports'] if report['author_gender'] == 'f']) for show in shows])

    average_reports = number_of_all_reports / len(shows)
    average_male_authors = number_of_male_authors / len(shows)
    average_female_authors = number_of_female_authors / len(shows)

    print(f'Povprečno število poročil: {average_reports} (vseh: {number_of_all_reports})')
    print(f'Povprečno moških avtorjev: {average_male_authors} (vseh: {number_of_male_authors})')
    print(f'Povprečno ženskih avtoric: {average_female_authors} (vseh: {number_of_female_authors})')


# - ali moški bolj prekinjajo goste ali ženske (ali je kaka razlika v spolu gosta)
#   - sum[(število prekinitev / število vprašanj) for guest in guests]/len(guests)
#   - kakšna je verjetnost, da te bo voditelj pri naslednjem vprašanju prekinil
#     glede na to, kakega spola je voditelj in kakega spola si ti
def get_interruptions_report(shows):
    male_hosted_shows = [show for show in shows if show['host_gender'] == 'm']
    female_hosted_shows = [show for show in shows if show['host_gender'] == 'f']

    interruptions = {
        'total': {
            'm': 0,
            'f': 0,
        },
        'avg': {
            'm': 0,
            'f': 0,
        },
        'male_hosts': {
            'total': {
                'm': 0,
                'f': 0,
            },
            'avg': {
                'm': 0,
                'f': 0,
            },
        },
        'female_hosts': {
            'total': {
                'm': 0,
                'f': 0,
            },
            'avg': {
                'm': 0,
                'f': 0,
            },
        },
    }

    # total interruptions
    interruptions['total']['m'] = sum([sum([guest['interruptions'] for guest in show['guests']]) for show in male_hosted_shows])
    interruptions['total']['f'] = sum([sum([guest['interruptions'] for guest in show['guests']]) for show in female_hosted_shows])

    interruptions['male_hosts']['total']['m'] = sum([sum([guest['interruptions'] for guest in show['guests'] if guest['gender'] == 'm']) for show in male_hosted_shows])
    interruptions['male_hosts']['total']['f'] = sum([sum([guest['interruptions'] for guest in show['guests'] if guest['gender'] == 'm']) for show in female_hosted_shows])

    interruptions['female_hosts']['total']['m'] = sum([sum([guest['interruptions'] for guest in show['guests'] if guest['gender'] == 'f']) for show in male_hosted_shows])
    interruptions['female_hosts']['total']['f'] = sum([sum([guest['interruptions'] for guest in show['guests'] if guest['gender'] == 'f']) for show in female_hosted_shows])

    # interruptions per guest
    interruptions['avg']['m'] = sum([sum([guest['interruptions'] for guest in show['guests']]) / len(show['guests']) for show in male_hosted_shows]) / len(male_hosted_shows)
    interruptions['avg']['f'] = sum([sum([guest['interruptions'] for guest in show['guests']]) / len(show['guests']) for show in female_hosted_shows]) / len(female_hosted_shows)

    interruptions['male_hosts']['avg']['m'] = sum([sum([guest['interruptions'] for guest in show['guests'] if guest['gender'] == 'm']) / len(show['guests']) for show in male_hosted_shows]) / len(male_hosted_shows)
    interruptions['male_hosts']['avg']['f'] = sum([sum([guest['interruptions'] for guest in show['guests'] if guest['gender'] == 'm']) / len(show['guests']) for show in female_hosted_shows]) / len(female_hosted_shows)

    interruptions['female_hosts']['avg']['m'] = sum([sum([guest['interruptions'] for guest in show['guests'] if guest['gender'] == 'f']) / len(show['guests']) for show in male_hosted_shows]) / len(male_hosted_shows)
    interruptions['female_hosts']['avg']['f'] = sum([sum([guest['interruptions'] for guest in show['guests'] if guest['gender'] == 'f']) / len(show['guests']) for show in female_hosted_shows]) / len(female_hosted_shows)

    print('INTERRUPTIONS')
    pp.pprint(interruptions)


def get_questions_report(shows):
    male_hosted_shows = [show for show in shows if show['host_gender'] == 'm']
    female_hosted_shows = [show for show in shows if show['host_gender'] == 'f']

    questions = {
        'total': {
            'm': 0,
            'f': 0,
        },
        'pm': {
            'm': 0,
            'f': 0,
        },
        'male_hosts': {
            'total': {
                'm': 0,
                'f': 0,
            },
            'pm': {
                'm': 0,
                'f': 0,
            },
        },
        'female_hosts': {
            'total': {
                'm': 0,
                'f': 0,
            },
            'pm': {
                'm': 0,
                'f': 0,
            },
        },
    }

    # total questions
    questions['total']['m'] = sum(
        [
            sum(
                [guest['questions'] for guest in show['guests']]
            ) for show in male_hosted_shows
        ]
    )
    questions['total']['f'] = sum(
        [
            sum(
                [guest['questions'] for guest in show['guests']]
            ) for show in female_hosted_shows
        ]
    )

    questions['male_hosts']['total']['m'] = sum(
        [
            sum(
                [guest['questions'] for guest in show['guests'] if guest['gender'] == 'm']
            ) for show in male_hosted_shows
        ]
    )
    questions['male_hosts']['total']['f'] = sum(
        [
            sum(
                [guest['questions'] for guest in show['guests'] if guest['gender'] == 'm']
            ) for show in female_hosted_shows
        ]
    )

    questions['female_hosts']['total']['m'] = sum(
        [
            sum(
                [guest['questions'] for guest in show['guests'] if guest['gender'] == 'f']
            ) for show in male_hosted_shows
        ]
    )
    questions['female_hosts']['total']['f'] = sum(
        [
            sum(
                [guest['questions'] for guest in show['guests'] if guest['gender'] == 'f']
            ) for show in female_hosted_shows
        ]
    )

    # interruptions per guest
    questions['pm']['m'] = sum(
        [
            sum(
                [guest['questions'] for guest in show['guests']]
            ) / (sum(
                [guest['seconds'] for guest in show['guests']]
            ) / 60) for show in male_hosted_shows
        ]
    ) / len(male_hosted_shows)
    questions['pm']['f'] = sum(
        [
            sum(
                [guest['questions'] for guest in show['guests']]
            ) / (sum(
                [guest['seconds'] for guest in show['guests']]
            ) / 60) for show in female_hosted_shows
        ]
    ) / len(female_hosted_shows)

    # MALE HOSTS
    print('MALE HOSTS')
    male_hosts_questions_m = [sum([guest['questions'] for guest in show['guests'] if guest['gender'] == 'm' and int(guest['questions']) != 0]) for show in male_hosted_shows if len(show['guests']) > 0]
    male_hosts_seconds_m = [sum([guest['seconds'] for guest in show['guests'] if guest['gender'] == 'm' and int(guest['seconds']) != 0]) for show in male_hosted_shows if len(show['guests']) > 0]
    male_hosts_qpm_m = []

    for i, number_of_questions in enumerate(male_hosts_questions_m):
        if number_of_questions > 0 and male_hosts_seconds_m[i] > 0:
            male_hosts_qpm_m.append(number_of_questions / (male_hosts_seconds_m[i] / 60))
    print('TIPI PREKINJAJO TIPE: ', sum(male_hosts_qpm_m) / len(male_hosts_qpm_m))

    male_hosts_questions_f = [sum([guest['questions'] for guest in show['guests'] if guest['gender'] == 'f' and int(guest['questions']) != 0]) for show in male_hosted_shows if len(show['guests']) > 0]
    male_hosts_seconds_f = [sum([guest['seconds'] for guest in show['guests'] if guest['gender'] == 'f' and int(guest['seconds']) != 0]) for show in male_hosted_shows if len(show['guests']) > 0]
    male_hosts_qpm_f = []

    for i, number_of_questions in enumerate(male_hosts_questions_f):
        if number_of_questions > 0 and male_hosts_seconds_f[i] > 0:
            male_hosts_qpm_f.append(number_of_questions / (male_hosts_seconds_f[i] / 60))
    print('TIPI PREKINJAJO BABE: ', sum(male_hosts_qpm_f) / len(male_hosts_qpm_f))

    print('FEMALE HOSTS')
    female_hosts_questions_m = [sum([guest['questions'] for guest in show['guests'] if guest['gender'] == 'm' and int(guest['questions']) != 0]) for show in female_hosted_shows if len(show['guests']) > 0]
    female_hosts_seconds_m = [sum([guest['seconds'] for guest in show['guests'] if guest['gender'] == 'm' and int(guest['seconds']) != 0]) for show in female_hosted_shows if len(show['guests']) > 0]
    female_hosts_qpm_m = []

    for i, number_of_questions in enumerate(female_hosts_questions_m):
        if number_of_questions > 0 and female_hosts_seconds_m[i] > 0:
            female_hosts_qpm_m.append(number_of_questions / (female_hosts_seconds_m[i] / 60))
    print('BABE PREKINJAJO TIPE: ', sum(female_hosts_qpm_m) / len(female_hosts_qpm_m))

    female_hosts_questions_f = [sum([guest['questions'] for guest in show['guests'] if guest['gender'] == 'f' and int(guest['questions']) != 0]) for show in female_hosted_shows if len(show['guests']) > 0]
    female_hosts_seconds_f = [sum([guest['seconds'] for guest in show['guests'] if guest['gender'] == 'f' and int(guest['seconds']) != 0]) for show in female_hosted_shows if len(show['guests']) > 0]
    female_hosts_qpm_f = []

    for i, number_of_questions in enumerate(female_hosts_questions_f):
        if number_of_questions > 0 and female_hosts_seconds_f[i] > 0:
            female_hosts_qpm_f.append(number_of_questions / (female_hosts_seconds_f[i] / 60))
    print('BABE PREKINJAJO BABE: ', sum(female_hosts_qpm_f) / len(female_hosts_qpm_f))

    pp.pprint(questions)

with open ('data.json', 'r') as infile:
    shows = json.load(infile)
    # shows = [show for show in shows if show['host_gender'] == 'm']
    get_host_report(shows)
    print()
    get_intro_report(shows)
    print()
    get_guest_report(shows)
    print()
    get_report_report(shows)
    print()
    get_interruptions_report(shows)
    print()
    get_questions_report(shows)
