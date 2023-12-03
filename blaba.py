import pandas as pd
from itertools import combinations

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
        # m : 1 2 3
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
            if len(i) > 1:
                if i[0:len(i) - 1] != j[0:len(j) - 1]:
                    break
            # (M,O) : 1, 2, 3
            candidate = generate_candidate_item_sets(df[i],df[j])
            name = str(i + j[len(j) - 1:])
            king[name] = candidate
        cnt = cnt + 1

    # for frequent set more than of equal 2
    king = data_pruning(king,min_sub)
    return king


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
    return ["".join(subseq) for subseq in subsequences]


def generate_association_rules_addition(v):
    x = len(v[-1])
    result_pairs = []
    for i in range(len(v)):
        for j in range(len(v)):
            if v[i] != v[j] and len(v[i]) + len(v[j]) == x:
                b = helper_fun(v[i], v[j])
                if b:
                    result_pairs.append((v[i], v[j]))
    return result_pairs


def helper_fun(str1, str2):
    if str1 > str2:
        str1, str2 = str2, str1
    s = set(str2)
    for ch in str1:
        if ch in s:
            return False
    return True

def generate_association_rules(frequent_itemsets, min_confidence):
    levels = len(frequent_itemsets)
    print("levels : " , levels)
    # print(frequent_itemsets)
    if levels == 1:
        print("No Association Rules can be generated!\n")
        return
    all_rules = []
    strongrule = []
    real_association_rules=[]
    print(frequent_itemsets)
    for level in range(1,levels):
        # print("level in for loop : ",level)
        for itemset, support in frequent_itemsets[level].items():
                subsequences = []
                my_item=itemset
                subsequences=generate_subsequences(my_item)
                # print(subsequences)
                x=generate_association_rules_addition(subsequences)
                print(x)
                real_association_rules=real_association_rules+x
                # you cam mapp first element only {m,k} {k,m} km mot exsits
                orginal_list=x[0]
                result_string=""
                for char in orginal_list:
                    result_string=result_string+str(char)
                stringOfAll = ''
                for z in x[0]:
                    stringOfAll = stringOfAll + z
                print('----------------------------')
                print(stringOfAll)
                list_lift = []
                for i in range(0,int(len(x)/2)):
                    # print('blabla : ',x[i])
                    support_all_item = len(frequent_itemsets[len(stringOfAll)-1][stringOfAll])
                    support_partof_item = len(frequent_itemsets[len(x[i][0])-1][x[i][0]])
                    second_support_partof_item = len(frequent_itemsets[len(x[i][1])-1][x[i][1]])
                    list_lift.append(1/(support_all_item / support_partof_item * second_support_partof_item))
                    print("HHHHEEEE")
                    print(list_lift)

                for rules_inx in x:
                    support_all_item = len(frequent_itemsets[len(result_string)-1][result_string])
                    support_partof_item = len(frequent_itemsets[len(rules_inx[0])-1][rules_inx[0]])
                    confidence = support_all_item / support_partof_item
                    rule = {"first_item": rules_inx[0], "second_item": rules_inx[1], "confidence": confidence}
                    all_rules.append(rule)
                    if confidence >= min_confidence:
                        rule = {"first_item": rules_inx[0], "second_item": rules_inx[1], "confidence": confidence}
                        strongrule.append(rule)
                        

    # for rule in strongrule:
    #     print(
    #         f"Strong Rules: {rule['first_item']} => {rule['second_item']}, Confidence: {rule['confidence']} , Lift:{rule['lift']}"
    #     )
    print('#'*50)
    for rule in all_rules:
        print(
            f"All Rules: {rule['first_item']} => {rule['second_item']}, Confidence: {rule['confidence']}"
        )
    


def run(df, min_sup):
    king = []
    queen = df
    king.append(data_pruning(queen, min_sup))
    while True:
        queen = Key_item_comp(queen, min_sup)
        if queen == {}:
            break
        king.append(queen)
    return king


## running area
df = check_data_format("Horizontal_Format.xlsx")
df = run(df,3)

print(df)
generate_association_rules(df,1)
# for level in range(len(result)):
#     print(f"L{level + 1}:")
#     for item, TID_SET in result[level].items():
#         print(item, f"Support is {len(TID_SET)}\n")

# generate_association_rules(df, 0.5)