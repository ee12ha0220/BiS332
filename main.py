from platform import architecture
from tkinter.tix import InputOnly
from db import Databases
from datetime import date, timedelta
from utils import analyze, cal_nutrient, input_handler, activity_metabolism_rate, add_diet, show_diet

def main():
    d = Databases("u20180586")
    print("\n===================================================\n")
    print(" _    _        _   ")                            
    print("| |  | |      | |                              ")
    print("| |  | |  ___ | |  ___   ___   _ __ ___    ___ ")
    print("| |/\| | / _ \| | / __| / _ \ | '_ ` _ \  / _ \ ")
    print("\  /\  /|  __/| || (__ | (_) || | | | | ||  __/ ")
    print(" \/  \/  \___||_| \___| \___/ |_| |_| |_| \___|   ")
    
    print("    _____              ___  ______ ___  ___")
    print("   |_   _|            / _ \ |  _  \|  \/  |")
    print("     | |    ___      / /_\ \| | | || .  . |")
    print("     | |   / _ \     |  _  || | | || |\/| |")
    print("     | |  | (_) |    | | | || |/ / | |  | |")
    print("     \_/   \___/     \_| |_/|___/  \_|  |_/")
    print("\n===================================================\n")
                                    
                                        

    print("What is your ID? : ", end = '')
    ID = input()

    personal_info = d.readDB("*", "personal_info", "where id='{}'".format(ID))

    if personal_info == []:
        print("No match found! Would you like to register?\n")
        print("1 : Yes")
        print("2 : Maybe next time...")
        choice = input()
        if choice == '2':
            return
        elif choice != '1':
            print("Please type the right command!")
        else:
            print("Please type your personal information")
            
            age = input_handler('age')
            gender = input_handler('gender')
            height = input_handler('height')
            weight = input_handler('weight')
            exercise_level = input_handler('exercise_level')
            disease = input_handler('disease')

            amr = activity_metabolism_rate(age, gender, height, weight, exercise_level)

            d.insertDB("personal_info", "'{}',{},'{}',{},{},{},'{}'".format(ID, age, gender, height, weight, exercise_level, disease))
            d.insertDB("personal_amr", "'{}',{}".format(ID,amr))
            personal_info = d.readDB("*", "personal_info", "where id='{}'".format(ID))

    else:
        print("\nSuccessfully logged in!\n")

    personal_info = personal_info[0]
    changed_date = set()
    while True:
        for date in changed_date:
            cal_nutrient(d, ID, date)
        changed_date = set()
        
        print("============================\n")
        print("What do you want to do?\n")
        print("1 : Upload my diet")
        print("2 : Check my diet")
        print("3 : Change my information")
        print("4 : Analyze my diet")
        print("5 : Exit")
        print("\n============================")
        print("Your choice is: ",end='')
        choice = input()
        if choice == '1':
            changed_date = add_diet(ID)
        elif choice == '2':
            date = input_handler("date")
            show_diet(ID, date)
        elif choice == '3':
            while True:
                print("\n============================\n")
                print("What would you like to change?\n")
                print("1 : Age")
                print("2 : Height")
                print("3 : Weight")
                print("4 : Exercise level")
                print("5 : Disease")
                print("6 : I'm done!")
                print("\n============================")
                print("Your choice is: ",end='')
                choice = input()
                if choice == '1':
                    age = input_handler('age')
                    amr = activity_metabolism_rate(age, personal_info[2], personal_info[3], personal_info[4], personal_info[5])
                    d.updateDB("personal_info", "age={}".format(age), "id='{}'".format(ID))
                    d.updateDB("personal_amr", "amr={}".format(amr), "id='{}'".format(ID))
                elif choice == '2':
                    height = input_handler('height')
                    amr = activity_metabolism_rate(personal_info[1], personal_info[2], height, personal_info[4], personal_info[5])
                    d.updateDB("personal_info", "height={}".format(height), "id='{}'".format(ID))
                    d.updateDB("personal_amr", "amr={}".format(amr), "id='{}'".format(ID))
                elif choice == '3':
                    age = input_handler('weight')
                    amr = activity_metabolism_rate(personal_info[1], personal_info[2], personal_info[3], weight, personal_info[5])
                    d.updateDB("personal_info", "weight={}".format(weight), "id='{}'".format(ID))
                    d.updateDB("personal_amr", "amr={}".format(amr), "id='{}'".format(ID))
                elif choice == '4':
                    exercise_level = input_handler('exercise_level')
                    print(exercise_level)
                    amr = activity_metabolism_rate(personal_info[1], personal_info[2], personal_info[3], personal_info[4], exercise_level)
                    d.updateDB("personal_info", "exercise_level={}".format(exercise_level), "id='{}'".format(ID))
                    d.updateDB("personal_amr", "amr={}".format(amr), "id='{}'".format(ID))
                elif choice == '5':
                    disease = input_handler('disease')
                    d.updateDB("personal_info", "disease='{}'".format(disease), "id='{}'".format(ID))
                elif choice == '6':
                    break
                else:
                    print("Please type the correct command!")
        elif choice == '4':
            start_date = input_handler('date', "Start date[yyyymmdd] : ")
            end_date = input_handler('date', "End date[yyyymmdd] : ")
            analyze(ID, start_date, end_date)
            pass
        elif choice == '5':
            break
        else:
            print("Please type the correct command!")

main()