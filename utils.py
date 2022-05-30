from db import Databases
from datetime import date, timedelta, datetime
from tabulate import tabulate

d = Databases("u20180586")

def input_handler(input_type, text=False):
    input_val = None
    if input_type == 'age':
        while True:
            print("\nAge[yr] : ", end='')
            input_val = input()
            if input_val.isnumeric():
                print("")
                break
            else:
                print("Please type correct age!")
        input_val = int(input_val)

    if input_type == 'gender':
        while True:
            print("\nGender[M or W] : ", end='')
            input_val = input()
            if not input_val in ['m', 'w', 'M', 'W']:
                print("Please type correct gender!")
            else:
                print("")
                break
        input_val = input_val.upper()

    if input_type == 'height':
        while True:
            print("\nHeight[cm] : ", end='')
            input_val = input()
            try:
                input_val = float(input_val)
                print("")
                break
            except:
                print("Please type correct height!")

    if input_type == 'weight':
        while True:
            print("\nWeight[kg] : ", end='')
            input_val = input()
            try:
                input_val = float(input_val)
                print("")
                break
            except:
                print("Please type correct weight!")

    if input_type == 'exercise_level':
        while True:
            print("\nChoose your exercise level\n")
            print("1: Rarely exercise.")
            print("2: 1~3 days for a week")
            print("3: 4~5 days for a week")
            print("4: 6~7 days for a week")
            print("5: Exercise very actively everyday")
            print("\nexercise level : ", end='')
            input_val = input()
            if input_val.isnumeric():
                print("")
                break
            else:
                print("Please type correct exercise level!")
        input_val = int(input_val)

    if input_type == 'date':
        while True:
            if text:
                print("\n"+text, end='')
            else:
                
                print("\nDate[yyyymmdd] : ", end='')
            input_val = input()
            try:
                input_val = datetime.strptime(input_val,"%Y%m%d")
                input_val = input_val.date()
                break
            except:
                print("Please type correct date!")

    if input_type == 'amount':
        while True:
            print("\nAmount[g] : ", end='')
            input_val = input()
            try:
                input_val = float(input_val)
                print("")
                break
            except:
                print("Please type correct amount!")

    if input_type == 'disease':
        while True:
            print("\nYour disease: ", end='')
            input_val = input()
            print("")
            try:
                input_val = str(input_val)
                break
            except:
                print("Please type correct disease name!")
    return input_val

def activity_metabolism_rate(age, gender, height, weight, exercise_level):
    if gender == "W":
        bmr = (9.99*weight)+(6.25*height)-(4.95*age)-161
    elif gender == "M":
        bmr = (9.99*weight)+(6.25*height)-(4.95*age)+5

    if exercise_level == "1":
        amr = bmr*1.2
    elif exercise_level == "2":
        amr = bmr*1.375
    elif exercise_level == "3":
        amr = bmr*1.55
    elif exercise_level == "4":
        amr = bmr*1.725
    else:
        amr = bmr*1.9  
    return amr

def cal_nutrient(d, ID, date):
    d.deleteDB("nutrient_info", "id='{}' and date='{}'".format(ID, date))
    diet_infos = d.readDB("*", "diet_info", "where id='{}' and date='{}'".format(ID, date))
    nutrients = []
    amounts = []
    for diet_info in diet_infos:
        fdc_id = diet_info[2]
        food_nutrient_infos = d.readDB("nutrient_id, amount","food_nutrient","where fdc_id="+str(fdc_id))
        weight = float(diet_info[3]) / 100.0

        for nutrient_id,nutrient_amount in food_nutrient_infos:
            if nutrient_id in nutrients:
                amounts[nutrients.index(nutrient_id)] += nutrient_amount*weight
                d.updateDB("nutrient_info", "amount={}".format(amounts[nutrients.index(nutrient_id)]), "id='{}' and date='{}' and nutrient_id={}".format(ID,date,nutrient_id))
            else:
                nutrients.append(nutrient_id)
                amounts.append(nutrient_amount*weight)
                d.insertDB("nutrient_info","'{}','{}',{},{}".format(ID,date,nutrient_id,nutrient_amount*weight))

def lookup_food(food_name):
    d = Databases("u20180586")
    temp = d.readDB("*", "food", "where description ilike '%{}%'".format(str(food_name)))
    length = len(temp)
    temp2 = dict()
    if length == 0:
        print("there is no such food in the data base.")
        return 0
    print("\n--------------------------------------------------------")
    for i in range(length):
        temp2[str(i)] = [temp[i][0]]
        print("{} : {}".format(str(i), temp[i][1]))
    print("--------------------------------------------------------\n")
    while True:
        print("select : ", end='')
        index = input()
        try:
            fid = temp2[index][0]
            break
        except:
            print("Please choose the right food!")

    selected_fdc_id = d.readDB("*", "food", "where fdc_id = {}".format(fid))
    return selected_fdc_id

