import os, sys
import argparse
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# simdoc.py

def load_data(vectorfile):
    
    #Read the data and transform it into an numpy array
    pdfile = pd.read_csv(vectorfile)
    vectors = np.array(pdfile)
    
    return vectors


def extract_topics(vectors):

    crude_vectors = []
    grain_vectors = []

    #Arrays have the article path as first element.
    #Split each vector and use the 0 element for topic
    #and the rest as the vector
    
    for arr in vectors:
        path = arr[0]
        vector = arr[1:]

        pathparts = path.split('/')
        topic = pathparts[len(pathparts)-2] #the topic is always the next to last element

        #Add vectors to their topic lists
        if topic == 'crude':
            crude_vectors.append(vector)
        elif topic == 'grain':
            grain_vectors.append(vector)
        else:
            print("The folder {} was not found".format(path))
         
    print("{} vectors for topic crude".format(len(crude_vectors)))
    print("{} vectors for topic grain".format(len(grain_vectors)))
    return crude_vectors, grain_vectors


def ave_x_sim(matrix, topic):

    #Calculates cosine similarity of one matrix
    sim = cosine_similarity(matrix)

    simsum = 0
    comparecount = 0

    #Add each similarity value and keep track of the count
    #For each vector, only count the values not already accounted for
    for i in range(0, len(sim)):
        v = sim[i]
        for j in range(i, len(v)):
            simsum += v[j]
            comparecount += 1

    #Divide the sum with the count to get the average
    average = simsum/comparecount

    print("Values for {}".format(topic))
    print("Average: {}".format(average))
    print()

def ave_xy_sim(matrix1, matrix2, topic1, topic2):

    #Calculates cosine similarity of two matrices
    sim_table = cosine_similarity(matrix1, matrix2)

    simsum = 0
    comparecount = 0

    #Add each similiarity value and keep track of the count
    for vector in sim_table:
        for sim in vector:
            simsum += sim
            comparecount += 1

    #Divide the sum with the count to get the average
    average = simsum/comparecount
    
    
    print("Comparing {} to {}:".format(topic1, topic2))
    print("Average: {}".format(average))
    print()
    
    
def parse_arguments(parser):

    """Parses the argument from the command line. 

    Args:
    parser: An ArgumentParser object.

    Returns:
    A Namespace object buit from the parsed attributes.
    """

    #Adds arguments from the command line to the parser    
    parser.add_argument("vectorfile", type=str,
                    help="The name of the input  file for the matrix data.")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments(argparse.ArgumentParser(description="Compute some similarity statistics."))

    print("Reading matrix from {}.".format(args.vectorfile))

    #Load the data
    vectors = load_data(args.vectorfile)

    #Extract the data into topics
    crude_vectors, grain_vectors = extract_topics(vectors)

    #Calculates cosine within a topic
    ave_x_sim(crude_vectors, 'crude')
    ave_x_sim(grain_vectors, 'grain')

    #Calculate cosine across two topics
    ave_xy_sim(crude_vectors, grain_vectors, 'crude', 'grain')
    ave_xy_sim(grain_vectors, crude_vectors, 'grain', 'crude')
