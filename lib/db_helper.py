#! python3
import sqlite3
import time


def connect(path):
    return sqlite3.connect(path, check_same_thread=False)


def disconnect(conn):
    conn.close()


def cursor(conn):
    return conn.cursor()


def drop_table(conn, table):
    cur = cursor(conn)
    cur.execute('DROP TABLE IF EXISTS ' + table)
    conn.commit()
    cur.close()


def create_table(conn):
    drop_table(conn, "urls")
    drop_table(conn, "images")
    cur = cursor(conn)
    cur.execute('CREATE TABLE "urls" ('
                '"url"  TEXT(255) NOT NULL COLLATE NOCASE ,'
                '"time"  INTEGER'
                ');')
    cur.execute('CREATE UNIQUE INDEX "urlIndex"'
                'ON "urls" ("url" COLLATE NOCASE ASC);')
    cur.execute('CREATE TABLE "images" ('
                '"url"  TEXT(255) NOT NULL COLLATE NOCASE ,'
                'PRIMARY KEY ("url")'
                ');')
    conn.commit()
    cur.close()


def insert_url(conn, url):
    cur = cursor(conn)
    cur.execute('INSERT INTO `urls` (`url`, `time`) VALUES (?, ?)', (url, int(time.time() * 1000)))
    conn.commit()
    cur.close()


def insert_image(conn, url):
    cur = cursor(conn)
    cur.execute('INSERT INTO `images` (`url`) VALUES (?)', [url])
    conn.commit()
    cur.close()


def find_url(conn, url):
    cur = cursor(conn)
    cur.execute('SELECT * FROM `urls` WHERE `url`=?', [url])
    result = cur.fetchone()
    cur.close()
