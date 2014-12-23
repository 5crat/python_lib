#!/usr/bin/env python
# -*-coding:utf-8-*-
#-*-author:scrat-*-


import MySQLdb
import sqlite3


class DB():
    def __init__(self, db_type, db_name='', username='', password='', host='localhost', port=3306, charset='utf8'):
        if db_type == None:
            print 'Not Enter db_type!'
            exit()
        self.db_type = db_type
        self.db_name = db_name
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.charset = charset
        self.__table = ''
        self.__where = ''
        self.__like = ''

        if self.db_type == 'mysql':
            self.conn = MySQLdb.connect(
                db=self.db_name,
                host=self.host,
                user=self.username,
                passwd=self.password,
                charset=self.charset)
        elif self.db_type == 'sqlite':
            self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def get_table(self):
        return self.__table

    def set_table(self, table):
        if 'str' not in str(type(table)):
            print '[-] praram must be string!' + str(__file__)
            table = ''
        self.__table = table

    @staticmethod
    def _param(p):
        if 'dict' in str(type(p)):
            result = {}
            v = []
            k = ''
            for i in p:
                v.append(p[i])
                k += i + ','
                result = {'key': i, 'value': v}
            result = {'key': k.rstrip(','), 'value': tuple(result['value'])}
            return result
        elif 'tuple' in str(type(p)):
            result = ''
            for i in p:
                result += i + ','
            result = result.rstrip(',')
            return result

    def select(self, field):
        field = self._param(field)
        print field['key']
        self.cur.execute("select * from "+self.__table+" where "+field['key']+"=33")
        return self.cur.fetchone()

    def select_row(self, field):
        fields = self._param(field)
        self.cur.execute('select '+fields+' from '+self.__table)
        return self.cur.fetchone()

    def select_all(self, field):
        fields = self._param(field)
        self.cur.execute('select '+fields+' from '+self.__table)
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    t = {'hehe': 1, 'haha': 2, 'xixi': 3, 'woca': 4}
    h = DB(db_type='mysql', username='root', password='', host='localhost', db_name='bank')
    h.set_table('host')
    #print h.select_row(('ip', 'web_title'))
    print h.select({'id': '33'})
