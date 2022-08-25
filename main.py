import json
import os
import pickle
from datetime import datetime
import pandas as pd
import pymysql
from pymysql.cursors import DictCursor
from contextlib import closing
from classes import SerpJSON, Profile, ExportFields
import clipboard

skills_ids_dtb_name = 'skill_ids.dtb'
SERP_dtb = 'serp_dtb'
SERP_table = 'serp'
profiles_table = 'profiles'
sibl = 'pars'



def main():
    skill_ids_database = {}
    profiles_list = []
    # <<<< Checking clipboard for valid json >>>>
    prev_cb = None
    clipboard.copy('')
    while clipboard.paste().lower() != ' ':
        cb = clipboard.paste()
        if cb != prev_cb:
            js = validate_clipboard(cb)
            if js:
                dt = datetime.now()
                s_json = SerpJSON(js, dt)
                print(vars(s_json))
                # <<<< Add skills ids and names to dtb >>>>
                skill_ids_database = process_skill_ids(s_json, skill_ids_database)
                # <<<< Get relative skill names >>>>
                skill_names = []
                for skill_id in s_json.upwork_relat_skill_ids.split(','):
                    try:
                        skill_names.append(skill_ids_database['skills'][skill_id]['name'].lower())
                    except:
                        skill_names.append(skill_id)
                s_json.upwork_relative_skill_names = ','.join(skill_names)
                print(f'JSON Valid::   Keyword:"{s_json.q}",   Page:"{s_json.page}",   Relatice Skills:"{s_json.upwork_relative_skill_names}",   Date:{s_json.date},   Time:{s_json.time}')
                print('----------------------------------------------------------------------------------------------------------------------------------------------')
                create_database_if_not_exist(SERP_dtb)

                sql = f"""
                    ################################## SERP
                    CREATE TABLE IF NOT EXISTS {SERP_table} (
                    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
                    timestamp TIMESTAMP,
                    json JSON,
                    page TINYINT UNSIGNED NOT NULL,
                    q VARCHAR(255),
                    upwork_relat_skill_ids VARCHAR(255),
                    relative_skill_names VARCHAR(255),
                    PRIMARY KEY (id),
                    INDEX timestamp_idx (timestamp),
                    INDEX json_idx (json),
                    INDEX upwork_relat_skill_ids_idx (upwork_relat_skill_ids),
                    INDEX relative_skill_names_idx (relative_skill_names),
                    INDEX q_idx (q))
                    ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=1 ;
                    """
                create_table_if_not_exist(SERP_dtb, sql)
                insert_SERP(SERP_dtb, SERP_table, s_json)
                for prof in s_json.json['results']['profiles']:
                    profile = Profile(prof, s_json.q, s_json.page, s_json.timestamp)
                    skill_ids = profile.skills_ids.split(',')
                    skill_names = []
                    for skill_id in skill_ids:
                        skill_name = skill_ids_database['skills'][skill_id]['name']
                        skill_names.append(skill_name)
                    profile.skills_names = ','.join(skill_names)
                    profiles_list.append(profile)


        prev_cb = cb
    for profile in profiles_list:
        profile.export_fields = ExportFields(profile, sibl, profiles_list)
        print()
        sql = f"""
            ################################## SERP
            CREATE TABLE IF NOT EXISTS {profiles_table} (
            id INT UNSIGNED NOT NULL AUTO_INCREMENT,
            uid VARCHAR(255),
            ciphertext VARCHAR(255),
            shortName VARCHAR(255),
            timestamp TIMESTAMP,
            page TINYINT UNSIGNED NOT NULL,
            keyword VARCHAR(255),
            description_words_count TINYINT,
            sibl_in_description TINYINT,
            sibl_to_words_count_descr TINYINT,
            title_words_count TINYINT,
            sibl_in_title TINYINT,
            sibl_to_words_count_title TINYINT,
            PRIMARY KEY (id))
            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=1 ;
            """
        create_table_if_not_exist(SERP_dtb, sql)
        keys = ', '.join(list(vars(profile.export_fields).keys()))
        values = ', '.join( [add_quotes(x) for x in (vars(profile.export_fields).values())])

        insert_profile(SERP_dtb, profiles_table, keys, values)

def add_quotes(s):
    return '"'+str(s)+'"'

def process_skill_ids(s_json, db):
    if is_file_exist(skills_ids_dtb_name):
        db = read_dict(skills_ids_dtb_name)
    else:
        db = {'checked_profiles': [], 'skills': {}}

    profiles = s_json.json['results']['profiles']
    for p in profiles:
        skills = p['skills']
        uid = p['uid']
        if uid not in db['checked_profiles']:
            db['checked_profiles'].append(uid)
            for s in skills:
                s_name = s['skill']['name']
                s_id = s['uid']
                if s_id not in db['skills']:
                    db['skills'][s_id] = {'name': s_name, 'count': 1}
                else:
                    db['skills'][s_id]['count'] += 1
    write_dict(db, skills_ids_dtb_name)
    # for k, v in db['skills'].items():
    #     print(k, v['name'], v['count'])
    df = pd.DataFrame.from_dict(db['skills'], orient='index')
    df.to_excel('skills.xlsx')
    print(f"Skills in database:{len(db['skills'])}")
    print(f"Profiles checked:{len(db['checked_profiles'])}")
    return db


def is_file_exist(file):
    if os.path.isfile(file):
        return True
    else:
        return False


def read_dict(file_name):
    if os.path.isfile(file_name):
        with open(file_name, 'rb') as file:
            all_urls_dict = pickle.load(file)
    else:
        all_urls_dict = {}
    return all_urls_dict


def write_dict(dict_to_write, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(dict_to_write, file)


def validate_clipboard(cb):
    try:
        js = json.loads(cb)
        js['results']['urlParams']['q']
        return js
    except json.JSONDecodeError as e:
        print('Not valid JSON')
        return None
    except KeyError:
        print('JSON valid but not contain necessary data')
        return None


def connect_to_dtb(dtb):
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db=dtb,
        charset='utf8mb4',
        cursorclass=DictCursor
    )


def connect_to_mysql():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        charset='utf8mb4',
        cursorclass=DictCursor
    )


def create_database_if_not_exist(dtb):
    connection = connect_to_mysql()
    with closing(connection) as conn:
        with conn.cursor() as cursor:
            cursor._defer_warnings = True
            cursor.execute('CREATE DATABASE IF NOT EXISTS SERP_DTB')


def create_table_if_not_exist(dtb, sql):
    connection = connect_to_dtb(dtb)
    with closing(connection) as conn:
        with conn.cursor() as cursor:
            cursor._defer_warnings = True
            cursor.execute(sql)


def insert_SERP(dtb, table, sj):
    sql = f"""INSERT INTO {table} (timestamp, json, page, q, upwork_relat_skill_ids, relative_skill_names ) 
    VALUES (%s, %s, %s, %s, %s, %s)"""
    connection = connect_to_dtb(dtb)
    with closing(connection) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (sj.timestamp, json.dumps(sj.json), sj.page, sj.q, sj.upwork_relat_skill_ids, sj.upwork_relative_skill_names))
            connection.commit()

def insert_profile(dtb, table, keys, values):
    sql = f"""INSERT INTO {table} ({keys}) VALUES ({values})"""
    connection = connect_to_dtb(dtb)
    with closing(connection) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()


main()


