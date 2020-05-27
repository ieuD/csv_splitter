import glob
import subprocess
import math
import random
from varname import nameof

def get_csv():
    csv_list = glob.glob("./*.csv")
    # print(csv_list)
    if [] == csv_list:
        return None
    else:
        return csv_list


def merger():
    csv_list = get_csv()
    print(csv_list)
    with open("merged.csv", "w") as csv_writer:
        for csv in csv_list:
            with open(csv, "r") as csv_reader:
                all_rows = csv_reader.readlines()
                csv_writer.writelines(all_rows)


def get_count_of_lines():
    process = subprocess.Popen(
        ["wc", "-l", "merged.csv"], stdout=subprocess.PIPE,encoding='utf8')
    out, err = process.communicate()
    if out != "":
        count_row = out.split(" ")[0]
    else:
        count_row = ""

    return count_row


def shuffle_csv(csv):
    with open(csv.replace(".csv", "_shuffled.csv"), "w") as shuffle_writer:
        with open(csv, "r") as reader:
            all_lines = reader.readlines()
            random.shuffle(all_lines)
            shuffle_writer.writelines(all_lines)


def percentage_calc(train, test, dev):
    length = int(get_count_of_lines())
    print("Length of csv :", length)
    amount_train, amount_test, amount_dev = (
        length*train)/100, (length*test)/100, (length*dev)/100

    print(amount_train ,amount_test, amount_dev)    


    splitted_amounts = amount_train+amount_test+amount_dev
    if length > (splitted_amounts):
        amount_dev = length - splitted_amounts + amount_dev

    return int(amount_train), int(amount_test), int(amount_dev)


def split_by_percentage(train=70, test=20, dev=10):
    amount_train, amount_test, amount_dev = percentage_calc(train,test,dev)
    print(amount_train + amount_test + amount_dev)    
    with open("./merged.csv", "r") as csv_reader:
        all_lines = csv_reader.readlines()
        train_data = all_lines[0:amount_train]
        test_data = all_lines[amount_train:amount_train+amount_test]
        dev_data = all_lines[amount_train+amount_test:]

        return train_data,test_data, dev_data


def splitted_csv_serialization():
    train_data,test_data,dev_data = split_by_percentage()
    random.shuffle(train_data)
    random.shuffle(test_data)
    random.shuffle(dev_data)

    # print(train_data,test_data,dev_data)
    x = {
        "train_data" : train_data,
        "test_data" : test_data,
        "dev_data" : dev_data
    }
    
    for k,v in x.items():
        print(k)
        with open(k+".csv","w") as csv_writer:
            csv_writer.writelines(v)
    print("Done")
            
splitted_csv_serialization()