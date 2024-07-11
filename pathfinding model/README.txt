# Emergency Services Pathfinding in Heidelberg, Germany

## Basic Project Description
This project aims to enhance the efficiency of emergency services in Heidelberg, Germany, by implementing and evaluating pathfinding algorithms to find the shortest path from any point in the city to the nearest hospital.

## Installation Instructions
1. Ensure you have Python installed on your system.
2. Install the required dependencies by running:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
To run the project and find the shortest path to the nearest hospital:

1. Collect and process data:
    ```bash
    python DataCollection.py
    ```

2. Map the city graph and add hospitals:
    ```bash
    python graph_mapping.py
    ```

3. Run the pathfinding script and provide the starting location when prompted:
    ```bash
    python pathfinding.py
    ```

### Example Input
Enter the starting location (e.g., 'Some Building, Heidelberg, Germany'): Boxberg, Heidelberg, Germany 

The script will output the nearest hospital and the shortest path using both Dijkstra's and A* algorithms.
