from TNA import TNAfunc
from fileNames import files
from fixSentiments import fixSentimentFiles


def main():
    mainPath = '/Users/jaime/Documents/York_University/Winter_2021/Data_Vizualization/Project/gitlab/datasets/sentiment'
    names = files(mainPath)

    # for cleaning the reviews
    #fixSentimentFiles(mainPath, names)

    TNAfunc(mainPath, names)

if __name__ == "__main__":
    main()