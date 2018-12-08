# Expense-Manager
# Copyright (c) 2018 Reza Soltani
# Distributed under the GPL software license, see the accompanying
# file LICENSE or https://opensource.org/licenses/GPL-3.0.

import csv
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

import matplotlib.pyplot as plt


# input files
prefix = 'data/'
files = []

# expense types
expense_types = ["GROCERIES", "RESTAURANT", "GAS", "PARKING", "HEALTH", "OTHER", "SHOPPING"]

# Add specific expense labels here
# TODO: Automate this process
groceries_terms = []
food_terms = []
gas_items = []
parking_items = []
health_items = []
shopping_items = []
interest_items = []

expense_total = [0, 0, 0, 0, 0, 0, 0]
expense_vtotal = [0, 0, 0, 0, 0, 0, 0]

payment_type = "PAYMENT"
payment_total = 0
payment_vtotal = 0


interest_type = "INTEREST"
interest_total = 0
interest_vtotal = 0


expense_value_overall = [0, 0, 0, 0, 0, 0, 0]
items_size = 7


def drawPie(items, values):


    labels = items
    sizes = values
    explode = (0, 0, 0, 0)


    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels,
            shadow=False, startangle=90, labeldistance=1, rotatelabels=True, autopct='%1.1f%%')
    ax1.axis('equal')

    plt.show()


def drawBar(items, values):


    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    # labels = expense_types
    # sizes = expense_vtotal
    # explode = (0, 0, 0, 0)

    # fig1, ax1 = plt.subplots()
    # ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
    #         shadow=True, startangle=90)
    # ax1.axis('equal')

    # bar graph
    y_pos = np.arange(len(items))

    plt.bar(y_pos, values, align='center', color="blue")
    plt.ylabel('Dollars')
    plt.xticks(y_pos, items)


def submitExpenses(expense_vtotal):

    global expense_value_overall

    for i, item in enumerate(expense_vtotal):
        expense_value_overall[i] += item



def categorize(name, value, payment):
    global expense_vtotal, expense_total, payment_total, payment_vtotal, payment_type, interest_vtotal, interest_total, expense_value_overall

    if (payment == True):
        payment_total += 1
        payment_vtotal += value
        return payment_type

    if any(x in name for x in groceries_terms):
        expense_total[0] += 1
        expense_vtotal[0] +=  value
        return expense_types[0]

    elif any(x in name for x in food_terms):
        expense_total[1] += 1
        expense_vtotal[1] += value
        return expense_types[1]

    elif any(x in name for x in gas_items):
        expense_total[2] += 1
        expense_vtotal[2] +=value
        return expense_types[2]

    elif any(x in name for x in parking_items):
        expense_total[3] += 1
        expense_vtotal[3] += value
        return expense_types[3]

    elif any(x in name for x in health_items):
        expense_total[4] += 1
        expense_vtotal[4] += value
        return expense_types[3]

    elif any(x in name for x in shopping_items):
        expense_total[6] += 1
        expense_vtotal[6] += value
        return expense_types[6]

    elif any(x in name for x in interest_items):
        interest_total += 1
        interest_vtotal += value
        return interest_type

    else:
        expense_total[5] += 1
        expense_vtotal[5] += value
        return expense_types[5]


def main():
    global expense_vtotal, expense_total, items_size
    print("start...")



    for file in files:
        rownum = 0
        other_items = set()

        expense_vtotal = [0] * items_size
        expense_total = [0] * items_size

        with open(prefix+file, 'r') as csvfile:
           reader = csv.reader(csvfile, delimiter=',')
           for row in reader:
               rownum += 1

               if rownum == 1:
                   continue

               #print("{}: {}".format(rownum,row))


               name = row[3]
               valueNoSymbol = row[2];

               payment = False
               if valueNoSymbol.find('(') > -1:
                   payment = True

               valueNoSymbol = valueNoSymbol.strip(',$-()"').replace(',', '')

               value = float(valueNoSymbol)
               category = categorize(name, value, payment)
               print("categorizing {} -->  {}".format(name, category))

               if category == expense_types[5]:
                other_items.add(name)



        print ("\n-----------\nResults...")
        itemcount = 0
        for item in expense_types:
            print("Type {}: total count: {}, total amount {}".format(expense_types[itemcount], expense_total[itemcount], expense_vtotal[itemcount]))
            itemcount += 1

        print("UNcategorized items... {}".format(other_items))

        print("Total Expenses: {} \nTotal Payments: {} \nTotal Interest: {}".format(sum(expense_vtotal), payment_vtotal,  interest_vtotal))
        drawBar(expense_types, expense_vtotal)
        drawPie(expense_types, expense_vtotal)

        submitExpenses(expense_vtotal)


        print("\n====================\n")


    drawBar(expense_types, expense_value_overall)
    drawPie(expense_types, expense_value_overall)


if __name__ == "__main__":
    main()
