# CSDA Final Project

Detecting Coordinated Troll Farm Activity on Reddit r/Conservative during the 2024 U.S. Election

## File Overview

- **Data_Extraction.ipynb**  
  Imports data from `.zst` files, cleans it, and exports to CSV.

- **conservative_sept_nov_2024_clean.csv**  
  Cleaned dataset ready for analysis.

- **posting_patterns_analysis.py**  
  Script for analyzing posting patterns in the dataset.

- **suspicious_accounts_posting_patterns.csv**  
  CSV containing accounts flagged as suspicious based on posting patterns.

- **reddit_analysis.yml**  
  Conda environment file for setting up the project dependencies.

## Setup

To create the environment:

```bash
conda env create -f reddit_analysis.yml
conda activate reddit_analysis
