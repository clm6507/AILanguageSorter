# AILanguageSorter
Makes decision trees and AdaBoost forests which can predict whether sentences are English or Dutch

To use the language soter, run the LanguageSorter.py file with one of the following commands following it. Running the program without any commands will tell the user to read this file. For training samples of 15 word sentence fragments, the user can either make their own or use the "trainingset1.txt" or the "trainingset2.txt". When predicting, the user can use the "best.model" file or train their own tree/forest. Additionally, the user can either make their own file of 15 word sentence fragments in English or Dutch, or they can use the "testfile.txt". Both the training sets and the test file are made from Wikipedia articles written in English and Dutch.

train <examples> <hypothesisOut> <learning-type> reads in labeled examples and performs training.

    examples: name of a file containing labeled examples. For example- "en|ZETA's failure was due to limited information; using the best available measurements, ZETA was returning", "nl|actie en deelname in het publieke debat. De periode van 2001 tot 2021, zal vier"
    hypothesisOut: the file name to write your model to.
    learning-type: the type of learning algorithm, either "dt" or "ada".

predict <hypothesis> <file> classifies each line as either English or Dutch using the specified model. For each input example, the program simply prints its predicted label on a newline. ("en" for English and "nl" for Dutch)

    hypothesis: trained decision tree or ensemble created by the train program
    file: is a file containing lines of 15 word sentence fragments in either English or Dutch. For example- "de zouten achter in zee, waardoor neerslag geen zout bevat, dit noemt men zoet water."