import pandas as pd



def read_data_from_excel(file_path):
# read by default 1st sheet of an excel file
        data = pd.read_excel(file_path)
        first_column = data.columns[0]
        if first_column.capitalize() == "Tid" or first_column.capitalize() == "Sid":
            Horizontal_Data = 1
        itemset_column = data.columns[1]
        data_in_list = data[[first_column, itemset_column]].values.tolist()
        for i in range(len(data_in_list)):
            data_in_list[i][1] = str(data_in_list[i][1]).split(',')
            
        data = []
        for item in data_in_list:
            number = item[0]
            letters = item[1]
            for letter in letters:
                data.append([number,letter])
        
        df = pd.DataFrame(data,columns = ["TiD" , "items"])
        df.drop_duplicates(inplace=True)
        return df
    
    
def BadBunny(pathfile):
    orginal  = {}
    df = read_data_from_excel(pathfile)
    for i in range(len(df)):
        orginal[df.iloc[i][1]] = []
    for i in range(len(df)):
        orginal[df.iloc[i][1]].append(df.iloc[i][0])
    return orginal
    

df = check_data_format('Horizontal_Format.xlsx')
# print(df)

def data_pruning(df,min_sup):
    res = {}
    for i in df.items():
        # m : 1 2 3
        if len(i[1]) >= min_sup:
            res[i[0]] = i[1]
    
    return res

# jimmy nitron
def fun(v1, v2):
    i = 0
    j = 0
    v = []
    while i < len(v1) and j < len(v2):
        while i < len(v1) and j < len(v2) and v1[i] != v2[j]:
            if v1[i] < v2[j]:
                i += 1
            else:
                j += 1
        if i < len(v1) and j < len(v2) and v1[i] == v2[j]:
            v.append(v1[i])
            i += 1
            j += 1
    return v

def Key_item_comp(df,min_sub):

    keys = []
    king = {}
    cnt = 1


    # data pruning
    df = data_pruning(df,min_sub)
    keys = list(df.keys())
    n = len(keys)


    # compination
    for i in keys:
        for j in keys[cnt:n]:
            if len(i) > 1:
                if i[0:len(i) - 1] != j[0:len(j) - 1]:
                    break
            # (M,O) : 1, 2, 3
            candidate = fun(df[i],df[j])
            name = str(i + j[len(j) - 1:])
            king[name] = candidate
        cnt = cnt + 1
    
    # for frequent set more than of equal 2
    king = data_pruning(king,min_sub)
    return king



def run(df,min_sup):
    king = []
    queen = df
    king.append(data_pruning(queen,min_sup))
    while True:
        queen = Key_item_comp(queen,min_sup)
        if queen == {}:
            break
        king.append(queen)
    return king

df = run(df,3)
print(df)
