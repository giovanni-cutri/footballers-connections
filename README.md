# Footballers Connections
 
Find the shortest path between two football players based on the teams they have played for using the breadth-first search algorithm.

Inspired by [this](https://cs50.harvard.edu/ai/2020/projects/0/degrees/) CS50 Project.

Data from [worldfootball.net](worldfootball.net).

# Usage

- Clone this repository to your local machine.
- Ensure that you have installed Python.
- Install the dependencies listed in *requirements.txt*.
  
  ````
  pip install -r requirements.txt
  ````
- Run *footballers_connections.py*.

You will be prompted to provide the Worldfootball URL of the initial player and the final player.

Alternatively, you can provide the aforementioned information as two command-line arguments, like this:

````
python footballers_connections.py [initial_player] [final_player]
````

# License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/giovanni-cutri/footballers-connections/blob/main/LICENSE) file for details.
