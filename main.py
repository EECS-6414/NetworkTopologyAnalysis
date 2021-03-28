from RecommendationAPP import RecommendApp
from TNA import TNAfunc
from fileNames import files
from fixSentiments import fixSentimentFiles


def main():
    mainPath = '/Users/jaime/Documents/York_University/Winter_2021/data_vizualization/project/gitlab/datasets/sentiment'
    #mainPath = '/Users/jaime/Documents/York_University/Winter_2021/data_vizualization/project/Sentiment'
    names = files(mainPath)

    # for cleaning the reviews
    #fixSentimentFiles(mainPath, names)

    #TNAfunc(mainPath, names)
    authorsUsedWith8 = ["Karen Barnes", "Edward Figueroa","Matt Arnold", "Melanie Martinez", "Andrew Burke"]
    #authorsUsedFrom8to12 = ["Jesse Castillo", "Steve Lewis", "Pavlina Gueorgieva", "Brenda Genrich", "Ronald Taylor"] # from 8 to 12

    for i in authorsUsedWith8:
        RecommendApp(i)

if __name__ == "__main__":
    main()