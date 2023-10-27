from django.shortcuts import render
# import openpyxl
import pandas as pd
import random

from django.http import HttpResponse

def index(request):
    if "GET" == request.method:
        return render(request, 'myapp/index.html', {"success":False})
    else:

        resultDf = randomizer(request)

        # Save the shuffled data to a new Excel file
        output_excel_file = "shuffled_excel_file.xlsx"
        resultDf.to_excel(output_excel_file, index=False)
        
        return render(request, 'myapp/index.html', {"success":True})

def randomizer(request):
    excel_file = request.FILES["excel_file"]
    df = pd.read_excel(excel_file)
        # you may put validations here to check extension or file size

    polling_booths = []
    employees = []
    for i, row in df.iterrows():
        polling_booths.append({"booth_name": row[df.columns[0]], "city": row[df.columns[1]]})
        employees.append({"employee_name": row[df.columns[2]],"contact":row[df.columns[3]], "city": row[df.columns[4]]})
    

    # Create a list to store the allocations
    allocations = []

    # Shuffle the order of polling booths and employees to randomize the allocation
    random.shuffle(polling_booths)
    random.shuffle(employees)
    randomizing = 1
    print("Randomization Count: "+ str(randomizing))
    # Iterate through polling booths and employees to make allocations
    for booth in polling_booths:
        for employee in employees:
            if booth["city"] != employee["city"]:
                # Allocate the booth to the employee
                allocation = {df.columns[0]:booth["booth_name"], df.columns[1]:booth["city"], df.columns[2]:employee["employee_name"], df.columns[3]:employee["contact"], df.columns[4]: employee["city"]}
                # allocation = {"employee_name": employee["employee_name"], "booth_name": booth["booth_name"]}
                allocations.append(allocation)
                # Remove the allocated employee to avoid double allocation
                employees.remove(employee)
                break  # Move to the next booth
    
    if (len(allocations) != len(df)):
        randomizing +=1
        print("Randomization Count: "+ str(randomizing))
        randomizer(request)
    # Print the allocations
    for allocation in allocations:
        print(f"Allocated {allocation[df.columns[0]]} to {allocation[df.columns[2]]}")

    resultDf = pd.DataFrame(allocations)

    return resultDf


def export_excel_file(request):
    df = pd.read_excel("shuffled_excel_file.xlsx")
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=shuffled_excel_file.xlsx'
    df.to_excel(response, index=False)
    
    return response




def export_excel_file_template(request):
    df = pd.read_excel("template.xlsx")
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=template.xlsx'
    df.to_excel(response, index=False)
    
    return response