import psycopg2

class Databases():
    def __init__(self, dbname):
        self.db = psycopg2.connect(host='biostar.kaist.ac.kr', dbname=dbname ,user='u20180586',password='bipro20180586',port=5432)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self,query,args={}):
        self.cursor.execute(query,args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.cursor.commit()
    
    def createDB(self, DB, entry):
        sql = "CREATE TABLE {DB} ({entry});".format(DB=DB, entry=entry)
        print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
                print(" create DB  ",e) 

    def insertDB(self, DB, values):
        sql = "INSERT INTO {DB} VALUES ({values})".format(DB = DB, values=values)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB  ",e) 

    def insertDB_file1(self, DB, filename, index):
        f = open(filename, "r")
        entry_str = f.readline()[1:-2].split('","')
        entry = []
        if index == "all":
            for i in range(len(entry_str)):
                entry.append(i)
        else:
            index = index.split(",")
            for i in index:
                entry.append(entry_str.index(i))
        
        while True:
            data = f.readline()
            if not data:
                break
            data = data[1:-2].split('","')
            query = ""
            for i in entry:
                if data[i].isnumeric():
                    query = query + data[i] + ","
                else:
                    query = query + "'" + data[i] + "',"

            sql = "INSERT INTO {DB} VALUES ({query});".format(DB=DB, query=query[:-1])
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except Exception as e :
                print(" insert DB  ",e) 

    def insertDB_file2(self, DB, filename, index):
        f = open(filename, "r")
        entry_str = f.readline()[:-1].split(',')
        entry = []
        if index == "all":
            for i in range(len(entry_str)):
                entry.append(i)
        else:
            index = index.split(",")
            for i in index:
                entry.append(entry_str.index(i))
        
        while True:
            data = f.readline()
            if not data:
                break
            data = data[:-1].split(',')
            query = ""
            for i in entry:
                if data[i].isnumeric():
                    query = query + data[i] + ","
                else:
                    query = query + "'" + data[i] + "',"

            sql = "INSERT INTO {DB} VALUES ({query});".format(DB=DB, query=query[:-1])
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except Exception as e :
                print(" insert DB  ",e) 

    def readDB(self,colum, table, statement):
        sql = "SELECT {colum} FROM {table} {statement};".format(colum=colum,table=table,statement=statement)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e :
            result = (" read DB err",e)
    
        return result

    def updateDB(self, DB, set, where):
        sql = "UPDATE {DB} SET {set} WHERE {where};".format(DB = DB, set = set, where = where)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" update DB  ",e) 

    def deleteDB(self, DB, where):
        sql = "DELETE FROM {DB} WHERE {where};".format(DB=DB, where=where)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" delete DB  ",e) 