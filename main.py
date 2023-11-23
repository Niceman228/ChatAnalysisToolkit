import os
from bs4 import BeautifulSoup

flag = False

# Get the current directory path
current_directory = os.getcwd()

# Get the list of files in the current directory
files = os.listdir(current_directory)

# Find the folder containing 'Chat' in its name
for i in files:
    if str(i).count('Chat') == 1:
        chat_directory = current_directory + '/' + i
        flag = True

# Check if 'Chat' directory exists, if not, print a message and exit
if flag != True:
    print('There is no chat folder in this directory')
    exit()

messages = ''

# Function to create a vocabulary of values and their counts
def vocab_of_values(list_of_values):
    temp_vocab = {}
    set_list = list(set(list_of_values))
    for item in set_list:
        temp_vocab[item] = 0

    for item in list_of_values:
        temp_vocab[item] = temp_vocab[item] + 1

    return temp_vocab

# Function to merge two vocabularies
def vocab_mult(temp_vocab, vocab):
    for item in temp_vocab:
        if item in vocab:
            vocab[item] = vocab[item] + temp_vocab[item]
        else:
            vocab[item] = temp_vocab[item]
    return vocab

vocab_of_words = {}
vocab_of_times = {}

# Get files from the 'Chat' directory
files = os.listdir(chat_directory)
for file in files:
    words = []
    times = []
    if file.count('messages') != 0:
        # Open 'messages.html' file and read its content
        with open(chat_directory + '/' + str(file), 'r', encoding='utf-8') as file:
            messages = file.read()

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(messages, 'html.parser')

        # Extract text messages and times from HTML
        for message in soup.find_all('div', class_='text'):
            message = message.text.lower().strip().replace(',', '').replace('.','').replace('?', '').replace('!', '')
            words += message.split()

        for time in soup.find_all('div', class_='pull_right date details'):
            time = time.text[1:6]
            times.append(time)

        # Update vocabularies with words and times
        vocab_of_words = vocab_mult(vocab_of_words, vocab_of_values(words))
        vocab_of_times = vocab_mult(vocab_of_times, vocab_of_values(times))

        print('Read data from the file' + str(file.name))

# Function to write statistics to a file
def end_of_num(temp_list, name_file):
    # Sort the dictionary by values in descending order
    sorted_data = sorted(temp_list.items(), key=lambda x: x[1], reverse=True)

    # Write data to a file
    with open(name_file, 'w') as file:
        for item in sorted_data:
            file.write(f"{item[0]}: {item[1]}\n")
    print('Statistics are written to' + str(name_file))

# Write vocabularies to files
end_of_num(vocab_of_words, 'words.txt')
end_of_num(vocab_of_times, 'times.txt')