def add_diet(ID):
    changed_date = set()
    while True:
        print("\n============================\n")
        print("1 : Add diet")
        print("2 : Return to main menu")
        print("\n============================")
        print("Your choice is: ",end='')
        operation = input()
        if not operation in ["1", "2"]:
            print("Please type right command!")
        else:
            break

    if operation == "2":
        return changed_date
    while True:
        date = input_handler('date')
        diet_list = d.readDB("*", "diet_info", "where id='{}' and date='{}'".format(ID, date))
        food_list = []
        for diet in diet_list:
            food_list.append(diet[2])

        while True:
            print("Food name: ", end='')
            food_name = input()
            fdc_id = lookup_food(food_name)
            if fdc_id == 0:
                continue
            fdc_id = fdc_id[0][0]
            if fdc_id in food_list:
                index = food_list.index(fdc_id)
                current_amount = diet_list[index][3]
                print("You already had {}[g] of this food today!".format(current_amount))
                print("\n============================\n")
                print("Do you want to add anyway?\n")
                print("1 : Yes")
                print("2 : No")
                print("\n============================")
                while True:
                    print("Your choice is: ",end='')
                    choice = input()
                    if not choice in ["1", "2"]:
                        print("Please type right command!")
                    else:
                        break
                if choice == '1':
                    print("\n============================\n")
                    print("How will you add it?\n")
                    print("1 : Replace")
                    print("2 : Add")
                    print("3 : No.. I changed my mind")
                    print("\n============================")
                    while True:
                        print("Your choice is: ",end='')
                        choice = input()
                        if not choice in ["1", "2", "3"]:
                            print("Please type right command!")
                        else:
                            break
                    
                    if choice == '3':
                        pass
                    else:
                        amount = input_handler("amount")
                        if choice == '1':
                            d.updateDB("diet_info","amount={}".format(amount),"id='{}' and date='{}' and fdc_id={}".format(ID,date,fdc_id))
                            changed_date.add(date)
                        elif choice == '2':
                            d.updateDB("diet_info","amount={}".format(amount+current_amount),"id='{}' and date='{}' and fdc_id={}".format(ID,date,fdc_id))
                            changed_date.add(date)
                        else:
                            print("Please type the right command!")
                if choice == '2':
                    pass
            else:
                amount = input_handler("amount")
                d.insertDB("diet_info","'{}','{}',{},{}".format(ID,date,fdc_id,amount))
                changed_date.add(date)

            print("\n============================\n")
            print("1 : Add diet to current date")
            print("2 : Change date")
            print("3 : Return to main menu")
            print("\n============================")
            while True:
                print("Your choice is: ",end='')
                operation = input()
                if not operation in ["1","2","3"]:
                    print("Please type right command!")
                else:
                    break
            if operation == "2":
                break
            if operation == "3":
                return changed_date

