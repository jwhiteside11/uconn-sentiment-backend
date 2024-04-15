from scoring import score_CSV
from HTMLtoCSV import extract_data
import sys, os

if __name__ == "__main__":
    option = sys.argv[1]
    args = sys.argv[2:]

    if option == "HTMLtoCSV":
        inputdir = args[0]
        outputdir = args[1]

        for input in os.listdir(inputdir):
            extract_data(inputdir + '/' + input, outputdir + '/' + input.split(".")[0] + ".csv")