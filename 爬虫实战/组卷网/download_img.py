from common.mysql_util import mysql
import requests
import os
import sys


def get_questions(subject):
    with mysql(db="kuaik", host="localhost", password="kuaikang", port=3333) as cur:
        sql = "SELECT * from {subject_key}_question WHERE answer_img is null limit 1000"
        cur.execute(sql.format(subject_key=subject))
        return cur.fetchall()


def get_tags(subject):
    with mysql(db="kuaik", host="localhost", password="kuaikang", port=3333) as cur:
        sql = "SELECT * from {subject_key}_tag_question WHERE tag_img is null limit 1000"
        cur.execute(sql.format(subject_key=subject))
        return cur.fetchall()


def download_question_img(subject_key):
    update = "update {subject_key}_question set answer_img = '{answer_img}' WHERE question_id = '{question_id}';"
    data = get_questions(subject_key)
    with mysql(db="kuaik", host="localhost", password="kuaikang", port=3333) as cur:
        for d in data:
            path = "F:/img/{subject_key}_0424/answer/{question_id}".format(subject_key=subject_key,
                                                                           question_id=d.get('question_id'))
            if not os.path.exists(path): os.makedirs(path)
            response = requests.get(d.get('answer_url'))
            img_type = response.headers.get('Content-Type').split("/")[-1]
            img_path = path + '/' + d.get('question_uuid') + '.' + img_type
            with open(img_path, mode="wb") as f:
                f.write(response.content)
            print(update.format(subject_key=subject_key, answer_img=img_path, question_id=d.get('question_id')))
            cur.execute(update.format(subject_key=subject_key, answer_img=img_path, question_id=d.get('question_id')))


def download_tag_img(subject):
    update = "update {subject_key}_tag_question set tag_img = '{tag_img}' WHERE question_id = '{question_id}';"
    data = get_tags(subject)
    with mysql(db="kuaik", host="localhost", password="kuaikang", port=3333) as cur:
        for d in data:
            path = "F:/img/{subject_key}_0424/tag/{question_id}".format(subject_key=subject_key,
                                                                        question_id=d.get('question_id'))
            if not os.path.exists(path): os.makedirs(path)
            response = requests.get(d.get('tag_url'))
            img_type = response.headers.get('Content-Type').split("/")[-1]
            img_path = path + '/' + d.get('question_uuid') + '.' + img_type
            with open(img_path, mode="wb") as f:
                f.write(response.content)
            print(update.format(subject_key=subject, tag_img=img_path, question_id=d.get('question_id')))
            cur.execute(update.format(subject_key=subject, tag_img=img_path, question_id=d.get('question_id')))


if __name__ == '__main__':
    subject_key = sys.argv[1]
    subject_keys = ["yw", "sx", "yy", "dl", "hx", "ls", "wl", "zz", "sw", 'kx', "sp", "dd", "ty", "ms", "mu"]
    if subject_key not in subject_keys:
        print("subject_key error")
    download_tag_img(subject_key)
