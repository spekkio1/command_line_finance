
# clf.py --- (basic) command-line finance

# Copyright (C) 2020 Tyler Brown

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Version: 0.11
# Updated for Python 3

# Commentary:

# This is a basic program which enables one to keep track of a series of
# financial accounts. Transactions to single accounts, transfers between
# them, and some basic reporting are available. Transactions can be performed
# interactively at the command line, or with shell commands.

# The transactional data is stored in a tab-delimited text file.

# import io

import os
import csv
import time
import sys

# from pprint import pprint
profile_name = os.environ["USER"]
path = "/home/" + profile_name + "/Documents/money/cli_finance"
os.chdir(path)


# Print out the account that has been selected, nicely.
def print_acct_sel_msg(account, account_dict):
    print("You have selected account " + account + ": " \
        + account_dict[account] + ".")


# Print out the account's balance, nicely.
def print_acct_balance(acct):
    print("The balance of account " + str(acct) + " is " \
        + dollar_fmt(summarize_one(acct)) + ".")


# Return a formatted string with a dollar amount.
def dollar_fmt(num):
    if (num < 0):
        num = -1 * num
        num = '${:,.2f}'.format(num)
        num = '(' + num + ')'
    else:
        num = '${:,.2f}'.format(num)
    return num


# Print the transaction data nicely.
def trans_print(year, month, day, hour, minute, acct_num, acct_name,
                dollars_fmt, desc):
    print(year + '/' + month + '/' + day \
        + '{:.>32}'.format("Acct_" + acct_num + "_" + acct_name) \
        + '{:.>14}'.format(dollars_fmt) \
        + '...' + desc)


# Return the index of the sublist whose first element
# is equal to the given number.
def index2d(lst, given):
    found = False
    for i in list(range(len(lst))):
        if (lst[i][0] == given):
            found = True
            answer = i
            break
    if (found is False):
        answer = "Not found"
    return answer


# Takes a list of lists (essentially a two dimensional array)
# Prints it nicely, tab delimited.
def summ_nice_print(lst):
    for i in list(range(len(lst))):
        dollars = dollar_fmt(lst[i][2])
        print('{:.<5}'.format(str(lst[i][0])) \
            + '{:.>22}'.format(lst[i][1]) + '{:.>14}'.format(dollars))


def summ_grand_total(lst):
    total = 0
    for i in list(range(len(lst))):
        total += lst[i][2]
    return total


def get_accounts():
    # with open('accounts', 'rb') as f:
    with open('accounts', 'r', newline = '') as f:
        acct_file = list(csv.reader(f, delimiter='\t'))
        # Use a dictionary to store the accounts and their names.
        acct_def = {}
        for i in list(range(len(acct_file))):
            # Handle the account definition rows first.
            if (len(acct_file[i]) == 1):
                # acct_file[i] is an account definition.
                # It's a list of one string element;
                # split it into a list of strings.
                x = acct_file[i][0].split()
                # Put it into the dictionary.
                # Substring to remove the colon from the account number string.
                acct_num = x[1][:len(x[1])-1]
                acct_name = x[2]
                acct_def[acct_num] = acct_name
    f.close()
    return acct_def


