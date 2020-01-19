import pandas as pd
import re
import tools

# FILENAME = "tests/test1.txt"
# FILENAME = "tests/test2.txt"
FILENAME = "tests/test3.txt"

CSV_FILE = "data/stems.csv"


def clear_file(filename):
    open(filename, 'w').close()


def print_table(filename):
    column_names = ["word", "stem", "inflection", "steps_taken", "part_of_speech"]
    df = pd.read_csv(filename, sep=",", names=column_names)

    print(df)


def diff(string1, string2):
    if len(string1) > len(string2):
        res = ''.join(string1.split(string2))  # get diff
    else:
        res = ''.join(string1.split(string2))  # get diff

    return res.strip()


def write_to_csv(filename, line):
    f = open(filename, "a")
    f.write(line + "\n")

    f.close()


def read_from_file(filename):
    content = ""
    f = open(filename, "r")

    if f.mode == 'r':
        content = f.read()
    else:
        print("No file found!")

    f.close()
    return content


def lowercase(word_list):
    word_list = [element.lower() for element in word_list]

    return word_list


def tokenize(arg):
    tokens = re.findall(r"[\w']+", arg)
    tokens = lowercase(tokens)

    return tokens


def main():
    content = read_from_file(FILENAME)
    tokens = tokenize(content)

    # user_input = input("Stem: ")
    # tokens = tokenize(user_input)

    stemmer = tools.PorterStemmer()

    for token in tokens:
        if len(token) > 2:
            stemmer.clear()
            stemmer.word = token

            # get the stem
            stem = stemmer.stem()
            stem = "".join(stem)

            # choose diff output
            if len(diff(token, stem)) > 0:
                difference = "-" + diff(token, stem)
            else:
                difference = "None"

            # line to write to the csv file
            line = token + "," + stem + "," + difference + "," + str(len(stemmer.steps)) + "," + stemmer.part_of_speech

            # write to the csv file
            write_to_csv(CSV_FILE, line)
        else:
            line = token + "," + token + ",None,None,Not available"
            write_to_csv(CSV_FILE, line)

    print("_______________________________________________________________")
    print_table(CSV_FILE)
    clear_file(CSV_FILE)


if __name__ == '__main__':
    main()
