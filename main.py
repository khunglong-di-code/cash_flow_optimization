from Algorithm.Check_Graph import *
from Algorithm.General_Graph import *
from Algorithm.Fixed_Height_Grid import *
from Algorithm.Mincost_Maxflow import *

from Data.Class_DebtGraph import *
from Data.Class_edge import *
from Data.Class_DebtGraph import *
from Data.create_input_alg import *
from Data.Extended_Data_Structures import *

import csv
import os

csv_file = "cash_flow_optimization_dataset.csv"

with open(csv_file, newline = '', encoding = 'utf-8') as file:
    reader = csv.reader(file)

print ("Khởi động chương trình ! \n "

choice = int(input()) 

switch_case () 