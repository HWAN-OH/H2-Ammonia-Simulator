H2-Ammonia-Simulator: Green Ammonia LCOA Calculator
A Python-based simulator for calculating the Levelized Cost of Ammonia (LCOA) from green hydrogen, enabling economic feasibility analysis for sustainable energy projects.

Overview
The H2-Ammonia-Simulator provides a streamlined tool to assess the economic viability of green ammonia production. By inputting key technical and financial parameters, users can model the entire value chain—from production and storage to transportation—to determine the final cost of delivering green ammonia to a specific demand center.

This project is designed for researchers, project developers, and policymakers to make data-driven decisions on investing in and deploying green ammonia technologies.

Key Features
End-to-End Cost Analysis: Calculates the Levelized Cost of Ammonia (LCOA), including CAPEX, OPEX, storage, and transportation costs.

Parameter-Driven Simulation: Easily adjust key variables such as electrolyzer efficiency, electricity cost, and transportation distance through a centralized configuration.

Component-Based Costing: Breaks down costs by major components like the Air Separation Unit (ASU), Haber-Bosch synthesis loop, and energy storage.

Clear Financial Outputs: Generates key financial metrics, providing a clear summary of the project's economic profile.

How to Use
Clone the repository:

git clone https://github.com/HWAN-OH/H2-Ammonia-Simulator.git
cd H2-Ammonia-Simulator

Install dependencies:

pip install -r requirements.txt

Configure your simulation:
Modify the parameters in config.yml to match your project's specifications.

Run the simulator:

python main.py

Review the results:
The output will be saved as a CSV file in the results directory.

Core Logic
The simulation integrates several established models and cost assumptions for green energy production. The core calculation process is as follows:

Hydrogen Production: Models the cost of producing green hydrogen via electrolysis.

Ammonia Synthesis: Calculates the costs associated with the Haber-Bosch process.

Storage & Transportation: Aggregates costs for ammonia storage and delivery to the target location.

Levelized Cost Calculation: Amortizes the total lifecycle costs over the project's lifetime to determine the final LCOA in $/tonne.

Contributing
Contributions are welcome. Please feel free to submit a pull request or open an issue to discuss potential improvements or new features.

License
This project is licensed under the MIT License. See the LICENSE file for details.
