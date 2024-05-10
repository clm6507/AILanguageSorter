import pickle
import sys
from TreeNode import TreeNode
from Sample import Sample
from DataNode import DataNode, Language



#pass in a filename and the function will return a Sample with all the data in the file in it
def makeSample(thefile: str):
    #this block makes a set with as the number of attributes of a datanode in it
    example_datanode = DataNode("", Language.UNKNOWN, 0)
    untested_attributes = set()
    for att in range(len(example_datanode.attribute_list)):
        untested_attributes.add(att)

    #initializes the sample
    empty_list = []
    sample = Sample(empty_list, untested_attributes)


    #reads file
    with open(thefile) as file:
        file_lines = file.readlines()
        for line in file_lines:
            #lines formatted as LANGUAGE|15 WORDS for training sets
            split_line = line.split("|")
            if(split_line[0] == "en"):
                sample.addNode(DataNode(split_line[1], Language.ENGLISH, 1)) 
            else:
                sample.addNode(DataNode(split_line[1], Language.DUTCH, 1))
        
        #weights all samples evenly and makes sure they add to 1 for adaBoost  
        sample.normalizeWeights()

    return sample
    
#based on the forest and node passed in, uses weights of the stumps to make a guess about what language the 15 word block is
def makeAdaBoostGuess(forest: list[TreeNode], data: DataNode):
    is_english = 0
    is_dutch = 0
    for stump in forest:
        if(data.attribute_list[stump.split_on]):
            is_english += stump.stumpWeight
        else:
            is_dutch += stump.stumpWeight
    
    if( is_english > is_dutch):
        print("en")
    else:
        print("nl")

#returns a fleshed out decision tree
def makeDecisionTree(dataset: Sample) -> TreeNode:
    untested: set[int] = set()
    for i in range(len(dataset.datanodes[0].attribute_list)):
        untested.add(i)
    return TreeNode(dataset, untested)

#pass in a training sample, where you want to write it, and how many stumps you want
#the function will write a list of decision tree stumps to the file passed in
def trainAdaBoost(dataset: Sample, outfile: str, num_stumps: int):
    #initializes forest and the first node
    adaBoostForest: list[TreeNode] = []
    originalNode = TreeNode(dataset)
    adaBoostForest.append(originalNode)

    for i in range(num_stumps-1):
        #makes new nodes based on previous nodes
        new_sample = adaBoostForest[-1].makeNewSample()
        adaBoostForest.append(TreeNode(new_sample))
    
    #dumps into file
    with open(outfile, "wb") as file:
        pickle.dump(adaBoostForest, file)


#pass in a training sample and what you want to write to and this function will write the decision tree there
def trainDecisionTree(dataset: Sample, outfile: str):
    decisionTree = makeDecisionTree(dataset)
    with open(outfile, "wb") as file:
        pickle.dump(decisionTree, file)
    




def main():
    if(len(sys.argv) == 1):
        #this is for testing locally and with debugger
        """
        dataset = makeSample("./train_15_1000.txt")
        trainDecisionTree(dataset, "./best.model")

        with open("./best.model", "rb") as file:
            tree: TreeNode = pickle.load(file)"""
        print("Read the README.md for instructions on how to use the language sorter")
        

    #training
    elif(sys.argv[1].lower() == "train"):

        examplesFile = sys.argv[2]
        hypothesisOutFile = sys.argv[3]

        sample = makeSample(examplesFile)
        
        #training decision tree
        if(sys.argv[4] == "dt"):
            trainDecisionTree(sample, hypothesisOutFile)
        
        #training adaBoost algo
        else:
            #number of trees that will be in the adaboost forest
            num_stumps = 4
            trainAdaBoost(sample, hypothesisOutFile, num_stumps)

        

    #prediction
    elif(sys.argv[1].lower() == "predict"):

        hypothesisFileName = sys.argv[2]

        with open(hypothesisFileName, "rb") as file:

            #object that is either an adaBoost forest or the decision tree parent node
            tree: TreeNode | list[TreeNode] = pickle.load(file)


            with open(sys.argv[3]) as predictfile:
                lines = predictfile.readlines()
                for line in lines:
                    if(type(tree) == TreeNode):
                        if(tree.makeGuess(DataNode(line)) == Language.ENGLISH):
                            print("en")
                        else:
                            print("nl")
                    else:
                        #this is actually passing in a forest
                        makeAdaBoostGuess(tree, DataNode(line))



    else:
        #if we ever see this we know something went wrong
        print("why r u here")

    


if(__name__ == "__main__"):
    main()