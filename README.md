# CSDA Final Project

Detecting Coordinated Troll Farm Activity on Reddit r/Conservative during the 2024 U.S. Election

## File Overview

- **reddit_analysis.yml**  
  Conda environment file for setting up the project dependencies.

- **conservative_sept_nov_2024_clean.csv**  
  Cleaned dataset ready for analysis.

- **suspicious_accounts_posting_patterns.csv**  
  CSV containing accounts flagged as suspicious based on posting patterns.

- **suspicious_accounts_network_analysis.csv**  
  CSV containing accounts flagged as suspicious based on network analysis.

- **Data_Extraction.ipynb**  
  Imports data from `.zst` files, cleans it, and exports to CSV.
  
- **posting_patterns_analysis.py**  
  Script for analyzing posting patterns in the dataset.

- **Network_and_High_Activity_Code.ipynb**
  Script doing the network analysis on the dataset.


## Setup

To create the environment:

```bash
conda env create -f reddit_analysis.yml
conda activate reddit_analysis
