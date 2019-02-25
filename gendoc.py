import os, sys
import glob
import argparse
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfTransformer

# gendoc.py -- Don't forget to put a reasonable amount code comments
# in so that we better understand what you're doing when we grade!

# add whatever additional imports you may need here


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
            
    #print(vocab_counts)
    return vocab_counts

def make_unique(vocab_counts):

    #Done for all the words in the corpus or the limited set chosen by the user
    
    unique = {}
    count = 0
    
    for word in vocab_counts:
        unique[word] = count
        count+=1
        
    #print(unique)
    return unique

def limit_vocab(vocab_counts, number):
    limited_vocab = {}

    for x in vocab_counts:
        if vocab_counts[x] > number:
            limited_vocab[x] = vocab_counts[x]
    
    return limited_vocab


def build_vectors(class_documents, unique_words, vocab_counts):
    #Builds vectors out of the two classes
    #Form of class_documents: {news:{article1:[hej, hopp], article2:[hopp, hej]}}, {fiction:{article1:[hej, hopp], article2:[hopp, hej]}}
    #One vector per article
    
    vectors = []
    all_articles = []
    all_words = []
    
    #print(len(vocab_counts), len(unique_words))
    #First, sort the dictionary unique_words so that it goes from 0-n (by value)

    for topic in class_documents:
        articles = class_documents[topic]
        
        for art in articles:
            vector = []
            article_content = articles[art] #list of the words in the article
           
            #print(article_content)
    
            for word in unique_words:
                #i = unique_words[word]

                vector.append(article_content.count(word)) #counts in the article
                
                #Considers the -B argument - this should be done in the vocab_counts (see Asad's example - for the whole corups, not per document), you want to look at the words that occur many times in the whole crpus, and then see how frequent they are in the resp doc. Try make a list of these words before this method, an own method that is triggered if B is set and use that list as argument to this method instead. 

                '''
                if number != None and article_content.count(word) > number:
                    print("appending just " + str(number) + "counts")
                    vector.append(article_content.count(word)) #counts in the article
                else:
                    print("appending all counts")
                    vector.append(article_content.count(word)) #counts in the article
                

                if number==None:
                    print("Appending all counts")
                    vector.append(article_content.count(word))
                    all_words.append(word)
                else:
                    if article_content.count(word) > number:
                        print("Word has count: " + str(article_content.count(word)))
                        vector.append(article_content.count(word))
                    else:
                        print("Word count TOO LOW")
                        pass
                '''
                
            #Check here if vector is a duplicate! 
            if vector not in vectors:
                vectors.append(vector)
                all_articles.append(art)
            else:
                print("Dropped duplicate vector {}".format(art))    

    vector_array = np.array(vectors)
    #print(vector_array)
    print(vector_array.shape)

    #print(vectors)
    return vector_array, all_articles

def apply_tdidf(matrix):

    
    tfidf_transformer = TfidfTransformer()
    tfidf_data = tfidf_transformer.fit_transform(matrix)

    #print(tfidf_data)
    #print(type(tfidf_data))
    #print(tfidf_data.shape)

    return tfidf_data


def apply_svddims(matrix, dimension):

    TS = TruncatedSVD(dimension)

    svd = TS.fit_transform(matrix)

    #print(svd)
    #print(svd.shape)
    
    return svd


def make_pdframe(vectors):

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
    if not args.basedims:
        print("Using full vocabulary.")
        unique_words = make_unique(vocab_counts)
    else:
        print("Using only top {} terms by raw count.".format(args.basedims))
        limited_vocab = limit_vocab(vocab_counts, args.basedims)
        unique_words = make_unique(limited_vocab)
    
    #Build vectors
    vectors, all_articles = build_vectors(class_documents, unique_words, vocab_counts)
    
    #vectors, all_articles = build_vectors(class_documents, unique_words, limited_vocab)    
    #vectors, all_articles = build_vectors(class_documents, unique_words, vocab_counts, args.basedims)

    
    if args.tfidf:
        print("Applying tf-idf to raw counts.")
        tdidf_data = apply_tdidf(vectors)

    if args.svddims:
        print("Truncating matrix to {} dimensions via singular value decomposition.".format(args.svddims))
        svd = apply_svddims(vectors, args.svddims)
        
    pdframe = make_pdframe(vectors)

    #Prints the matrix to the specified output file
    print("Writing matrix to {}.".format(args.outputfile))

    out = open(args.outputfile, 'w')

    pdframe.columns = list(unique_words)
    pdframe.index = all_articles

    print(pdframe)

    #Use max counts bla bla to show all data in the rows, might help with the simdoc input reading
    
    pdframe.to_csv(out, encoding="utf-8")
    
    #for i in range(0, len(all_articles)):
        #out.write("{}\t{}\n".format(all_articles[i], vectors[i]))

    out.close()
