# Ecoloop - Circular Design & Material Lifecycle Engine

Ecoloop is a high-performance sustainability intelligence dashboard designed to model circular product lifecycles. It translates complex material logistics, feedstock parameters, and end-of-life recycling coefficients into circularity indexes and Scope 3 carbon offsets.

The application implements the mathematical standards defined by the **Ellen MacArthur Foundation (EMF)** for product circularity audits, helping product teams and engineers design waste-free products and verify manufacturing compliance under global standards like the EU Ecodesign Regulation (ESPR).

## Key Features
 
- **Circularity Index (MCI) Calculations:** Automatically computes Material Circularity Index (MCI) and Linear Flow Index (LFI) based on material weights, recycled content, and end-of-life recovery rates.
- **Supply Chain Carbon Modeling:** Tracks greenhouse gas sourcing offsets (recycled vs. virgin material sourcing coefficients) and logistics transport emissions.
- **Dynamic Bill of Materials (BOM) Editor:** Interactive UI sliders to adjust individual component parameters in real time and see updates on the composition and disposal mass charts.
- **Design Optimization Simulator:** Programmatic lifecycle simulator that models transitions to sustainable shipping modes, extended product durability, and optimal recycling rates.
- **Compliance Export:** Generates and exports comprehensive CSV sourcing audit reports suitable for regulatory reviews.

## Mathematical Model (EMF Standard)

The engine calculates metrics utilizing the following formulas:
- **Virgin Material Sourcing Fraction (V):**
  $$V = \sum M_i \times (1 - R_{in,i})$$
- **Total Lifecycle Waste (W):**
  $$W = \text{Process Losses}_{\text{Input}} + \text{Process Losses}_{\text{EoL}} + \text{Landfilled Waste}$$
- **Linear Flow Index (LFI):**
  $$LFI = \frac{V + W}{2M}$$
- **Material Circularity Index (MCI):**
  $$MCI = 1 - LFI \times F(U)$$
  *(where $F(U)$ is the product longevity utility utility adjustment factor)*

## Technical Stack

- **Backend Logic & UI:** Python, Streamlit
- **Data Visualizations:** Plotly Express, Plotly Graph Objects
- **Data Manipulation:** Pandas

## Installation and Execution

To run this project locally, ensure you have Python 3.8+ installed.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mekhushi/Ecoloop.git
   cd Ecoloop
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the dashboard:**
   ```bash
   streamlit run app.py
   ```
