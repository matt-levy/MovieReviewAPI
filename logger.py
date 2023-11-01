from datetime import datetime

# the name of the log file to write to.
log_file = "log-file-" + datetime.today().strftime('%Y-%m-%d') + ".log"


def log(text, log_file=log_file):
    # open up the log file in the correct mode.
    file = open(log_file, 'a')
    # create a string that has the current date and time in the beginning of the text.
    dateAndTime = "[" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "]  "
    # Ensure the string ends with a new line character.
    # append the text to the end of the file.
    file.write(dateAndTime + text + "\r")
    # close the file.
    file.close()
    


def dump(log_file=log_file):
    '''
    This function prints out each line in the log file to the console
    '''
    # open up the log file in the correct mode.
    file = open(log_file, 'r')
    # read the file into a list.
    data = file.read()
    # iterate through each item in the list and print out the results.
    print(data)
    # close the file.
    file.close()

