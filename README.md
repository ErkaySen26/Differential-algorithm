# Power Generation Optimization Using Differential Evolution

## Project Description
This project implements a **Differential Evolution** (DE) algorithm to optimize power generation from multiple generators while minimizing fuel cost and adhering to constraints such as power limits and forbidden zones. The goal is to find the optimal power distribution that meets the total demand while keeping the cost as low as possible.

The problem is solved by adjusting the power output of each generator using DE, which is an evolutionary algorithm for global optimization problems.

## Technologies Used
- **Python 3.x**
- **NumPy** (For mathematical computations)

## Problem Definition
Each generator has:
- A cost function of the form: `Cost = a*P^2 + b*P + c`, where `P` is the power generated.
- Power limits: `P_min` and `P_max`, which restrict the range of power output.
- Forbidden zones: Specific ranges of power output where the generator cannot operate.

The objective is to minimize the total fuel cost, while ensuring that:
- The sum of power outputs from all generators equals the total demand.
- The power output from each generator stays within the limits and avoids forbidden zones.

## Features
- Optimization using **Differential Evolution** (DE).
- Constraints for power limits and forbidden zones for each generator.
- Calculates total fuel cost while minimizing it.

## Parameters
- **Total Demand:** 1263 MW
- **Population Size:** 25 (number of candidates in the population)
- **Maximum Generations:** 300
- **Scaling Factor (F):** 0.5
- **Crossover Rate (CR):** 0.8

## Installation
To run the project, follow these steps:
1. **Clone the repository:**
git clone https://github.com/ErkaySen26/shopping-app.git
2. **Navigate to the project directory:**
3. **Install the required Python packages:**
4. **Run the script:**
5. The program will output the optimal power distribution and the total fuel cost.
## Usage
The script will output:
- **Optimal Power Distribution (MW):** The power output for each generator.
- **Total Fuel Cost (R/h):** The total fuel cost for the current solution.
## Example Output
## Contributing
If you would like to contribute to this project, please feel free to fork the repository and submit a pull request with your improvements.

## License
This project is licensed under the MIT License.

