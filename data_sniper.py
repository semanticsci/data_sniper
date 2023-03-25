#This Python script is licensed under the MIT License.
#Copyright (c) 2023 Semantic Science
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from presidio_analyzer import Pattern
from presidio_analyzer import PatternRecognizer
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_anonymizer import AnonymizerEngine


#This function takes inputStr as a parameter and returns de-identified string back
def deid_data(inputStr):
    # Set up the engine, loads the NLP module (spaCy model by default) 
    # and other PII recognizers
    analyzer = AnalyzerEngine()

    # Call analyzer to get results
    results = analyzer.analyze(text=inputStr,
                            entities=["PHONE_NUMBER", "CREDIT_CARD", "DATE_TIME", "EMAIL_ADDRESS", "NRP", "LOCATION", "PERSON", "MEDICAL_LICENSE", "US_BANK_NUMBER", "US_DRIVER_LICENSE", "US_ITIN", "US_PASSPORT", "US_SSN"],
                            language='en')

    # Analyzer results are passed to the AnonymizerEngine for anonymization
    anonymizer = AnonymizerEngine()
    anonymized_text = anonymizer.anonymize(text=inputStr,analyzer_results=results)

    # Define the regex pattern in a Presidio `Pattern` object:
    numbers_pattern = Pattern(name="numbers_pattern",regex="\d+", score = 0.5)

    # Define the recognizer with one or more patterns
    number_recognizer = PatternRecognizer(supported_entity="NUMBER", patterns = [numbers_pattern])
    
    numbers_result = number_recognizer.analyze(text=anonymized_text.text, entities=["NUMBER"])
    
    anonymizer = AnonymizerEngine()
    anonymized_text_final = anonymizer.anonymize(text=anonymized_text.text,analyzer_results=numbers_result)
    
    return anonymized_text_final.text