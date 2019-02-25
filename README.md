# LT2212 V19 Assignment 2

From Asad Sayeed's statistical NLP course at the University of Gothenburg.

My name: Sandra Derbring

## Additional instructions

You can choose a output file in .txt format but the script will transform it into a csv file for convenience. 

## File naming convention

1.csv - no vocabulary restriction and no other transformations
2.csv - vocabulary restriction and no other transformations
3.csv - no vocabulary restriction and tf-idf applied
4.csv - vocabulary restriction and tf-idf applied
5.csv - no vocabulary restriction and truncated SVD applied to 100 dimensions
6.csv - no vocabulary restriction and truncated SVD applied to 1000 dimensions
7.csv - no vocabulary restriction, tf-idf applied and truncated SVD applied to 100 dimensions
8.csv - no vocabulary restriction, tf-idf applied and truncated SVD applied to 1000 dimensions

## Results and discussion

### Vocabulary restriction.

The vocabulary restriction for output file (2) and (4) is 500, meaning that only words that occur more frequently than 500 times in the corpus. I chose this number to filter out many low-frequent words but still keep frequent words that are not only stopwords.

### Result table

|       | Crude               | Grain               | Crude to grain      | Grain to crude      |
|-------|---------------------|---------------------|---------------------|---------------------|
| 1.csv | 0.40972978673808474 | 0.40381580296901565 | 0.3669166364591192  | 0.36691663645911965 |
| 2.csv | 0.6069213421472334  | 0.5737999038679049  | 0.5445101257668392  | 0.5445101257668352  |
| 3.csv | 0.12087728860490521 | 0.11953203655230543 | 0.08872626926860958 | 0.08872626926861149 |
| 4.csv | 0.5013893102077449  | 0.4483378958686223  | 0.40042725733848666 | 0.4004272573385009  |
| 5.csv | 0.40972978673808474 | 0.40381580296901565 | 0.3669166364591192  | 0.36691663645911965 |
| 6.csv | 0.40972978673808474 | 0.40381580296901565 | 0.3669166364591192  | 0.36691663645911965 |
| 7.csv | 0.12087728860490521 | 0.11953203655230543 | 0.08872626926860958 | 0.08872626926861149 |
| 8.csv | 0.12087728860490521 | 0.11953203655230543 | 0.08872626926860958 | 0.08872626926861149 |

### The hypothesis in your own words
The hypothesis was that comparing the data belonging to two topics, the similarities between the texts within a topic would be greater in average than comparing data between topics. 

### Discussion of trends in results in light of the hypothesis
The trends in my data is that the hypothesis actually holds true, but that the differences between the numbers are not that significant. The numbers are however significantly lower generally when comparing the inverse frequency values than the raw values and the difference between groups are also larger. For the files with SVD truncated, the numbers are exactly the same, no matter the dimensions. The conclusion is that treating data in these ways don't shed much light when comparing similiarites.
