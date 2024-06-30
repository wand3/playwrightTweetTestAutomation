#!/usr/bin/python3
def text_to_list(filename):   
    with open(filename, "r") as file:
        msg_list = file.readlines()
        
        li = []
        for i in msg_list:
            new_list = i.strip('')
            li.append(new_list)
        # print(len(li))

        # res = []
        cleaned_list = [line.strip() for line in li if line.strip()]
        return cleaned_list        


# print(text_to_list(filename="pre_presale.txt"))