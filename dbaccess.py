from db import Databases

def func():
    d = Databases("u20180586")
    print("operation : ", end='')
    temp = input()

    if temp == "create":
        print("DB : ", end='')
        DB = input()
        print("entries : ", end='')
        entry = input()
        d.createDB(DB, entry)

    elif temp == "read":
        print("DB : ", end='')
        DB = input()
        print("column : ", end='')
        column = input()
        print("statement : ", end='')
        statement = input()
        result = d.readDB(column, DB, statement)
        print(result)
        return result

    elif temp == "insert file 1":
        print("DB : ", end = '')
        DB = input()
        print("filename : ", end = '')
        filename = input()
        print("index : ", end = '')
        index = input()
        d.insertDB_file1(DB, filename, index)

    elif temp == "insert file 2":
        print("DB : ", end = '')
        DB = input()
        print("filename : ", end = '')
        filename = input()
        print("index : ", end = '')
        index = input()
        d.insertDB_file2(DB, filename, index)

    elif temp == "insert":
        print("DB : ", end = '')
        DB = input()
        print("values : ", end = '')
        values = input()
        d.insertDB(DB, values)

    elif temp == "delete":
        print("DB : ", end = '')
        DB = input()
        print("condition : ", end = '')
        cond = input()
        d.deleteDB(DB, cond)

    elif temp == "update":
        print("DB : ", end = '')
        DB = input()
        print("set : ", end = '')
        set = input()
        print("condition : ", end = '')
        cond = input()
        d.updateDB(DB, set, cond)
    
    else:
        print("Not Implemented!")

func()