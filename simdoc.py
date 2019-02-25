import os, sys
import argparse
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# simdoc.py -- Don't forget to put a reasonable amount code comments
# in so that we better understand what you're doing when we grade!

# add whatever additional imports you may need here

def load_data(vectorfile):
    
    #Read the data and transform it into an numpy array
    pdfile = pd.read_csv(vectorfile)

    #print(type(pdfile))
    
    vectors = np.array(pdfile)

    #print(type(vectors))
    print(vectors.shape)
    
    #print(vectors)
    #This gets the arrays with the article path as first element. Just split each vector (elemtn 0 and rest) and use the 0 element for topic and the rest as a list input to cosine function

    return vectors


def extract_topics(vectors):

    crude_vectors = []
    grain_vectors = []

    #print vectors
    #Arrays have the article path as first element. Split each vector and use the 0 element for topic and the rest as a list input to cosine function

    '''
    print(vectors[0,0])
    print(vectors[0,1])
    print(vectors[1,0])
    print(vectors[1,1])
    '''
    
    for arr in vectors:
        #print(arr)
        path = arr[0]
        vector = arr[1:]

        #print(path)
        #print(vector)

        
        pathparts = path.split('/')
        topic = pathparts[len(pathparts)-2]
        #print(topic)

        if topic == 'crude':
            #print("Adding vector to crude list")
            crude_vectors.append(vector)
        elif topic == 'grain':
            #print("Adding vector to grain list")
            grain_vectors.append(vector)
        else:
            print("The folder {} was not found".format(path))
         
    print("{} vectors for topic crude".format(len(crude_vectors)))
    print("{} vectors for topic grain".format(len(grain_vectors)))
    return crude_vectors, grain_vectors


def ave_x_sim(matrix, topic):
    
    sim = cosine_similarity(matrix)

    #print(sim)
    #print(type(sim))

    simsum = 0
    comparecount = 0

    for i in range(0, len(sim)):
        v = sim[i]
        for j in range(i, len(v)):
            simsum += v[j]
            comparecount += 1

    average = simsum/comparecount

    print("Values for {}".format(topic))
    print("**********")
    print("Sum: {}".format(simsum))
    print("Nr of comparisions: {}".format(comparecount))
    print("Average: {}".format(average))
    print()

def ave_xy_sim(matrix1, matrix2, topic1, topic2):
    
    sim_table = cosine_similarity(matrix1, matrix2)

    print(sim_table)
    #print(type(sim_table))

    
    simsum = 0
    comparecount = 0

    for vector in sim_table:
        for sim in vector:
            simsum += sim
            comparecount += 1

    average = simsum/comparecount
    
    
    print("Comparing {} to {}:".format(topic1, topic2))
    print("**********")
    print("Sum: {}".format(simsum))
    print("Nr of comparisions: {}".format(comparecount))
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

    vectors = load_data(args.vectorfile)

    crude_vectors, grain_vectors = extract_topics(vectors)

    #ave_x_sim(crude_vectors, 'crude')
    #ave_x_sim(grain_vectors, 'grain')

    #ave_xy_sim(crude_vectors, grain_vectors, 'crude', 'grain')
    #ave_xy_sim(grain_vectors, crude_vectors, 'grain', 'crude')
    
    #Testdata
    pdtest1 = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    pdtest2 = pd.DataFrame([[3, 3, 3], [2, 2, 2], [1, 1, 1]])
    nptest1 = np.array(pdtest1)
    nptest2 = np.array(pdtest2)
    #ave_x_sim(nptest1, 'test')
    ave_xy_sim(nptest1, nptest2, 'test1', 'test2')
    ave_xy_sim(nptest2, nptest1, 'test2', 'test1')