def get_data(choice, val):
    # with open('transactions', 'rb') as f:
    with open('transactions', 'r', newline = '') as f:
        acct_file = list(csv.reader(f, delimiter='\t'))
        ##########
        #    print(acct_file[1000])
        #    print(acct_file[1000][0]) has the date and time.
        #    print(acct_file[1000][1]) has the account number.
        #    print(acct_file[1000][2]) has the dollar amount;
        #        credits > 0, debits < 0.
        #    print(acct_file[1000][3]) has the description.
        ##########
        #    for i in list(range(len(acct_file))):
        #        lengths.append(len(acct_file[i]))
        #    print(set(lengths))
        ##########
        acct_def = get_accounts()
        # parse the 'val' list
        wanted_acct_num = val[0]
        wanted_dollars = val[1]
        # process the data
        for i in list(range(len(acct_file))):
            # Handle the rows with transaction data.
            if (len(acct_file[i]) == 4):
                # assign date and time
                datetime = acct_file[i][0]
                year = datetime[:4]
                month = datetime[4:6]
                day = datetime[6:8]
                hour = datetime[8:10]
                minute = datetime[10:12]
                # assign account number and name
                acct_num = acct_file[i][1]
                acct_name = acct_def[acct_num]
                # assign dollars
                dollars = float(acct_file[i][2])
                # assign description
                desc = acct_file[i][3]
                # Assemble it and print it out.
                ##########
                # If opt = option = 'a' then they want to pull data
                # for an account number.
                # output = []
                if (choice == 'qa'):
                    # If the line of data has the account value we want,
                    # then print it.
                    if (acct_num == wanted_acct_num):
                        trans_print(year, month, day, hour, minute, acct_num,
                                    acct_name, dollar_fmt(dollars), desc)
                # If opt = option = 'd' then they want to pull data
                # for a dollar amount.
                elif (choice == 'qd'):
                    # If the line of data has the dollar amount we want,
                    # then print it.
                    if (abs(dollars) == wanted_dollars):
                        trans_print(year, month, day, hour, minute, acct_num,
                                    acct_name, dollar_fmt(dollars), desc)
                elif (choice == 'qad'):
                    if (acct_num == wanted_acct_num and abs(dollars) == wanted_dollars):
                        trans_print(year, month, day, hour, minute, acct_num,
                                    acct_name, dollar_fmt(dollars), desc)
                # If opt is something other than 'a' or 'd',
                # then output error message.
                else:
                    print("Error: valid option not given")
    f.close()

# function should read in the entire contents of the transactions file.
# On each line, we want the account number, the account name,
# and the total of its dollars.
# The intention is to give a total balance for each account
# in a compact manner.
def summarize():
    # with open('transactions', 'rb') as f:
    with open('transactions', 'r', newline = '') as f:
        acct_file = list(csv.reader(f, delimiter='\t'))
        acct_def = get_accounts()
        # store dictionary in list of lists.
        # this will be like a 2-d array.
        # element 1 of each sublist: account number
        # element 2 of each sublist: account name
        # element 3 of each sublist: total dollars for that account
        #     (initially set to zero)
        summ_list = []
        for i in list(range(len(acct_def))):
            list_to_add = []
            single_key = list(acct_def.keys())[i]
            # first element of sublist
            list_to_add.append(int(single_key))
            # second element of sublist
            list_to_add.append(acct_def[single_key])
            # third element of sublist
            list_to_add.append(0)
            # append sublist to the list of lists
            summ_list.append(list_to_add)
        # sort the stored dictionary
        summ_list.sort()
        # for each line of transaction data
        # find the summary array sublist index
        # which matches the account number on this row
        # increment its third element by the dollars on this row
        for i in list(range(len(acct_file))):
            if (len(acct_file[i]) == 4):
                # assign account number
                acct_num = int(acct_file[i][1])
                # assign dollars
                dollars = float(acct_file[i][2])
                sublist_to_edit = index2d(summ_list, acct_num)
                summ_list[sublist_to_edit][2] += dollars
        for i in list(range(len(summ_list))):
            summ_list[i][2] = round(summ_list[i][2], 2)
        print("SUMMARY OF TRANSACTIONS")
        summ_nice_print(summ_list)
        print("The grand total is: " + dollar_fmt(summ_grand_total(summ_list)))
#        pprint(summ_list)
    f.close()


# function should read in the entire contents of the transactions file.
# On each line, we want the account number, the account name,
# and the total of its dollars.
# The intention is to give a total balance
# for each account in a compact manner.
def summarize_one(wanted_acct):
    # with open('transactions', 'rb') as f:
    with open('transactions', 'r', newline = '') as f:
        acct_file = list(csv.reader(f, delimiter='\t'))
        total = 0
        # for each line of transaction data
        # if the row doesn't pertain to the wanted account,
        # ignore it and move on.
        # if the row does pertain, add its dollar amount to the total.
        for i in list(range(len(acct_file))):
            # assign account number
            acct_num = int(acct_file[i][1])
            if (acct_num == int(wanted_acct)):
                # assign dollars
                dollars = float(acct_file[i][2])
                total += dollars
        wanted_value = round(total, 2)
    f.close()
    return wanted_value


