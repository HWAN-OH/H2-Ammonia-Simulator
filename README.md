# H2-Ammonia Simulator

A techno-economic simulation tool for green and blue ammonia production, developed as part of the **MirrorMind** project — a next-generation AI framework designed to support strategic thinking, scenario modeling, and techno-economic validation in the energy transition space.

---

## 🔍 Purpose

This simulator performs reverse calculations to estimate the necessary investments, renewable capacity (solar/wind), and electrolyzer scaling to produce a **target quantity of low-carbon ammonia** (e.g., 100,000 tons per year).

It is designed for early-stage feasibility studies, investment modeling, and policy support in hydrogen-ammonia value chains.

---

## ⚙️ Key Features

- Reverse computation based on a fixed annual NH₃ production target
- Optimizes solar/wind/ESS ratio based on LCOA minimization
- Hydrogen buffer tank sizing to ensure minimum 60% uptime for ammonia plants
- Full-grid or hybrid electricity scenarios
- LCOA (Levelized Cost of Ammonia) breakdown
- IRR-driven revenue modeling (planned)
- Exportable PDF reports (coming soon)

---

## 📐 Assumptions & Data Sources

All default values and formulas are based on international hydrogen and ammonia techno-economic benchmarks:

| Parameter | Value | Source |
|----------|-------|--------|
| Hydrogen energy density | 33.33 kWh/kg | IEA (2022) |
| Hydrogen mass per Nm³ | 0.08988 kg | Standard ISO value |
| Electrolyzer types | ALC (AWE), PEM, SOEC | Typical system specs |
| Solar/Wind CF | 20~35% (input) | IRENA, regional data |
| CapEx/Opex for NH₃ plant | Input-driven | User-defined or market average |

---

## 📊 Use Cases

- Project finance & investment planning
- Pre-FEED techno-economic assessment
- Policy simulations (RE/IRR/carbon targets)
- Export competitiveness analysis

---

## 🧠 MirrorMind Background

This simulator is part of the **MirrorMind** system — an AI-powered simulation and identity modeling platform created by **Seunghwan Oh**, a strategic leader in the global hydrogen economy. MirrorMind enables users to build cognitive agents and analytical tools that assist in real-world scenario planning.

Learn more: [github.com/HWAN-OH](https://github.com/HWAN-OH)

---

## 👤 Author

Developed and maintained by:

**Seunghwan Oh**  
SVP, HD Hydrogen  
Former Strategy Lead at SK Group (Hydrogen Division)  
M.S. Industrial Engineering, Seoul National University  
[LinkedIn](https://www.linkedin.com/in/shoh1224/) / [GitHub](https://github.com/HWAN-OH)

---

*Last updated: July 2025*
