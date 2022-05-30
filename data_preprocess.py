def preprocess_food():
    f = open("data/foundation_food.csv", "r")
    # g = open("data/food.csv", "r")
    h = open("data/food_nutrient.csv", "r")
    # f2 = open("data/foundation_food_name.csv", "w")
    g2 = open("data/foundation_food_nut.csv", "w")

    fdc_id = []
    line = f.readline()
    while True:
        line = f.readline()
        if not line:
            break
        line_list = line[1:-2].split('","')
        fdc_id.append(line_list[0])

    # line = g.readline()
    # f2.write(line)
    # while True:
    #     line = g.readline()
    #     if not line:
    #         break
    #     line_list = line[1:-2].split('","')
    #     if line_list[0] in fdc_id:
    #         f2.write(line)

    line = h.readline()
    g2.write(line)
    while True:
        line = h.readline()
        if not line:
            break
        line_list = line[1:-2].split('","')
        if line_list[1] in fdc_id:
            g2.write(line)



def preprocess_nutrient():
    # nutrient_list = [1003, 1079, 1104, 1175, 1178, 1158, 1162, 1087, 1093, 1095, 1089]
    nutrient_list = [1008, 1003, 1004, 1005, 1079, 1106, 1109, 1162 ,1175 ,1178 ,1087, 1093, 1089, 1095]
    f = open("data/nutrient.csv", "r")
    g = open("data/important_nutrient.csv", "w")

    line = f.readline()
    g.write(line)

    while True:
        line = f.readline()
        if not line:
            break
        line_list = line[1:-2].split('","')
        if int(line_list[0]) in nutrient_list:
            g.write(line)
    f.close()
    g.close()

def preprocess_food_nutrient():
    food_nutrient = open("data/food_nutrient.csv", "r")
    nutrient = open("data/important_nutrient.csv", "r")
    foundation_food = open("data/foundation_food_name.csv", "r")
    output = open("data/foundation_food_nutrient2.csv", "w")

    ### get fdc_id of foundation food
    fdc_id = []
    line = foundation_food.readline()
    while True:
        line = foundation_food.readline()
        if not line:
            break
        line_list = line[1:-2].split('","')
        fdc_id.append(line_list[0])
    foundation_food.close()
    
    ### get nutrient_id of important nutrients
    nutrient_id = []
    ine = nutrient.readline()
    while True:
        line = nutrient.readline()
        if not line:
            break
        line_list = line[1:-2].split('","')
        nutrient_id.append(line_list[0])
    nutrient.close()
    
    # write to output file
    line = food_nutrient.readline()
    output.write(line)

    while True:
        line = food_nutrient.readline()
        if not line:
            break
        line_list = line[1:-2].split('","')
        if line_list[1] in fdc_id:
            if line_list[2] in nutrient_id:
                output.write(line)
                
                
# preprocess_food()
# preprocess_nutrient()
preprocess_food_nutrient()


