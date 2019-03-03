import os, sys
import glob
import argparse
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfTransformer

# gendoc.py 

def load_data(filename):
        
    with open(filename, "r") as myfile:
        lines = myfile.readlines() 
        doc = " ".join([a.strip() for a in lines])
    
    return doc


def browse_data(folder):

    print(folder)
    
    subfolders = os.listdir(folder)
    
    #Excluding possible folder settings files in the folders
    if '.DS_Store' in subfolders:
        sindex = subfolders.index('.DS_Store')
        subfolders.pop(sindex)
            
    subfolder_texts = {}
        
    for sub in subfolders:
        classtexts = {}
        subpath = folder+sub
        articles = os.listdir(subpath)
        
        if '.DS_Store' in articles:
            aindex = articles.index('.DS_Store')
            articles.pop(aindex)
        
        for art in articles:
            filename = '/'.join([subpath, art])
            document = load_data(filename)
            processed_document = preprocess(document)
            classtexts[filename] = processed_document
                           
        subfolder_texts[sub] = classtexts
        
    return subfolder_texts


def count_vocab(class_documents):
    
    #Puts all word type into a vocabulary with their frequency in the corpus
            
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
            
    return vocab_counts

def make_unique(vocab_counts):

    #Creates a dictionary of all words with a unique index number
    #Done for all the words in the corpus or the limited set chosen by the user
    
    unique = {}
    count = 0
    
    for word in vocab_counts:
        unique[word] = count
        count+=1
        
    return unique


def limit_vocab(vocab_counts, number):

    #Selects only words with a corpus frequency higher
    #than the user's choice
    
    limited_vocab = {}

    for x in vocab_counts:
        if vocab_counts[x] > number:
            limited_vocab[x] = vocab_counts[x]
    
    return limited_vocab


def build_vectors(class_documents, unique_words):
    #Builds vectors out of the two classes
     #One vector per article
    
    vectors = []
    all_articles = []
    
    #Sort the dictionary unique_words into a list by index value with lowest value first
    sorted_unique_words = sorted(unique_words, key=unique_words.get)

    for topic in class_documents:
        articles = class_documents[topic]
        
        for art in articles:
            vector = []
            article_content = articles[art] #list of the words in the article
               
            for word in sorted_unique_words:

                vector.append(article_content.count(word)) #counts in the article
                                
            #Checks if vector is a duplicate
            if vector not in vectors:
                vectors.append(vector)
                all_articles.append(art)
            else:
                print("Dropped duplicate vector {}".format(art))    

    vector_array = np.array(vectors)
    
    return vector_array, all_articles


def apply_tdidf(matrix):

    #Applies tf-idf on the matrix
    tfidf_transformer = TfidfTransformer()
    tfidf_data = tfidf_transformer.fit_transform(matrix)

    return tfidf_data


def apply_svddims(matrix, dimension):

    #Applies truncated SVD on the matrix with a given dimension
    TS = TruncatedSVD(dimension)

    svd = TS.fit_transform(matrix)
    
    return svd


def make_pdframe(vectors):

    #Make a Panda Dataframe of the vectors
    dataframe = pd.DataFrame(vectors)
    
    return dataframe


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


def print_matrix(outputfile, vectors, unique_words, all_articles, is_svd):

    #Make sure the file will be a csv file
    if outputfile.endswith('.txt'):
        filename = outputfile.split('.')[0]
        outputfile = filename+'.csv'
        print("Transforming your given output file to csv format: {}".format(outputfile))
        
    out = open(outputfile, 'w')
    
    #Makes a panda dataframe
    pdframe = make_pdframe(vectors)
    pdframe.index = all_articles

    if not is_svd:
        pdframe.columns = list(unique_words)
    
    #Prints to a csv file
    pdframe.to_csv(out, encoding="utf-8")
        
    out.close()



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

    is_svd = False
    
    #Parses the arguments from the command line
    args = parse_arguments(argparse.ArgumentParser(description="Generate term-document matrix."))
    
    #Open the files and creates the corpus
    print("Loading data from directory {}.".format(args.foldername))    
    class_documents = browse_data(args.foldername)
           
    #Count words
    vocab_counts = count_vocab(class_documents)
        
    #Make a unique dictionary
    if not args.basedims:
        print("Using full vocabulary.")
        unique_words = make_unique(vocab_counts)
    else:
        print("Using only top {} terms by raw count.".format(args.basedims))
        limited_vocab = limit_vocab(vocab_counts, args.basedims)
        unique_words = make_unique(limited_vocab)
        
    #Build vectors
    vectors, all_articles = build_vectors(class_documents, unique_words)

    #Applies tf-idf
    if args.tfidf:
        print("Applying tf-idf to raw counts.")
        tfidf = apply_tdidf(vectors)
        vectors = tfidf.toarray()

    #Applies SVD
    if args.svddims:
        print("Truncating matrix to {} dimensions via singular value decomposition.".format(args.svddims))
        vectors = apply_svddims(vectors, args.svddims)
        is_svd = True
            
    #Prints the matrix to the specified output file
    print("Writing matrix to {}.".format(args.outputfile))
    print_matrix(args.outputfile, vectors, unique_words, all_articles, is_svd)