def debit(acct_to_debit, amt_to_debit, desc):
    # write this: yyyymmddhhmm + '\t' + acct_to_debit + '\t'
    #     + -(amt_to_debit) + '\t' + desc
    current_date_time = time.strftime("%Y%m%d%H%M")
    # debits need to be negative, as they are subtracting
    # from the account balance.
    amt_to_debit_formatted = -1 * amt_to_debit
    # open file & append to it (using w would overwrite the entire file)
    # with open('transactions', mode='ab') as f:
    with open('transactions', mode='a', newline = '') as f:
        acct_file = csv.writer(f, delimiter='\t')
        acct_file.writerow([current_date_time, acct_to_debit,
                            amt_to_debit_formatted, desc])
    f.close()


def credit(acct_to_credit, amount_to_credit, desc):
    # write this: yyyymmddhhmm + '\t' + acct_to_credit + '\t'
    #     + -(amount_to_credit) + '\t' + desc
    current_date_time = time.strftime("%Y%m%d%H%M")
    # open file & append to it (using w would overwrite the entire file)
    # with open('transactions', mode='ab') as f:
    with open('transactions', mode='a', newline = '') as f:
        acct_file = csv.writer(f, delimiter='\t')
        acct_file.writerow([current_date_time, acct_to_credit,
                            amount_to_credit, desc])
    f.close()


def transfer(account_to_transfer_from, account_to_transfer_to,
             amount_to_transfer, desc):
    # write this: yyyymmddhhmm + '\t' + acct_to_credit + '\t'
    #     + -(amount_to_credit) + '\t' + desc
    # current_date_time = time.strftime("%Y%m%d%H%M")
    desc_for_debit = "Transfer from account #" \
        + str(account_to_transfer_from) + ": " + desc
    desc_for_credit = "Transfer to account #" + \
        str(account_to_transfer_to) + ": " + desc
    # use debit function
    debit(account_to_transfer_from, amount_to_transfer, desc_for_debit)
    # use credit function
    credit(account_to_transfer_to, amount_to_transfer, desc_for_credit)


def create_new_account(number, name):
    # with open('accounts', mode='ab') as f:
    with open('accounts', mode='a', newline = '') as f:
        acct_file = csv.writer(f, delimiter='\t')
        new_row = "ACCOUNT " + number + ": " + name
        acct_file.writerow([new_row])
    f.close()


