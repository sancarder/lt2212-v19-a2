import os, sys
import glob
import argparse
import numpy as np
#import pandas as pd
#from sklearn.decomposition import TruncatedSVD
#from sklearn.feature_extraction.text import TfidfTransformer

# gendoc.py -- Don't forget to put a reasonable amount code comments
# in so that we better understand what you're doing when we grade!

# add whatever additional imports you may need here




'''
if args.tfidf:
    print("Applying tf-idf to raw counts.")

if args.svddims:
    print("Truncating matrix to {} dimensions via singular value decomposition.".format(args.svddims))

# THERE ARE SOME ERROR CONDITIONS YOU MAY HAVE TO HANDLE WITH CONTRADICTORY
# PARAMETERS.

print("Writing matrix to {}.".format(args.outputfile))
'''





def load_data(filename):
        
    with open(filename, "r") as myfile:
        lines = myfile.readlines() #read all the lines
        doc = " ".join([a.strip() for a in lines])
    
    #tokenize sentences for document and return them
    #return sent_tokenizer.tokenize(doc)

    #print(doc)
    return doc

def browse_data(folder):
    
    subfolders = os.listdir(folder)
    
    if '.DS_Store' in subfolders:
        sindex = subfolders.index('.DS_Store')
        subfolders.pop(sindex)
    
    #print(subfolders)
    
    #Form of dictionary subfolder_texts: {news:{article1:[hej, hopp], article2:[hopp, hej]}}, {fiction:{article1:[hej, hopp], article2:[hopp, hej]}}
    
    subfolder_texts = {}
        
    for sub in subfolders:
        classtexts = {} # a list of documents
        articles = os.listdir(folder+'/'+sub)
        
        if '.DS_Store' in articles:
            aindex = articles.index('.DS_Store')
            articles.pop(aindex)
        
        #print(articles)
        for art in articles:
            filename = '/'.join([folder, sub, art])
            #print(filename)
            document = load_data(filename)
            processed_document = preprocess(document)
            #print(processed_document)
            classtexts[filename] = processed_document
                           
        #print(classtexts)       
        subfolder_texts[sub] = classtexts
        
        
    #print(subfolder_texts)
    return subfolder_texts


def structure(class_documents):
    
    #Form of class_documents: {news:{article1:[hej, hopp], article2:[hopp, hej]}}, {fiction:{article1:[hej, hopp], article2:[hopp, hej]}}
    
    #Goal: to put all words into one corpus so that you can count the vocab and get the unique words
    #For the vector building you need to keep track of each article again
    
    class_instances = []

    #print(class_documents)
    #print('\n')
        
    #Making instances for each class
    for classlist in class_documents: #list of all document text for a class
        #print(classlist)
        cindex = class_documents.index(classlist)
        class_instance = []
        
        for document in classlist:
            document_instance = (classes[cindex], document)
        
            #print(document_instance)
            #print('\n')
            class_instance.append(document_instance)

        class_instances.append(class_instance)

    #Combines them into one structure by adding them
    corpus = class_instances[0] + class_instances[1]
    
    #print(corpus)
    return corpus


def count_vocab(class_documents):
    #Count the vocabulary for the whole structure by splitting into words and counting them
    #Can this be done smoother? By using count? In that case, transform the corpus into one string?
    #Now this is done for both tuples in the corpus (classes), should it be counted for each? 
    
    #Form of class_documents: {news:{article1:[hej, hopp], article2:[hopp, hej]}}, {fiction:{article1:[hej, hopp], article2:[hopp, hej]}}
    
    #Goal: to put all words into one corpus so that you can count the vocab and get the unique words
    #For the vector building you need to keep track of each article again
    
    print(type(class_documents))
        
    vocab_counts = {}
    
    for topic in class_documents:
        articles = class_documents[topic]
        
        for art in articles:
            words = articles[art]
        
            for word in words:
                if word in vocab_counts:
                    vocab_counts[word] +=1
                else:
                    vocab_counts[word] = 1
            
    print(vocab_counts)
    return vocab_counts

