import random as rd
import string
import datetime

from helpers import insert_data


def now():
    return datetime.datetime.now()


def rand_name():
    first_names = ['Иван', 'Василий', 'Пётр']
    second_names = ['Иванов', 'Петров', 'Сидоров']
    return rd.choice(first_names) + rd.choice(second_names)


def rand_str(length=10):
    letters = string.ascii_lowercase
    return ''.join(rd.choice(letters) for i in range(length))


def rand_uni_name():
    return ' '.join([
        rd.choice(['higher', 'middle', 'elementary']),
        'school of',
        rd.choice(['economics', 'informatics'])
    ])


def rand_bool():
    return rd.choice(['true', 'false'])


def rand_group():
    return rand_str(2) + str(rd.randint(101, 999))


FK_ORGANISATIONS = None
FK_UNIVERSITIES = None
FK_MENTORS = None


def gen_organisations(n_samples=10):
    global FK_ORGANISATIONS
    data = [(5 * i, rand_str(), rd.choice(['corporation', 'university']), rand_bool(), now())
                for i in range(n_samples)]
    FK_ORGANISATIONS = list(set(i[0] for i in data))
    insert_data('Organisations', data)


def gen_universities(n_samples=5):
    global FK_UNIVERSITIES
    data = [(4 * i, rand_uni_name(), now()) for i in range(n_samples)]
    FK_UNIVERSITIES = list(set(i[0] for i in data))


def gen_mentors(n_samples=15):
    global FK_MENTORS
    data = [(rand_str(), rand_str(), rand_name(), rd.choice(FK_ORGANISATIONS), now())
                        for i in range(n_samples)]
    FK_MENTORS = list(set(i[0] for i in data))
    insert_data('Mentors', data)


def gen_students(n_samples=15):
    data = [(rand_str(), rand_str(), rand_name(), rand_group(), rd.choice(FK_UNIVERSITIES), rand_str(), now())
                for i in range(n_samples)]
    insert_data('Students', data)


def gen_projects(n_samples=10):
    data = [(11 * i, rand_str(), rand_str(20), rand_str(20), rd.randint(0, 10),
                            rand_bool(), rand_str(), rd.choice(FK_MENTORS), now())
                for i in range(n_samples)]
    insert_data('Projects', data)


def gen_teams(n_samples=10):
    pass

def gen_team_proj_rel():
    pass

def gen_stud_team_rel():
    pass

def gen_stud_proj_rel():
    pass


def generate_data():
    gen_organisations()
    gen_universities()
    gen_mentors()
    gen_students()
    gen_projects()
    gen_teams()
    gen_team_proj_rel()
    gen_stud_team_rel()
    gen_stud_proj_rel()


if __name__ == '__main__':
    generate_data()
