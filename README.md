# A-Frame, Python, and NCAA Men's Basketball Data

## Demos
[Interactive 3D Chart](https://hopetambala.github.io/aframe-NCAAB/aFrame/)

<p align="middle">
    <img src="images/thumbnail.png">
</p>

## Description
The goal of this project was to use Google's BigQuery Python client library to query data in [Kaggle's NCAA Basketball data](https://www.kaggle.com/ncaa/ncaa-basketball) which dates from as far back as 1894. We chose a subset of data from the 2017-2018 NCAA Basketball Tournament bracket and created an A-Frame Visualization using D3.js. 

The data was queried into a Pandas to allow for easier data manipulation. CSVs of the data were generated and placed into the Aframe folder. Using d3, that data was loaded into Aframe to create a 3D "Bracket-like" Scatter Plot that explores the relationships between the basketball teams
A) Seed in the Tournament
B) Playing Style
C) Progression into the tournament.

## Resources 
[NCAAB Data Set](https://www.kaggle.com/ncaa/ncaa-basketball)

[Basketball Analytics](https://www.nbastuffer.com/team-evaluation-metrics/)

## Libraries
[Pandas](https://pandas.pydata.org/)

[Google BigQuery](https://cloud.google.com/bigquery/docs/reference/libraries)

[A-Frame](https://aframe.io/)

[D3.js](https://d3js.org/)

## Project Layout
    ├── python                                   # Folder for data generation script and data in csvs
    ├── aFrame                                   # Folder for Aframe
        ├── 2017_season_detailed_cleaned.csv        # the generated data from python that will be used by d3
        ├── 2017_season_detailed_cleaned.xlsx       # to make sense of the csv by the programmer
        ├── index.html                              # the website is based here
        ├── js                                      # Folder for js files
            ├── script_for_aFrame_d3.js                 # Use d3 to build and manipulate a-frame
            ├── script_for_aFrame.js                    # the original js file for manipulate a-frame without d3
    ├── images                                   # Folder for images used for README.md
    ├── LICENSE              
    └── README.md

## Build and run

### Python 
Install virtual environment library
```
cd python/
pip install virtualenv #if you don't have virtualenv installed 
```

Create and activate virtualenv
```
virtualenv <Name_of_Virtual_Environment>
source <Name_of_Virtual_Environment>/bin/activate
```

Install project requirements usings the reqs.text
```
pip install -r reqs.txt
```

Install BigQuery helper function
```
pip install -e git+https://github.com/SohierDane/BigQuery_Helper#egg=bq_helper
```

Enable Google authentication by exporting the required .json keys via terminal
```
export GOOGLE_APPLICATION_CREDENTIALS=./secrets/Data\ Visualization-0a64d281dd18.json
```

Run python script to generate CSV via terminal
```
python bball_query.py
```

### Javascript 
Run the following in the javascript folder to start your own server
```
python -m SimpleHTTPServer
```
## Tutorial & Development
### BigQuery and Pandas
We used Kaggle's NCAA Basketball dataset as the basis for the A-Frame visualization. We generated some "secret" keys in order to get access to the Python BigQuery library and then used pandas to query the data using the below `SELECT` statement.

```
query = """
    SELECT 
        *
    FROM `bigquery-public-data.ncaa_basketball.mbb_games_sr` as teams_game
    WHERE teams_game.season = 2017
    AND teams_game.tournament = 'NCAA'
    AND teams_game.tournament_type IN ('South Regional', 'West Regional', 'National Championship','East Regional','First Four','Midwest Regional','Final Four');
"""
```

We then threw that into the results from that query into a Pandas Dataframe and created a CSV

```
df = ncaa_basketball.query_to_pandas_safe(query, max_gb_scanned=1)
```
```
df.to_csv(r'generated_data/'+'2017_season_detailed'+'.csv')
```
#### NBA Analytics and Equations
There was a decent amount of manual manipulation that was required to get the CSV in the correct format. 
<p align="middle">
    <img src="images/excel.png">
</p>

The CSV generated had data on basketball matches versus teams. This made it harder to create a scatterplot regarding the stats of individual teams. We figured out that if we just copy and pasted the "Away" teams (and their stats) for each match and appended them to the end of the excel sheet, we would be able to make the scatterplot based on teams.

There were three variables we created to generate analytics for each team in a game.
- Possesion
- Offensive Efficiency
- Defensive Efficiency 

##### Possession
How the Possession is Calculated?
It counts as a team possession every time when a player of that team;
- attempts a field goal,
- misses a shot and does not get the offensive rebound,
- turns the ball over (some sources add “turnovers that are assigned to teams” for a more precise possession calculation),
- goes to the line for two or three shots and either makes the last shot or does not get the rebound of a missed last shot.

```
Basic Possession Formula=0.96*[(Field Goal Attempts)+(Turnovers)+0.44*(Free Throw Attempts)-(Offensive Rebounds)]
```

##### Offensive Effiency
The number of points a team scores per 100 possessions. This variable is determined using the previously the Possession variable
```
Offensive Efficiency Formula=100*(Points Scored)/(Possessions)
```

##### Defensive Effiency
The number of points a team allows per 100 opposing team possessions.
```
Defensive Efficiency Fomula=100*(Points Allowed/Possessions)
```
Note: In a game, the  “defensive efficiency” of a team equals to the “offensive efficiency” of the opponent team as well

### AFrame
A-Frame is basically a framework based on THREE.js for VR/AR experience to be built into DOM system. It is quite "user-friendly" for people who know HTML to pick up, since it looks like a bunch of HTML tags. Below is a simple structure for using A-Frame, which is wrapped in "body". But you should link the A-Frame version in "head":

```
<head>
    <title>NCAA VR DataVis</title>
    <script src="//aframe.io/releases/0.8.2/aframe.min.js"></script>
</head>
<body>
    <a-scene cursor="rayOrigin: mouse">
        <!--primitives-->
        <a-cylinder></a-cylinder>
    
        <!--camera-->
        <a-entity id="head" camera wasd-controls="fly: true" look-controls></a-entity> </a-entity>
        
        <!--background-->
        <a-sky color="#170F21"></a-sky>
    </a-scene>
</body>
```

#### Primitives
From the structure above, there's an a-cylinder, it is an A-Frame pre-defined cylinder, and you can find more at [HTML & Primitives](https://aframe.io/docs/0.9.0/introduction/html-and-primitives.html).

To modify the primitive, you can simply play with the attributes, like:
```
<a-cylinder scale="0.5 0.5 0.5" position="1 2 1" color="blue" segments-radial="20"></a-cylinder>
```
The attributes don't need to be sequential. Different primitive may have different unique attributes, like "segments-radial" is special for [a-cylinder](https://aframe.io/docs/0.9.0/primitives/a-cylinder.html). Feel free to just google the documents on any specific attributes you need.

Also, you can fork [Neil's CodePen](https://codepen.io/neilzhu/pen/axYgqm) and play around it to get some more sense.

#### A-entity
[A-entity](https://aframe.io/docs/0.9.0/core/entity.html) is a generic object in A-Frame that has the potential to be a lot of pre-defined A-Frame elements, the a-cylinder can be presented as a-entity as well:
```
<a-entity geometry="primitive: cylinder; segments-radial: 20" material="color: blue" position="1 2 1" scale="0.5 0.5 0.5"></a-entity>
```
Also, the "#head" in the example structure above is one example:
```
<a-entity id="head" camera wasd-controls="fly: true" look-controls></a-entity></a-entity>
```

#### VR control
Essentially, on top of what we already have, VR control just needs controllers defined. So here's how the camera part can be modified for this task:
```
<a-entity id="cameraRig">
    <a-entity id="head" camera wasd-controls="fly: true" look-controls></a-entity>
    <a-entity id="leftHand" raycaster="showLine: true"
                line="color: white; opacity: 0.25" laser-controls="hand:left"
                teleport-controls="cameraRig: #cameraRig;
                                    teleportOrigin: #head;
                                    button: trackpad;
                                    curveShootingSpeed: 30;"
                laser-controls></a-entity>
    <a-entity id="rightHand" raycaster="showLine: true"
                line="color: white; opacity: 0.25" laser-controls="hand:right"
                teleport-controls="cameraRig: #cameraRig;
                                    teleportOrigin: #head;
                                    button: trackpad;
                                    curveShootingSpeed: 30;"
                laser-controls></a-entity>
</a-entity>
```

Teleport-controls as an attribute, comes from a component that needs to be linked in <head> like:

```
<head>
    ...
    <script src="https://rawgit.com/fernandojsg/aframe-teleport-controls/master/dist/aframe-teleport-controls.min.js"></script>
    ...
</head>
```

#### Component
A-Frame has a lot of open-sourse components out there, they are basically libraries of A-Frame. You can easily find them online. For this project, the components are imported like:
```
<head>
    <title>NCAA VR DataVis</title>
    <script src="//aframe.io/releases/0.8.2/aframe.min.js"></script>
    
    <script src="https://unpkg.com/aframe-event-set-component@^4.0.0/dist/aframe-event-set-component.min.js"></script>
    <script src="https://rawgit.com/fernandojsg/aframe-teleport-controls/master/dist/aframe-teleport-controls.min.js"></script>
    <script src="https://rawgit.com/protyze/aframe-curve-component/master/dist/aframe-curve-component.min.js"></script>
    <script src="https://rawgit.com/bryik/aframe-bmfont-text-component/master/dist/aframe-bmfont-text-component.js"></script>
    
    <script src="https://d3js.org/d3.v5.min.js"></script>
</head>
```
#### D3 Data Manipulation
Since we have the A-Frame basically in the form of DOM, d3 can be used to easily manipulate the elements based on a large amount of data and make them interactable.

Here is one example of doing so:
```
const aScene = d3.select('a-scene');

const aEntity = aScene.append('a-entity')
                        .attr('id', 'whole')
                        .attr('position', '0 0 -15');

...

d3.csv('2017_season_detailed_cleaned.csv').then(function(data){

    ...
    
    aEntity.selectAll('.team')
                    .data(data)
                    .enter()
                    .append('a-cylinder')
                        .attr('id', (d) => d.id)
                        .attr('class', 'team')
                        .attr('segments-radial', (d) => {
                                if (conditionA){
                                    return 3;
                                } else{
                                    return 4;
                                }
                            })
                        .attr('scale', (d) => {
                                scaleFactor = scale_normal;
                                scaleFactor *= seed_impact_factor(d.seed);
                                return `${scaleFactor} ${scaleFactor} ${scaleFactor}`;
                            })
                        ...
                        .on('mouseenter', (d) => {
                                this.setAttribute('opacity', '0.5');
                            })
                        .on('mouseleave', (d) => {
                                this.setAttribute('opacity', '0.5');
                            })
                        ...
    
    ...
    
}

...
```

Happy coding!


## Extras
### Created Metrics
[Win Chance Percentage](https://public.tableau.com/views/NCAAB-aFrame/WinPCTChange?:embed=y&:display_count=yes&publish=yes)

[Transition Offense](https://public.tableau.com/profile/hope.tambala#!/vizhome/NCAAB-aFrame/TransitionOffense)