def analyze(pid, start_date, end_date):
    d = Databases("u20180586")
    p_info = d.readDB("age, gender, disease","personal_info","where id='{}'".format(pid))
    p_amr = d.readDB("amr","personal_amr","where id='{}'".format(pid))[0][0]
    p_age_int = p_info[0][0]
    if p_age_int<19:
        p_age = "15-18"
    elif p_age_int<30:
        p_age = "19-29"
    elif p_age_int<50:
        p_age = "30-49"
    elif p_age_int<65:
        p_age = "50-64"
    elif p_age_int<75:
        p_age = "65-74"
    else:
        p_age = "75-"
    p_gender = p_info[0][1]
    p_disease = p_info[0][2]

    temp = d.readDB("nutrient_id, low, high","recommended_nutrient", "where gender='{}' and age='{}'".format(p_gender,p_age))
    
    recommended_nutrient = dict()
    for i in temp:
        recommended_nutrient[i[0]] = [i[1],i[2]]

    avg = dict()

    days = (end_date - start_date).days + 1

    nutrient_infos = d.readDB("id, name, unit_name","nutrient","")
    food_infos = d.readDB("*", "food", "")
    unit_names = []
    nutrient_ids = []
    nutrient_names = []
    food_names = []
    food_ids = []

    for i in food_infos:
        food_ids.append(i[0])
        food_names.append(i[1])

    for i in nutrient_infos:
        avg[i[0]] = 0
        nutrient_ids.append(i[0])
        nutrient_names.append(i[1])
        unit_names.append(i[2])

    def find_food_name(nid):
        temp = d.readDB('fdc_id,amount','food_nutrient','where nutrient_id={} order by amount desc'.format(nid))
        food_id = temp[0][0]
        food_name = food_names[food_ids.index(food_id)]
        return food_name

    for day in range(days):
        today = str(start_date + timedelta(days = day))
        nutrients = d.readDB("nutrient_id, amount", "nutrient_info", "WHERE id='{}' and date='{}'".format(pid, today))
        for i in range(len(nutrients)):
            nutrient_id, nutrient_amount = nutrients[i]
            try:
                avg[nutrient_id] = avg[nutrient_id] + nutrient_amount
            except:
                avg[nutrient_id] = nutrient_amount

    for key in list(avg.keys()):
        avg[key] = avg[key] / days

    avg_lows = nutrient_ids.copy()
    avg_highs = []
    result = []

    for key in list(avg.keys()):
        try:
            low, high = recommended_nutrient[key]
        except:
            low = 0
            high = 0
            if key == 1003:
                low = 0.07 * p_amr / 4.0
                high = 0.2 * p_amr / 4.0
            if key == 1004:
                low = 0.15 * p_amr / 9.0
                high = 0.3 * p_amr / 9.0
            if key == 1005:
                low = 0.55 * p_amr / 4.0
                high = 0.65 * p_amr / 4.0
            if key == 1008:
                low = 0.8 * p_amr
                high = 1.2 * p_amr
                
        nutrient_name = nutrient_names[nutrient_ids.index(key)]
        unit = unit_names[nutrient_ids.index(key)]
        row = ["{}[{}]".format(nutrient_name, unit), low, avg[key], high]
        result.append(row)

        if avg[key] > low:
            avg_lows.remove(key)

        if avg[key] > high:
            avg_highs.append(key)
    print("====================================================================================\n")
    print("< Nutrient Report >\n")
    print(tabulate(result, headers=["Nutrient[Unit]", "Lower limit", "Your Average Intake", "Upper limit"], numalign='left'))

    under_nutrient = d.readDB("id","nutrient_disease","WHERE disease_name ilike '%{}%' and status = 'under'".format(p_disease))
    over_nutrient = d.readDB("id","nutrient_disease","WHERE disease_name ilike '%{}%' and status = 'over'".format(p_disease))
    under = []
    over = []
    for i in range(len(under_nutrient)):
        under += under_nutrient[i]
    for i in range(len(over_nutrient)):
        over += over_nutrient[i]
    
    print("====================================================================================\n")
    print("< Undertaken Nutrients >\n")
    
    low_result = []
    for nid in avg_lows:
        low_nutrient = nutrient_names[nutrient_ids.index(nid)]
        food_name = find_food_name(nid)
        low_result.append([low_nutrient, food_name])
    
    if low_result == []:
        print("None! Well done!\n")
    else:
        print(tabulate(low_result, headers=["Nutrient", "Recommended Food"], numalign='left'))
    
    print("====================================================================================\n")
    print("< Overtaken Nutrients >\n")
    high_result = []
    for nid in avg_highs:
        high_nutrient = nutrient_names[nutrient_ids.index(nid)]
        food_name = find_food_name(nid)
        high_result.append([high_nutrient, food_name])
    if high_result == []:
        print("None! Well done!\n")
    else:
        print(tabulate(high_result, headers=["Nutrient", "Food to avoid"], numalign='left'))

    print("====================================================================================\n")
    print("< You might get these diseases because of ... >\n")
    n_d_result = []
    for nid in avg_lows:
        n_name = nutrient_names[nutrient_ids.index(nid)]
        temp = d.readDB("disease_name", "nutrient_disease", "where id={} and status='under'".format(nid))
        temp2 = []
        for i in temp:
            temp2.append(i[0])
        n_d_result.append([n_name, "undertaken", ', '.join(temp2)])
    for nid in avg_highs:
        n_name = nutrient_names[nutrient_ids.index(nid)]
        temp = d.readDB("disease_name", "nutrient_disease", "where id={} and status='over'".format(nid))
        temp2 = []
        for i in temp:
            temp2.append(i[0])
        n_d_result.append([n_name, "overtaken", ', '.join(temp2)])
    if n_d_result == []:
        print("None! Well done!\n")
    else:
        print(tabulate(n_d_result, headers=["Nutrient", "Status", "Disease"], numalign='left'))


    n_name2 = []    
    for low_n in under:
        if low_n in avg_lows:
            n_name2.append(["undertake",nutrient_names[nutrient_ids.index(low_n)]])
    for high_n in over:
        if high_n in avg_highs:
            n_name2.append(["overtake",nutrient_names[nutrient_ids.index(high_n)]])
    if n_name2 == []:
        print("====================================================================================\n")
        print("You're dealing well with your disease '{}'. Good job!".format(p_disease))
    else:
        print("\n************************* ! WARNING ! ************************* \n")
        print("Your disease '{}' can get worse if you keep ... \n".format(p_disease))
        print(tabulate(n_name2, headers=["Status", "Nutrient"], numalign='left'))
        print("")
    
def show_diet(ID, date):
    d = Databases("u20180586")
    diet_list = d.readDB("fdc_id, amount","diet_info","where id='{}' and date='{}'".format(ID, date))
    result = []
    for fdc_id, amount in diet_list:
        food = d.readDB("description", "food", "where fdc_id={}".format(fdc_id))[0][0]
        result.append([food, amount])
    print("")
    print(tabulate(result, headers=["Food name", "Amount[g]"], numalign='left'))
