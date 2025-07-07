# H2-Ammonia-Simulator: Green Ammonia LCOA Calculator

A Python-based simulator for calculating the Levelized Cost of Ammonia (LCOA) from green hydrogen, enabling economic feasibility analysis for sustainable energy projects.

## About the Creator

This project was developed by **[HWAN-OH](https://github.com/HWAN-OH)**.

He is a developer passionate about building digital systems that model and solve complex, real-world challenges. His work focuses on creating 'digital twins' and specialized AI personas, transforming abstract data into tangible solutions.

## Project Philosophy: From Code to Digital Twin

The H2-Ammonia-Simulator is a direct result of this vision. It was created not just as a piece of code, but as a tangible step towards building dynamic models that reflect and solve complex real-world systems. The goal is to translate abstract data into concrete, actionable insights for a sustainable future.

This project shares its core philosophy with a larger vision: the **[MirrorMind Identity Protocol](https://github.com/HWAN-OH/MirrorMind-Identity-Protocol)**. If MirrorMind is the hub for designing versatile digital personas, the H2-Ammonia-Simulator is a real-world application of that concept—a specialized persona with deep expertise in energy economics. It demonstrates how a well-defined digital model can tackle specific, high-impact challenges.

## Overview

The **H2-Ammonia-Simulator** provides a streamlined tool to assess the economic viability of green ammonia production. By inputting key technical and financial parameters, users can model the entire value chain—from production and storage to transportation—to determine the final cost of delivering green ammonia to a specific demand center.

This project is designed for researchers, project developers, and policymakers to make data-driven decisions on investing in and deploying green ammonia technologies.

## Key Features

* **End-to-End Cost Analysis:** Calculates the Levelized Cost of Ammonia (LCOA), including CAPEX, OPEX, storage, and transportation costs.
* **Parameter-Driven Simulation:** Easily adjust key variables such as electrolyzer efficiency, electricity cost, and transportation distance through a centralized configuration.
* **Component-Based Costing:** Breaks down costs by major components like the Air Separation Unit (ASU), Haber-Bosch synthesis loop, and energy storage.
* **Clear Financial Outputs:** Generates key financial metrics, providing a clear summary of the project's economic profile.

## How to Use

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/HWAN-OH/H2-Ammonia-Simulator.git](https://github.com/HWAN-OH/H2-Ammonia-Simulator.git)
    cd H2-Ammonia-Simulator
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure your simulation:**
    Modify the parameters in `config.yml` to match your project's specifications.

4.  **Run the simulator:**
    ```bash
    python main.py
    ```

5.  **Review the results:**
    The output will be saved as a CSV file in the `results` directory.

## Contributing

Contributions are welcome. Please feel free to submit a pull request or open an issue to discuss potential improvements or new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
