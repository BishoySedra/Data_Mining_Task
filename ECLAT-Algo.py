import pandas as pd
from itertools import combinations

all_rules = []
strong_rules = []
lift_list=[]

def read_data_from_excel(file_path):
    data = pd.read_excel(file_path)
    first_column = data.columns[0]

    if "id" in first_column.lower():
        itemSet_column = data.columns[1]
        data_in_list = data[[first_column, itemSet_column]].values.tolist()
        data = [
            (number, letter)
            for number, letters in data_in_list
            for letter in str(letters).split(",")
        ]

    df = pd.DataFrame(data, columns=["TID", "item"])
    df.drop_duplicates(inplace=True)
    return df

def check_data_format(pathfile):
    orginal  = {}
    df = read_data_from_excel(pathfile)
    for i in range(len(df)):
        orginal[df.iloc[i][1]] = []
    for i in range(len(df)):
        orginal[df.iloc[i][1]].append(df.iloc[i][0])
    return orginal

def data_pruning(df,min_sup):
    res = {}
    for i in df.items():
        if len(i[1]) >= min_sup:
            res[i[0]] = i[1]
    return res

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
            if len(i) >= 1:
                if not check_condition_join(i,j):
                    break
            # (M,O) : 1, 2, 3
            candidate = generate_candidate_item_sets(df[i],df[j])
            if len(candidate)>=min_sub:
                name=str(join(i,j))
                king[name] = candidate
            # print(candidate)
        cnt = cnt + 1

    # for frequent set more than of equal 2
    king = data_pruning(king,min_sub)
    return king

def check_condition_join(str1,str2):
    list1 = str1.split(',')
    list2 = str2.split(',')
    i=j=0
    x=0
    for item1, item2 in zip(list1[:-1], list2[:-1]):
        if item1!=item2:
            return False
    return True

def join(i,j):
    list1 = j.split(',')
    last_str=list1[len(list1)-1]
    return i+","+last_str

def generate_candidate_item_sets(v1, v2):
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

def generate_subsequences(sequence):
    subsequences = []
    for r in range(1, len(sequence) + 1):
        # Use combinations to generate all subsequences of length r
        subsequences.extend(combinations(sequence, r))
    return [",".join(subseq) for subseq in subsequences]

def helper_fun(str1, str2):
    list1 = str1.split(',')
    list2 = str2.split(',')
    s = set(list1)
    for ch in list2:
        if ch in s:
            return False
    return True

def generate_association_rules_addition(v):
    x = len(v[-1])
    result_pairs = []
    # print(v)
    for i in range(len(v)):
        for j in range(len(v)):
            # here
            temp=v[i]+","+v[j]
            if v[i] != v[j] and len(temp) == x:
                b = helper_fun(v[i]+",", v[j])
                # print(temp,v)
                if b:
                    # print(v[i]+",",v[j])

                    result_pairs.append((v[i]+",",v[j]))
    return result_pairs

def convert_to_one_list(frequent_itemsets):
    result_dict = {}
    for d in frequent_itemsets:
        for key, value in d.items():
            if key in result_dict:
                result_dict[key].extend(value)
            else:
                result_dict[key] = value
    return result_dict