def menu(q):
    acct_def = get_accounts()
    ch = input("\nEnter input choice:  \n"
                   + "(d) Make a debit \n"
                   + "(c) Make a credit \n"
                   + "(t) Make a transfer \n"
                   + "(s) Summarize transaction data \n"
                   # + "(r) Show recent transactions (last 30 days)"
                   + "(qa) Query transaction data by account number \n"
                   + "(qd) Query transaction data by dollar amount \n"
                   + "(qad) Query transaction data by account and dollar \n"
                   + "(cna) Create a new account \n"
                   + "(q) Quit \n"
                   + "> ")
    if (ch == 'qa'):
        val = []
        val.append(input('Enter the account number: '))
        val.append(None) # zero dollars
        get_data(ch, val)
    elif (ch == 'qd'):
        val = []
        val.append(None) # null account
        val.append(float(input('Enter the dollar amount with no dollar sign: ')))
        get_data(ch, val)
        # print(str(val) + " as data type float is " + str(val_float))
    elif (ch == 'qad'):
        val = []
        val.append(input('Enter the account number: '))
        val.append(float(input('Enter the dollar amount with no dollar sign: ')))
        get_data(ch, val)
    elif (ch == 's'):
        summarize()
    # elif (ch == 'r'):
        # print_trans_recent(30)    
    elif (ch == 'd'):
        acct_to_debit = input("Enter account which you want to debit: ")
        print_acct_sel_msg(acct_to_debit, acct_def)
        amt_to_debit = float(input("Enter the amount to debit: "))
        desc_for_debit = input("Enter a description for the debit: ")
        debit(acct_to_debit, amt_to_debit, desc_for_debit)
        print_acct_balance(acct_to_debit)
    elif (ch == 'c'):
        acct_to_credit = input("Enter account which you want to credit: ")
        print_acct_sel_msg(acct_to_credit, acct_def)
        amount_to_credit = float(input("Enter the amount to credit: "))
        desc_for_credit = input("Enter a description for the credit: ")
        credit(acct_to_credit, amount_to_credit, desc_for_credit)
        print_acct_balance(acct_to_credit)
    elif (ch == 't'):
        acct_to_xfer_from = input("Enter account "
                                      + "which you want to transfer FROM: ")
        print_acct_sel_msg(acct_to_xfer_from, acct_def)
        acct_to_xfer_to = input("Enter account "
                                    + "which you want to transfer TO: ")
        print_acct_sel_msg(acct_to_xfer_to, acct_def)
        amt_to_xfer = float(input("Enter the amount to transfer: "))
        desc_for_xfer = input("Enter a description for the transfer: ")
        print("Before transfer, \taccount " + str(acct_to_xfer_from) \
            + " balance = " + dollar_fmt(summarize_one(acct_to_xfer_from)) \
            + "\t & account " + str(acct_to_xfer_to) + " balance = " \
            + dollar_fmt(summarize_one(acct_to_xfer_to)) + ".")
        transfer(acct_to_xfer_from, acct_to_xfer_to, amt_to_xfer,
                 desc_for_xfer)
        print("After transfer, \taccount " + str(acct_to_xfer_from) \
            + " balance = " + dollar_fmt(summarize_one(acct_to_xfer_from)) \
            + "\t & account " + str(acct_to_xfer_to) + " balance = " \
            + dollar_fmt(summarize_one(acct_to_xfer_to)) + ".")
    elif (ch == 'cna'):
        new_account_number = input("Enter new account number: ")
        # print(type(new_account_number))
        # while (type(new_account_number) != int):
        # print("You must enter a positive whole number.")
        # new_account_number = input("Enter new account number: ")
        new_account_name = input("Enter new account name: ")
        # print(type(new_account_number))
        # while (type(new_account_name) != str):
        # print("You must enter an alphabetical name.")
        # new_account_name = input("Enter new account name: ")
        create_new_account(new_account_number, new_account_name)
    elif (ch == 'q'):
        print("Bye!")
    # experimental
    # elif (ch == 'tf'):
        # write_tf()
    return ch


##########################################################################
# MAIN

# if there were no extra arguments passed when the script was run,
# we'll use the menu interface.
if (len(sys.argv) == 1):
    ch = str()
    while (ch != 'q'):
        ch = menu(ch)
        # I'd like to make it so I can abort the menu choice I have made
        # and return to the menu, without having to crash the program
        # (by entering a string where a number should be)
        # and start it over again.
        
# otherwise, we'll NOT use the menu interface,
# but only use the parameters passed from the shell
# to do the desired tasks.
# sys.argv[0] is the script name
# sys.argv[1] is the first argument ... and so on.
# At this time, I'm only writing a basic functionality for this,
# so I can easily interface a LibreOffice spreadsheet
# of mine with this program.
# Hence, I need nothing more than the ability to make credits
# without using the menu interface.
else:
    if (sys.argv[1] == 'c'):
        acct = sys.argv[2]
        amt = sys.argv[3]
        desc = sys.argv[4]
        credit(acct, amt, desc)
    elif (sys.argv[1] == 't'):
        acct_to_xfer_from = sys.argv[2]
        acct_to_xfer_to = sys.argv[3]
        amt_to_xfer = float(sys.argv[4])
        desc_for_xfer = sys.argv[5]
        transfer(acct_to_xfer_from, acct_to_xfer_to, amt_to_xfer,
                 desc_for_xfer)
    else:
        print("Invalid entry.")

