# Author: Ivan Klus
# Date: October 12, 2014
# Version: 3.01
# Systems Supported: Linux and Mac
"""This Python Program finds a word's social network, which consists of
all of it's friend, all of it's friends of friends, and all of it's
friends of friends of friends, from the word list entered. Two words
are friends if they have a Levenshtein distance of 1, meaning that you
can add, remove, or substitute exactly one letter in the first word to 
create the second word. The program takes in a word and file name on the
command line or by raw_input, and will output the word's social network 
to the terminal, or write all the words in its social network to a file. The
social network of a word includes itself and each word that is a friend,
friend of friend, or friend of friend of friend once. Additionally, when
printing to the terminal, each sections shows the new words found in each
iteration, so Friends of Friends: only shows the new words added to the social
network that were friends of friends, not all of the words that were friends of
the word's friends.  Also, the timing of the code will not work on Windows.
"""

import sys
from time import time

class SocialNetwork(object):
    def __init__(self, word, wordList):
        self.word = word
        self.wordList = wordList    # Stores the list of possible friends
                                    #   grouped by length in a dictonary.
        self.network = [self.word]  # Stores all of the words in the social 
                                    #   network starting with the word.
        self.friends = []   # Stores all the friends.
        self.friendsOf2 = []    # Stores all the friends of friends.
        self.friendsOf3 = []    # Stores all the friends of friends of friends.

    """Takes in a list of words and finds all of the friends for each word in
    the list and returns a list comprised of all of the found friends that are not
    already a part of the network.
    """
    def findFriends(self, toBeSearched):
        friendList = []
        for line in toBeSearched:
            length = len(line)
            # Checks if words of the same length are friends.
            if length in self.wordList:
                for word in self.wordList[length]:
                    diffLetters = 0
                    for index, letter in enumerate(word):
                        if letter != line[index]:
                            diffLetters += 1
                        if diffLetters == 2:
                            break
                    else:
                        if word not in self.network: friendList.append(word)
            # Checks if words that are one letter fewer are friends.
            if (length-1) in self.wordList:
                for word in self.wordList[length-1]:
                    diffLetters = 0
                    index2 = 0
                    tempWord = word + '_' # Makes words the same length.
                    for index1 in range(length):
                        if line[index1] != tempWord[index2]:
                            diffLetters += 1
                            index2 -= 1
                        if diffLetters == 2:
                            break
                        index2 += 1
                    else:
                        if word not in self.network: friendList.append(word)
            # Checks if words that are one letter longer are friends.
            if (length+1) in self.wordList:
                for word in self.wordList[length+1]:
                    diffLetters = 0
                    index2 = 0
                    tempLine = line + '_' # Makes words the same length.
                    for index1 in range(length+1):
                        if word[index1] != tempLine[index2]:
                            diffLetters += 1
                            index2 -= 1
                        if diffLetters == 2:
                            break
                        index2 += 1
                    else:
                        if word not in self.network: friendList.append(word)
        return friendList

    """Finds friends, friends of friends, and friend of friend of friends. Also,
    removes any duplicates from theses lists.
    """
    def findNetwork(self):
        # Sets friends to the word's friends and adds it to the network.
        self.friends = list(set(self.findFriends([self.word])))
        self.network += self.friends
        # Finds friends of friends and removes previous friends from list.
        self.friendsOf2 = list(set(self.findFriends(self.friends)))
        # Adds friends of friends to network.
        self.network += self.friendsOf2
        # Finds friends of friendsOf2 and removes previous friends from list.
        self.friendsOf3 = list(set(self.findFriends(self.friendsOf2)))
        # Adds friends of friends of friends to network and removes duplicates.
        self.network = list(set(self.network + self.friendsOf3))     

    """Writes the social network of the word to a file.
    """
    def writeNetworkToFile(self):
        outFileName = self.word + "_SocialNetwork.txt"
        outFile = open(outFileName,'a')
        outFile.write("The Social Network for %s is:\n" % self.word)
        for line in sorted(self.network):    
            outFile.write(line + "\n")
        outFile.close()
        
    """Says how the SocialNetwork class should be represented.
    """
    def __repr__(self):
        col = 10   # Sets the number of columns to print the results in.
        outStr = "The Social Network for %s consists of:\n" % self.word
        outStr += "Friends:\n"
        for count, line in enumerate(sorted(self.friends)):    
            outStr += (line + "\t")
            if (count+1)%col == 0 and count is not len(self.friends):
                outStr += "\n"
        outStr += "\n \nFriends of Friends: \n"
        for count, line in enumerate(sorted(self.friendsOf2)):    
            outStr += (line + "\t")
            if (count+1)%col == 0:
                outStr += "\n"
        outStr += "\n \nFriends of Friends of Friends: \n"
        for count, line in enumerate(sorted(self.friendsOf3)):    
            outStr += (line + "\t")
            if (count+1)%col == 0:
                outStr += "\n"
        return outStr


"""Takes in the name of a file and returns a dict with keys that are the
lenght of the words in the array that is the value.
"""
def fileToDict(inFileName):
    inFile = open(inFileName,"r")
    wordList = {}
    for line in inFile:
        length = len(line) - 1
        if length > 0:
            if length not in wordList:
               wordList[length] = []
            wordList[length].append(line[0:length])
    inFile.close()
    return wordList


"""Defines a main() function that finds a word's Social Network
"""
def main():
    # Gets the word and file name from the command line.
    word = ""
    fileName = ""
    if len(sys.argv) >= 2:
        word = sys.argv[1]
        fileName = sys.argv[2]
    # Checks if a word and file name were entered on command line.
    if word is "" or fileName is "":
        print "No word or file name was entered\n" \
        "Please enter the word and then the file name of the wordlist\n" \
        "on command line after social_network.py."
        # Asks if the user wants to enter them now, if nothing was entered.
        choice = raw_input("Or would you like to enter them now? (y/n): ")
        while True:
            if choice.lower() == "y":
                word = raw_input ("Word: ")
                fileName = raw_input ("File Name: ")
                break
            elif choice.lower() == "n":
                return
            else:
                choice = raw_input ('Sorry, please enter "y" or "n": ')
    # Finds start time.
    t_start = time()
    # Creates a SocialNetwork class for the word and turns the file to a dict.
    wordList = fileToDict(fileName)
    sNetwork = SocialNetwork(word, wordList)
    # Finds the Social Network of the word enterered.
    sNetwork.findNetwork()
    # Finds stop time and prints time elapsed.
    t_stop = time()
    print "Time elapled: %f " % (t_stop - t_start)
    # Allows the user to choose what type of output for the words social network.
    print "How would you like %s's Social Network to be outputted?" % word
    menu = raw_input("Enter 1 for print to terminal, 2 for write to file, " \
    "3 for both, or anything else for no action: ")
    if menu == '1': print sNetwork
    elif menu == '2': sNetwork.writeNetworkToFile()
    elif menu == '3':
        print sNetwork
        sNetwork.writeNetworkToFile()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
