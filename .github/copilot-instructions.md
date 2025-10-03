# Copilot Instructions for PL-Project

## Project Overview
This project analyzes Fantasy Premier League (FPL) data and optimizes team selection using Python, Jupyter notebooks, and linear programming (PuLP). It fetches, processes, and enriches player and fixture data from the FPL API, then applies custom metrics and optimization to select the best team under real-world constraints.

## Key Components
- **`fonctions.py`**: Contains core data enrichment and transfer analysis functions. These functions fetch player match histories and compute advanced stats (e.g., xGI, ICT, points per cost) using FPL API endpoints.
- **Jupyter Notebooks (`data.ipynb`, `FT.ipynb`, `optim1.ipynb`, `optim2.ipynb`, `sandbox.ipynb`)**: Orchestrate data loading, transformation, visualization, and optimization workflows. Notebooks are the main entry points for analysis and experimentation.
- **Parquet Files (`df_players.parquet`, `df_positions.parquet`, `df_teams.parquet`)**: Store processed dataframes for fast reloading and sharing between notebooks.

## Data Flow
1. **Fetch raw data** from FPL API (`bootstrap-static`, `fixtures`, `element-summary`).
2. **Transform and enrich** data in `data.ipynb` using `fonctions.py` utilities.
3. **Persist processed data** to Parquet files for reuse.
4. **Analyze and optimize** team selection in `FT.ipynb` and optimization notebooks using PuLP.

## Developer Workflows
- **Run notebooks** in order: Start with `data.ipynb` to generate and save Parquet files, then use `FT.ipynb` or optimization notebooks for analysis.
- **Update enrichment logic** in `fonctions.py` if new metrics or API fields are needed.
- **Debugging**: Print statements are used for error handling in API calls. Check for zero-filled columns if API errors occur.
- **Testing**: No formal test suite; validate changes by running notebooks and inspecting outputs.

## Project-Specific Patterns
- **API Integration**: All player and fixture data is fetched live from the FPL API. Functions handle missing or failed requests by filling with zeros and printing errors.
- **Data Enrichment**: Custom columns (e.g., `points_per_cost`, `ict_index`, `fdr_next_6`, `total_points_last_per_xGI_last`) are added to player dataframes for advanced analysis.
- **Optimization**: Team selection uses PuLP with constraints on budget, positions, and max players per team. See `FT.ipynb` for example constraints and objective setup.
- **Visualization**: Uses matplotlib, seaborn, and plotly for exploratory analysis and result presentation.

## Conventions & Tips
- **Column Naming**: Consistent, descriptive names (e.g., `web_name`, `ict_index`, `fdr_next_6`).
- **DataFrame Indexing**: Player dataframes are indexed by `id` for fast lookups.
- **Error Handling**: API failures are handled gracefully; check console output for details.
- **Reproducibility**: Always rerun `data.ipynb` after changing enrichment logic or API schema.

## Example: Adding a New Metric
1. Update `fonctions.py` to compute and add the metric to `df_players`.
2. Rerun `data.ipynb` to refresh Parquet files.
3. Use the new metric in analysis/optimization notebooks.

## Key Files
- `fonctions.py`: Data enrichment and transfer logic
- `data.ipynb`: Main data processing pipeline
- `FT.ipynb`: Team selection and optimization
- `df_players.parquet`, `df_positions.parquet`, `df_teams.parquet`: Cached data

---
For questions or missing details, review notebook comments or ask for clarification on specific workflows or metrics.
