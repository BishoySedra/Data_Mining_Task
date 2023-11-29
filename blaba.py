import pandas as pd
from itertools import combinations 

Horizontal_Data = 0
freq_item_set = []
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
    
    
def check_data_format(pathfile):
    orginal  = {}
    df = read_data_from_excel(pathfile)
    print(df.iloc[0])
    for i in range(len(df)):
        orginal[df.iloc[i][1]] = []
    for i in range(len(df)):
        orginal[df.iloc[i][1]].append([df.iloc[i][0]])
    return orginal
    
print(check_data_format('Horizontal_Format.xlsx'))
df = check_data_format('Horizontal_Format.xlsx')

# def support_removing(data,min_support): #if length 1 
def generate_frequent_item_sets(data,min_support):  
    support_items={}
    frequent_item_set=[]
    for item in df.keys():  
        support_items[item] =len(df[item])  #C1
        if len(item) == 1: 
            print(f"item {item} Support : {len(df[item])}")
            
        
    for item, support in support_items.items():
        if support >= min_support:
                frequent_item_set.append(item)#L1
    freq_item_set.append(list(frequent_item_set)) #list of set
    # print(freq_item_set)
    # print(frequent_item_set) 
    index = 2
    while True:
            elements = set()
            for item_set in freq_item_set[index - 2]:
                for item in item_set:
                    elements.add(item)
            print("###################################")
            # print(elements)
            elements_combinations = list(combinations(elements, index))
            print(elements_combinations)
            # print(support_items.items())
            for item_set in elements_combinations: 
                for item in range(index-1):
                    common = set(map(tuple,(df[item_set[item]]))).intersection(set(map(tuple,(df[item_set[item+1]])))) # Convert lists of lists to sets of tuples to make them hashable
                support_items[item_set] = len(common)
            print("###################################")
                
            # print(support_items.items())
            for item, support in support_items.items():
                if len(item) == index:
                    if support >= min_support:
                        frequent_item_set.append(item)
            # print(frequent_item_set)
            freq_item_set.append(list(frequent_item_set))
            count = 0
            for item in range(index-1):
                first_list= freq_item_set[count]
                freq_item_set[index - 1]=list(set(freq_item_set[index - 1]).difference(first_list))
                count+=1
            
            print(freq_item_set)
            print(len(freq_item_set[-1]))
            if len(freq_item_set[-1]) == 0:
                break
            
            index+=1


# support_removing(df,2)    
generate_frequent_item_sets(df,3)

