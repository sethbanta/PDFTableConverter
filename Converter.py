#Author Seth Banta
#https://github.com/sethbanta
import tabula
import csv
import os
import glob

#Function used to convert tables from one pdf
#produces an output.csv file then reads that output.csv and eliminates duplicate columns
#to eliminate duplicate columns it produces a new file called output_clean.csv
def convertFunc(p):
    cleanFileExists = os.path.isfile('output_clean.csv')
    array = ["deez"]
    dupeCount = 0
    tabula.convert_into(pdf_path, "output.csv", output_format="csv", pages='all')
    #read in the csv file
    with open('output.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        #begin tracking how many lines we have processed
        line_count = 0
        for row in csv_reader:
            #check if its the first column we are reading, that way we dont perform a search on an empty array
            if line_count == 0:
                array.append(row[0])
                line_count += 1
            else:
                #check if the column exists, this should always be 0 or 1
                columnCount = array.count(row[0])
                #if the column does not exist
                if(columnCount == 0):
                    #add the value to a list of tracked values
                    array.append(row[0])
                    #open out_clean.csv and begin writing to it
                    with open('output_clean.csv', mode='a', newline='') as csv_file:
                        #create a new csv writer to output_clean.csv
                        #this writer is set to append mode so it adds to the end of the file
                        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        #write the current row to the csv file
                        csv_writer.writerow(row)
                else:
                    #right now just counting deez and seeing if it work
                    #eventually this should do nothing
                    dupeCount += array.count("deez")
                line_count += 1
    print(f'Processed {line_count} lines.')
    print(f'Found {dupeCount} duplicate columns')
    if(cleanFileExists):
        print(f'Overwrote output_clean.csv, this will cause confusion if the same data was ran on')
    else:
        print(f'Created output_clean.csv')

#Function used to convert all pdfs in one directory
#this will create a bunch of csv's with the name of the pdf i.e. Submitted_By.pdf -> Submitted_By.pdf.csv
#after creating all of these csv's it will read them back in one by one, check for duplicates within
#outputs any non duplicate rows to output_clean.csv
#The way this works can be confusing
#if an output_clean.csv already exists and the user wishes to continue
#it will append onto the end of the csv, so if you happen to run on the same data twice, the clean output
#will contain the output of both clean outputs, appearing as if it didn't catch duplicates or ran an extra time      
def convertFuncBatch(p):
    cleanFileExists = os.path.isfile('output_clean.csv')
    array = ["deez"]
    dupeCount = 0
    #convert all pdfs within the directory to csvs
    for filepath in glob.glob(p+'\\*.pdf'):
        name = os.path.basename(filepath)
        tabula.convert_into(filepath, name+".csv", output_format="csv", pages='all')
    #for every csv we made, read and write to a clean output file
    for filepath in glob.glob("*.csv"):
        #grab filename
        name = os.path.basename(filepath)
        #place filename into an array as the only value
        #this is so that it can be properly added to the CSV
        #without it being in an array, it kinda freaks out
        nameForCSV = [name]
        #read in the csv file
        with open(name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            #begin tracking how many lines we have processed
            line_count = 0
            with open('output_clean.csv', mode='a', newline='') as csv_file:
                #create a new csv writer to output_clean.csv
                #this writer is set to append mode so it adds to the end of the file
                csv_writer = csv.writer(csv_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(nameForCSV)
            for row in csv_reader:
                #check if its the first column we are reading, that way we dont perform a search on an empty array
                if line_count == 0:
                    array.append(row[0])
                    line_count += 1
                else:
                    #check if the column exists, this should always be 0 or 1
                    columnCount = array.count(row[0])
                    #if the column does not exist
                    if(columnCount == 0):
                        #add the value to a list of tracked values
                        array.append(row[0])
                        #open out_clean.csv and begin writing to it
                        with open('output_clean.csv', mode='a', newline='') as csv_file:
                            #create a new csv writer to output_clean.csv
                            #this writer is set to append mode so it adds to the end of the file
                            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            #write the current row to the csv file
                            csv_writer.writerow(row)
                    else:
                        #does nothing except counts for duplicate columns for clarity
                        dupeCount += array.count("deez")
                    line_count += 1
    print(f'Processed {line_count} lines.')
    print(f'Found {dupeCount} duplicate columns')
    #Clean up excess CSV's
    for filepath in glob.glob("*.csv"):
        name = os.path.basename(filepath)
        if(name != "output_clean.csv"):
            os.remove(name)
    if(cleanFileExists):
        print(f'Overwrote output_clean.csv, this will cause confusion if the same data was ran on')
    else:
        print(f'Created output_clean.csv')

batchQuestion = input('Convert multiple pdfs? (y/n) ')
match batchQuestion:
        case "y":
            pdf_path = input('Please enter the directory of pdfs below\n')
            outputFileExists = os.path.isfile('output_clean.csv')
            if(outputFileExists):
                continueQuestion = input("output_clean.csv already exists, it will be overwritten, would you like to continue? (y/n)\n")
                match continueQuestion:
                    case "y":
                        convertFuncBatch(pdf_path)
                    case _:
                        print(f'Exiting')
            else:
                convertFuncBatch(pdf_path)
        case "n":
            pdf_path = input('Please enter the exact location of pdf below\n')
            outputFileExists = os.path.isfile('output.csv')
            if(outputFileExists):
                continueQuestion = input("output.csv already exists, it will be overwritten, would you like to continue? (y/n)\n")
                match continueQuestion:
                    case "y":
                        convertFunc(pdf_path)
                    case _:
                        print(f'Exiting')
            else:
                convertFunc(pdf_path)
        case _:
            print(f'Exiting')
