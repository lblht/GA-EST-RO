This repository contains the code and test results for an algorithm developed as part of a thesis titled *"Evolutionary Optimization Algorithm for the Euclidean Steiner Tree Problem with Constraints"*.

## Included Files

- **problem_instances**:  
  Contains example problem instances, including `.png` files with obstacles and `.csv` files with terminals.
  
- **results**:  
  Contains the results of tested problem instances. Some of these instances are sourced from [GitHub - ManouRosenberg/SteinerTreeProblemWithSoftObstacles](https://github.com/ManouRosenberg/SteinerTreeProblemWithSoftObstacles) and are not included in this repository.

- **requirements.txt**:  
  A list of required Python libraries.

- **astar.py**:  
  Implementation of the A* pathfinding algorithm.

- **avoiding_steiner_points.py**:  
  Functions for finding Steiner points used to avoid obstacles.

- **config.py**:  
  Configuration file for setting algorithm parameters.

- **delauney_steiner_points.py**:  
  Functions for finding Steiner points using Delaunay triangulation and the Simpson (Torricelli) method.

- **genetic_algorithm.py**:  
  The main algorithm loop, implementing the genetic algorithm.

- **main.py**:  
  The main file for running the algorithm, printing, and plotting results.

- **poly_to_raster.py**:  
  Script to convert StOBGA problem instances to raster form for use in the algorithm.

- **tester.py**:  
  A script for testing multiple instances in a row, used for testing StOBGA instances.

- **utils.py**:  
  Utility functions and implementations of algorithms used throughout the codebase.

- **visuals.py**:  
  Script for plotting the results using matplotlib.

## How to Use

1. **Clone the Repository**  
   Clone this repository to your local machine.

 2. **Create a Virtual Environment**  
 Create a virtual environment for the project by running the following command.  
 - For Windows:
   ```
   python -m venv venv
   ```
 - For macOS/Linux:
   ```
   python3 -m venv venv
   ```
 After creating the virtual environment, activate it:
 - For Windows:
   ```
   .\venv\Scripts\activate
   ```
 - For macOS/Linux:
   ```
   source venv/bin/activate
   ```

3. **Install Required Packages**  
   Install the necessary Python libraries by running the following command:
   ```
   pip install -r requirements.txt
   ```

5. **Set Paths for Problem Instances**  
   In `main.py`, set the `obstacles_path` and `terminals_path` variables to point to your problem instance files.

6. **Configure Algorithm Parameters**  
   Open `config.py` and adjust the parameters as needed.

7. **Run the Algorithm**  
   Execute the algorithm by running the `main.py` script.
