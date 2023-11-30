import pandas as pd


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


def bad_bunny(file_path):
    df = read_data_from_excel(file_path)
    original = df.groupby("item")["TID"].apply(list).to_dict()
    return original


def data_pruning(df, min_sup):
    return {item: tid_list for item, tid_list in df.items() if len(tid_list) >= min_sup}


def key_item_comp(df, min_sub):
    keys = list(df.keys())
    king = {}

    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            if len(keys[i]) > 1 and keys[i][:-1] != keys[j][:-1]:
                break

            candidate = fun(df[keys[i]], df[keys[j]])
            name = keys[i] + keys[j][-1]
            king[name] = candidate

    king = data_pruning(king, min_sub)
    return king


def run(df, min_sup):
    king = [data_pruning(df, min_sup)]

    while True:
        df = key_item_comp(df, min_sup)
        if not df:
            break
        king.append(df)

    return king


def fun(v1, v2):
    return list(set(v1) & set(v2))


def generate_association_rules(frequent_itemsets, min_confidence):
    levels = len(frequent_itemsets)

    if levels == 1:
        print("No Association Rules can be generated!\n")
        return

    all_rules = []

    for level in range(1, levels):
        for itemset, support in frequent_itemsets[level].items():
            for i in range(len(itemset)):
                before = itemset[:i]
                after = itemset[i:]
                # print(before)
                # print(after)
                before_support = frequent_itemsets[level][before]
                confidence = len(support) / before_support

                if confidence >= min_confidence:
                    rule = {"before": before, "after": after, "confidence": confidence}
                    all_rules.append(rule)

    # Print the generated association rules
    for rule in all_rules:
        print(
            f"Rule: {rule['before']} => {rule['after']}, Confidence: {rule['confidence']}"
        )


def run(df, min_sup):
    king = []
    queen = df
    king.append(data_pruning(queen, min_sup))
    while True:
        queen = key_item_comp(queen, min_sup)
        if queen == {}:
            break
        king.append(queen)
    return king


df = bad_bunny("Horizontal_Format.xlsx")
result = run(df, 4)
print(result)

for level in range(len(result)):
    print(f"L{level + 1}:")
    for item, TID_SET in result[level].items():
        print(item, f"Support is {len(TID_SET)}\n")

generate_association_rules(df, 0.5)
