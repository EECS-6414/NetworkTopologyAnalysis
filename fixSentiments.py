import pandas


def fixSentimentFiles(path, names):
    for index, item in enumerate(names):
        if "aaa_new" not in item:
            print("processing index (out of 500): "+str(index))
            try:
                filePath = pandas.read_csv(str(path+"/"+item))
                filePath.to_csv(str(path+"/aaa_new/"+item), index=False)
            except:
                print("Process file.."+str(item))
                filePath = open(str(path+"/"+item),'r', encoding='utf8')
                outputFile = open(str(path+"/aaa_new/"+item),'w', encoding='utf8')
                for i in filePath:
                    parts = i.split(",")
                    if len(parts)>7:
                        lenghtParts = len(parts)
                        sentiment = parts[lenghtParts-1]
                        compound = parts[lenghtParts-2]
                        pos = parts[lenghtParts-3]
                        neu = parts[lenghtParts-4]
                        neg =parts[lenghtParts-5]
                        date =parts[lenghtParts-6]
                        author = parts[0]
                        outputFile.write(author+","+date+","+neg+","+neu+","+pos+","+compound+","+sentiment)
                    else:
                        outputFile.write(i)