def make_unique(vocab_counts):
    
    unique = {}
    count = 0
    
    for word in vocab_counts:
        unique[word] = count
        count+=1
        
    #print(unique)
    return unique

def build_vectors(class_documents, unique_words, vocab_counts, number):
    #Builds vectors out of the two classes
    #Form of class_documents: {news:{article1:[hej, hopp], article2:[hopp, hej]}}, {fiction:{article1:[hej, hopp], article2:[hopp, hej]}}
    #One vector per article
    
    #When building vectors, store all vectors regardless of topic, in a list, and for each vector, look if it's in the list already. If it is, don't add it but print it to the terminal (or store in a duplicates list and print list last.
        
    vectors = {}
    print(len(vocab_counts), len(unique_words))
    #First, sort the dictionary unique_words so that it goes from 0-n (by value)

    for topic in class_documents:
        articles = class_documents[topic]
        
        for art in articles:
            vector = []
            article_content = articles[art] #list of the words in the article
           
            #print(article_content)
    
            for word in unique_words:
                i = unique_words[word]
                
                #Considers the -B argument
                if number != None and article_content.count(word) > number:
                    vector.append(article_content.count(word)) #counts in the article
                else:
                    vector.append(article_content.count(word)) #counts in the article
                    
                
            #Check here if vector is a duplicate! 
                
            vectors[art] = vector
    
    print(vectors)
    return vectors

def preprocess(textfile):
    
    """Preprocesses the file.
        
    Args:
        textfile:   A string consisting of the file's content.
    
    Returns:
        A list of words tokenized from the text.
    
    """       
    
    #Making the text lowercase
    text = textfile.lower()
    
    #Removes punctuation - expand this to a regular expressions with all punctuation
    text = text.replace('.', '')
    
    #Tokenizing the text by splitting on whitespace
    words = text.split()
    
    return words


def parse_arguments(parser):
    
    """Parses the arguments from the command line.
        
    Args:
        parser:   An ArgumentParser object.
    
    Returns:
        A Namespace object built from the parsed attributes.
    
    """      
    
    #Adds arguments from the command line to the parser
    parser.add_argument("foldername", type=str,
                    help="The base folder name containing the two topic subfolders.")
    parser.add_argument("-B", "--base-vocab", metavar="M", dest="basedims",
                    type=int, default=None,
                    help="Use the top M dims from the raw counts before further processing")
    parser.add_argument("-T", "--tfidf", action="store_true", help="Apply tf-idf to the matrix.")
    parser.add_argument("-S", "--svd", metavar="N", dest="svddims", type=int,
                    default=None,
                    help="Use TruncatedSVD to truncate to N dimensions")
    parser.add_argument("outputfile", type=str,
                    help="The name of the output file for the matrix data.")
    

    return parser.parse_args()



if __name__ == "__main__":
        
    #Parses the arguments from the command line
    args = parse_arguments(argparse.ArgumentParser(description="Generate term-document matrix."))  
    
    #Open the files and creates the corpus
    print("Loading data from directory {}.".format(args.foldername))    
    class_documents = browse_data(args.foldername)
    
    #Organize the texts
    #corpus = structure(class_documents)
    
    #Count words
    vocab_counts = count_vocab(class_documents)
    
    #Make a unique dictionary
    unique_words = make_unique(vocab_counts)
    
    #Build vectors
    if not args.basedims:
        print("Using full vocabulary.")
    else:
        print("Using only top {} terms by raw count.".format(args.basedims))
    
    vectors = build_vectors(class_documents, unique_words, vocab_counts, args.basedims)
                
    #Prints the matrix to the specified output file
    print("Writing matrix to {}.".format(args.outputfile))
    out = open(args.outputfile, 'w')
    for vector in vectors:
        out.write("{}: {}\n".format(vector, vectors[vector]))

    
    
