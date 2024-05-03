import csv
import re
import pdfplumber
import ipdb
from datetime import datetime

def extract_transactions_from_pdf(pdf_path):
    transactions = []
#    csv_path = "/Users/georgesnow/apple_card_transactions.csv"
#    with open(csv_path, 'w', newline='') as csvfile:
#        fieldnames = ['Date', 'Description', 'Amount']
#        
#        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#        writer.writeheader()
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
#            ipdb.set_trace()
            # Assuming transactions start with "Transactions" and end with "Total"
#            transaction_blocks = text.split("Transactions by")[1:-1]
            transaction_blocks = text.split("\n")
#            ipdb.set_trace()
#            transaction_details = {}
            for block in transaction_blocks:
#                lines = block.split("\n")
                transaction_details = {}
#                ipdb.set_trace()
#                for line in lines:
#                   print(lines)
#                improved => regex "(\d{1,2}\/\d{1,2}\/\d{2,4})(.*)(\d+\%) (\$\d+\.\d+)"
#                captures the cashback percentage and ignores space between it and amount

                pattern = r"(\d{1,2}\/\d{1,2}\/\d{2,4})(.*)(\$\d+\.\d*)"
#                   transaction_details = {}

                matches = re.findall(pattern, block)
                if "Daily Cash Adjustment" in block:
#                   ipdb.set_trace()
                   patternCashback = r"(.+)(-\d+\%.)(\$\d+\.\d+)"
                   cb_matches = re.findall(patternCashback, block)
#                   ipdb.set_trace()
                   transaction_details["Date"] = transactions[-1]['Date']
                   transaction_details["Description"] = cb_matches[0][0]
                   transaction_details["Original Description"] = cb_matches[0][0]
                   transaction_details["Amount"] = cb_matches[0][2]
                   transaction_details["Transaction Type"] = "debit"
#                   ipdb.set_trace()
                   transactions.append(transaction_details)
                   continue
                if len(matches) > 0:
#                       continue
#                       ipdb.set_trace()
#                       transaction_details["Date"] = [matches[0]]

#                       transaction_details["Description"] = [matches[1]]
#                       transaction_details["Amount"] = [matches[2]]
#                       transactions.append(transaction_details)                    
                       for match in matches:
                          print("Date:", match[0])
                          print("Description:", match[1])
##                       print("Daily Cash Amount:", match[3])
                          print("Amount:", match[2])
#                       print()
#                          ipdb.set_trace()
                          payments = ["payment", "transfer"]
                          returns = ["RETURN"]
                          if not any(x in match[1] for x in payments):
#                            continue
#                            ipdb.set_trace()

                            transaction_details["Date"] = match[0]

                            transaction_details["Description"] = match[1]
                            transaction_details["Original Description"] = match[1]
                            transaction_details["Amount"] = match[2]
                            if any(x in match[1] for x in returns):
                                transaction_details["Transaction Type"] = "credit"
                            else:
                                transaction_details["Transaction Type"] = "debit"
                            transactions.append(transaction_details)
#                          ipdb.set_trace()
                   
#                       transactions.append(transaction_details)


#                writer.writerow(transaction_details)
#                transactions.append(transaction_details)
                print(transactions)
    return transactions

def save_to_csv(transactions, csv_path):
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Description', 'Original Description', 'Amount', 'Transaction Type']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for transaction in transactions:
#            print(transaction)
            writer.writerow(transaction)

if __name__ == "__main__":
    pdf_path = "/path/to/applecard-pdf-path.pdf"
    csv_path = "/path/to/where_apple_card_transactions_csv_should_go.csv"

    transactions = extract_transactions_from_pdf(pdf_path)
#    ipdb.set_trace()
    save_to_csv(transactions, csv_path)

    print("CSV creation worked!")

