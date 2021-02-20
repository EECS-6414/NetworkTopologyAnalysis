## Network 
This network is based on two files:
1. **frequency.csv**: This file contains the reviews of 523,620 with at least 2 reviews. The real number after preprocessing, however, is 462,842 authors.
2. **apps_names**: It has the 546 app's names

### Sentiment 
The edge of this network is the sentiment prediction: red for negative, blue for positive and black for neutral. The red nodes is the app and the blue is autrors.
<div>
<img src="TopologicalAnalysis_edges.jpg" width="700px"</img> 
</div>

### How to execute
This script takes around 12 minutes to run. You need to have the Sentiment CSV files in our machine from the [GitLab](https://gitlab.com/jaimedantas/datasets/-/tree/master/sentiment) and update the path `mainPath` with your path.

In order to execute this script and have the network `G`, just execute the `main()` function as it is.

## Results
Name: Topological Network Analysis
Type: Graph
Number of nodes: 463387
Number of edges: 1105531
Average degree:   4.7715
Network density: 1.0297081884469975e-05
Node degree average APP: 2024.7857142857142
Node degree average Author: 2.388571885377484

Top 10 Authors:
('Lim Yen Ping', 24)
('Emanuel Seuneke', 23)
('Rhonda Paschal', 22)
('Filipe Governa', 20)
('Janko Kinčeš', 18)
('Christina Reed', 18)
('Josh Clark', 17)
('Samuel Smith', 17)
('Andri Untoro', 17)
('William Howard', 17)

Top 10 Apps:
('Google Photos', 178780)
('Google Duo - High Quality Video Calls', 119191)
('Candy Crush Soda Saga', 64660)
('Google Play Music', 59607)
('Candy Crush Saga', 49712)
('Mini Militia - Doodle Army 2', 44805)
('Candy Crush Jelly Saga', 27572)
('Castle Clash: Heroes of the Empire US', 25430)
('MX Player', 24602)
('Google Docs', 20272)
