import random as rd
import string
import datetime

from helpers import insert_data


def now():
    return datetime.datetime.now()


def rand_name():
    first_names = ['Иван', 'Василий', 'Пётр']
    second_names = ['Иванов', 'Петров', 'Сидоров']
    return rd.choice(first_names) + ' ' + rd.choice(second_names)


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
#   return rd.choice(['true', 'false'])
    return rd.randint(0, 1)

def rand_group():
    return rand_str(2) + str(rd.randint(101, 999))


def rand_diff_pairs(list_1, list_2, max_n=2):
    ans = []
    for v1 in list_1:
        for v2 in rd.sample(list_2, rd.randint(0, max_n)):
            ans.append((v1, v2))
    return ans


FK_ORGANISATIONS = None
FK_UNIVERSITIES = None
FK_MENTORS = None
FK_STUDENTS = None
FK_PROJECTS = None
FK_TEAMS = None


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
    insert_data('Universities', data)


def gen_mentors(n_samples=15):
    global FK_MENTORS
    data = [(rand_str(), rand_str(), rand_name(), rd.choice(FK_ORGANISATIONS), now())
                        for i in range(n_samples)]
    FK_MENTORS = list(set(i[0] for i in data))
    insert_data('Mentors', data)


def gen_students(n_samples=15):
    global FK_STUDENTS
    data = [(rand_str(), rand_str(), rand_name(), rand_group(), rd.choice(FK_UNIVERSITIES), rand_str(), now())
                for i in range(n_samples)]
    FK_STUDENTS = list(set(i[0] for i in data))
    insert_data('Students', data)


def gen_projects(n_samples=10):
    global FK_PROJECTS
    data = [(11 * i, rand_str(), rand_str(20), rand_str(20), rand_bool(), rand_str(), rd.choice(FK_MENTORS), now())
                for i in range(n_samples)]
    FK_PROJECTS = list(set(i[0] for i in data))
    insert_data('Projects', data)


def gen_teams(n_samples=10):
    global FK_TEAMS
    data = [(8 * i, rand_str(), rd.choice(FK_STUDENTS), now())
                for i in range(n_samples)]
    FK_TEAMS = list(set(i[0] for i in data))
    insert_data('Teams', data)


def gen_team_proj_rel(n_samples=10):
    data = [(team, proj, rand_bool(), now())
                for team, proj in rand_diff_pairs(FK_TEAMS, FK_PROJECTS)]
    insert_data('Team_Project_rel', data)


def gen_stud_team_rel():
    data = [(student, team, rand_bool(), now())
                for student, team in rand_diff_pairs(FK_STUDENTS, FK_TEAMS)]
    insert_data('Student_Team_rel', data)


def gen_stud_proj_rel():
    data = [(student, project, rd.randint(0, 10), rand_bool(), now())
                for student, project in rand_diff_pairs(FK_STUDENTS, FK_PROJECTS)]
    insert_data('Student_Project_rel', data)


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
