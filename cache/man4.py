#-*- coding : utf-8 -*-
import pandas as pd
import csv


if __name__ == "__main__":
    with open("C:\\Users\\Administrator\\Desktop\\1.csv","r") as csvfile: 
        read = csv.reader(csvfile)
        for row in read:
            with open("C:\\Users\\Administrator\\Desktop\\1.csv","r") as csvfile2:
                read2 = csv.reader(csvfile2)
                for ro in read2:
                    if((row[0]==ro[2]) and (row[1]!=ro[3])):
                         print(row[0])
                    else:
                        pass