#This Python script is licensed under the MIT License.
#Copyright (c) 2023 Semantic Science
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import data_sniper
import csv
import os
import datetime

#lets test data sniper
csv_filename = 'deidentify_intents.csv'

fieldnames = ['date','transcription','intent']

with open(csv_filename, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='|')
    writer.writeheader()


# Open the CSV file for reading
with open('input.csv', 'r') as csvfile:
    # Create a CSV reader object
    reader = csv.reader(csvfile, delimiter='|')
    # Skip the header row if it exists
    next(reader, None)
    # Loop through each row in the CSV file
    for row in reader:
        # Read the second field in each row (change the index if you need a different field)
        text = row[2]
        
        result = data_sniper.deid_data(text)
        data = {'date': datetime.datetime.now(), 'transcription': result}
        with open(csv_filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='|')
            writer.writerow(data)
        break