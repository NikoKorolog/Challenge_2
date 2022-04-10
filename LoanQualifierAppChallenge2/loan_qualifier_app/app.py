# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
import sys
import csv
import fire
import questionary
from pathlib import Path

from qualifier.utils.fileio import load_csv
from qualifier.utils.fileio import save_csv #I added my save csv function to the fileio file

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size         #this is pre-written
from qualifier.filters.credit_score import filter_credit_score           #this is pre-written
from qualifier.filters.debt_to_income import filter_debt_to_income       #this is pre-written
from qualifier.filters.loan_to_value import filter_loan_to_value         #this is pre-written


def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.


    Returns:
        The bank data from the data rate sheet CSV file.
    """
    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")

    return load_csv(csvpath)


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered

#this function takes a path and a data file and saves it as a csv THIS CODE GOES INTO qualifier.utils.fileio
'''
def save_csv(path, data):
    csvpath = Path(path)            #
    with open(csvpath, 'w', newline='') as csvfile:                                              
        csvwriter = csv.writer(csvfile)        
        for row in data:                       
            csvwriter.writerow(row.values())
    return data 
'''           

#this code saves qualifying loans
def save_qualifying_loans(qualifying_loans):
    confirm_save = questionary.confirm("would you like to save your qualifying loans").ask()
    if confirm_save == True:
        qualifying_loans_path = questionary.text("where would you like to save the qualifying loans?").ask()
        save_csv(qualifying_loans_path, qualifying_loans)
    return qualifying_loans   

    """Saves the qualifying loans to a CSV file.
    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    # @TODO: Complete the usability dialog for savings the CSV Files.
    # YOUR CODE HERE!


def run():
    """The main function for running the script."""

    # Load the latest Bank data                                                     #as of 3:09 april 9 this works
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()    #as of 3:09 april 9 this also works
 
    # Find qualifying loans                                                       #as of 3:09 april 9 this is where problems start
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans                                                       #as of 3:09 april 9 not sure if this works
    save_qualifying_loans(qualifying_loans)


if __name__ == "__main__":
    fire.Fire(run)
