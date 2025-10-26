import math
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

def EMI(LoanAmount, Rate, Months):
    Rate = Rate / (12 * 100)  
    EMI = (LoanAmount * Rate * math.pow(1 + Rate, Months)) / (math.pow(1 + Rate, Months) - 1)
    EMI = round(EMI, 2)
    return EMI

def FD_Returns_Per_Month(LoanAmount, Rate, Months):
    n = 1  
    t = Months / 12
    Rate = Rate/12*Months
    FD_Matured_Value = LoanAmount * math.pow(1 + (Rate / 100) / n, n * t)
    MonthlyMaturedValue = round(FD_Matured_Value / Months, 2)
    return MonthlyMaturedValue

def calculate_emi_and_fd(Loan_Amount, Loan_Rate, FD_Rate, Loan_Tenure_Months):
    emi = EMI(Loan_Amount, Loan_Rate, Loan_Tenure_Months)
    fd_return = FD_Returns_Per_Month(Loan_Amount, FD_Rate, Loan_Tenure_Months)
    total_emi_paid = round(emi * Loan_Tenure_Months,2)
    total_fd_return = round(fd_return * Loan_Tenure_Months,2)
    return Loan_Amount,Loan_Tenure_Months,emi, fd_return,total_emi_paid, total_fd_return


if __name__ == "__main__":

    Loan_Amount = 48_78_300
    Loan_Rate = 9.5
    FD_Rate = 6.6
    #Loan_Tenure_Months = 24

    Matrix = list()


    Loan_Tenure_Months = [i for i in range(6, 20*12+1, 6)]

    with ThreadPoolExecutor(max_workers=len(Loan_Tenure_Months)) as executor:
        futures=[executor.submit(calculate_emi_and_fd, Loan_Amount, Loan_Rate, FD_Rate, months) for months in Loan_Tenure_Months]

        for future in as_completed(futures):
            LA, months, emi, fd_return, total_emi_paid, total_fd_return = future.result()
            print(LA, months, emi, fd_return, total_emi_paid, total_fd_return)
            Matrix.append([LA, months, emi, fd_return, total_emi_paid, total_fd_return])
    
    Matrix.sort(key=lambda row: row[1])

    with open('loan_fd_analysis.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Loan Amount', 'Loan Tenure (Months)', 'EMI', 'FD Returns per Month', 'Total EMI Paid', 'Total FD Returns'])
        writer.writerows(Matrix)
    
    del Matrix

    print("Data written to loan_fd_analysis.csv")