def generate_association_rules(frequent_itemsets, min_confidence,number_trans):
    levels = len(frequent_itemsets)
    # print("levels : " , levels)
    # print(frequent_itemsets)
    if levels == 1:
        print("No Association Rules can be generated!")
        return


    result_dict=convert_to_one_list(frequent_itemsets)
    # print(frequent_itemsets)
    one_list=convert_to_one_list(frequent_itemsets)
    # print(frequent_itemsets)
    for level in range(1,levels):
        # print("level in for loop : ",level)
        for itemset, support in frequent_itemsets[level].items():
                subsequences = []
                my_item=itemset
                # print(my_item)
                my_list=my_item.split(',')
                subsequences=generate_subsequences(my_list)
                # print("sub")
                # print(subsequences)
                x=generate_association_rules_addition(subsequences)
                orginal_list=x[0]
                # print(x)
                result_string=""
                # print(x)
                for char in orginal_list:
                    result_string=result_string+str(char)

                # result_string=str(result_string[1:])
                # print(result_string)

                # first_comma_index = result_string.find(',')
                # print(result_string)


                # # print('----------------------------')
                for rules_inx in x:
                    # print("rules_inx",rules_inx)
                    # comma
                    string1=rules_inx[0]
                    string2=rules_inx[1]
                    real_string1=string1[:len(string1)-1]
                    # print("real_string1",real_string1)
                    # # print("string1",string1)
                    # print("string2",string2)

                    support_all_item = len(one_list[result_string])
                    support_partof_item = len(one_list[real_string1])
                    confidence = support_all_item / support_partof_item
                    # print("support_all_item",support_all_item)
                    # print("support_partof_item",support_partof_item)
                    # print("confidence",confidence)
                    rule = {"first_item": real_string1, "second_item": string2, "confidence": confidence}
                    all_rules.append(rule)
                    if confidence >= min_confidence:
                        rule = {"first_item": real_string1, "second_item": string2, "confidence": confidence}
                        strong_rules.append(rule)
                temp=0
                # print(x)
                for rules_inx1 in x:
                    if temp == len(x)/2:
                        break
                    # print(rules_inx1)
                    string1=rules_inx1[0]
                    string2=rules_inx1[1]
                    real_string1=string1[:len(string1)-1]
                    support_all_item = len(one_list[result_string])
                    support_partof_item1 = len(one_list[real_string1])
                    support_partof_item2 = len(one_list[string2])

                    lift = (support_all_item/number_trans) / ((support_partof_item1/number_trans)*(support_partof_item2/number_trans))
                    # print(lift)

                    rule = {"first_item": real_string1 , "second_item": string2 , "lift": lift}
                    # print(rule)
                    lift_list.append(rule)
                    temp=temp+1


def print_all():
    if len(all_rules) != 0:
        print("\nThe Frequent Itemsets in the form of association rules:\n")
        for rule in all_rules:
            print(f"{rule['first_item']} => {rule['second_item']}, Confidence= {round(rule['confidence'],2)}")

    print('-'*50)

    if len(strong_rules) != 0:
        print("\nThe strong association rules: \n")
        for rule in strong_rules:
            print(f"{rule['first_item']} => {rule['second_item']}, Confidence= {round(rule['confidence'],2)}")

    print('-'*50)

    if len(lift_list) != 0:
        # print(len(lift_list))
        print("\nThe lift : \n")
        for rule in lift_list:
            print(f"{rule['first_item']} => {rule['second_item']}, lift = {round(rule['lift'],2)}" , end = '')
            if rule['lift'] == 1:
                print(" --> Independent")
            elif rule['lift'] < 1:
                print(" --> Dependent , Negative Correlation")
            else :
                print(" --> Dependent , Positive Correlation")

def run(df, min_sup):
    king = []
    queen = df
    king.append(data_pruning(queen, min_sup))
    #print(data_pruning(queen, min_sup))
    while True:
        queen = Key_item_comp(queen, min_sup)
        # print (queen)
        if queen == {}:
            break
        king.append(queen)
    return king

def main():

    try:
        min_support = float(input("Enter a value of min support: "))
        min_confidence = float(input("Enter a value of min confidence: "))
    except ValueError:
        print("Please enter a valid input!")
        main()
        return

    # pathfile="Horizontal_Format.xlsx"
    pathfile="String_Format.xlsx"
    df = pd.read_excel(pathfile)
    number_trans=len(df)

    # print(df)
    df=check_data_format(pathfile)
    df=run(df,min_support)

    print(f"\n#levels= {len(df)}\n")
    # print(len(df))
    print('-'*50)

    # print(df)
    for i in range(len(df)):
        print(f"L{i+1}:")
        for item, ids in df[i].items():
            print(f"\t{item}: {ids}")

    print('-'*50)
    generate_association_rules(df, min_confidence, number_trans)

    # x=Key_item_comp(df,2)
    print_all()
    
    
    
main()