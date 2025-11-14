# DDC Project

This repository contains the group work for the **DDC assignment**, covering reasoning with Assumption-Based Argumentation (ABA), relation-based argument mining, and gradual semantics visualization.  

It centralizes all deliverables: code (in Jupyter notebooks), datasets, models, and reports.  

---

## 📌 Project Overview

The project is divided into **three parts**, with a **dedicated web application** to visualize results from all parts.

### Part 1 – Reasoning with ABA (3 + 2 marks)
- Create an **ABA generator** with:
  - Definition of literals, rules, and assumptions
  - Contraries for assumptions
  - Conversion to non-circular and atomic frameworks
  - Generation of all arguments and attacks
  - Preference handling and normal/reverse attacks

---

### Part 2 – Relation-based Argument Mining (2 + 4 marks)
- **Scrape Kialo**: extract ~250 debates, perform data exploration  
- **Binary classification**: given two arguments, predict *Support* or *Attack*  
- Train and evaluate models using scraped data  
- Compare performance with literature

---

### Part 3 – Gradual Semantics: Weighted h-Categorizer (2 + 3 + 4 marks)
- Implement weighted **h-categorizer semantics** with convergence parameter ε  
- Represent weights as vectors in \[0,1\]^A  
- Visualize acceptability degree spaces and convex hulls  

> /!\ NOTE : In order to test the sliders of the visualization, please run the streamlit app located in **notebooks/3-grading/visualization/main.py**. Use the command `streamlit run notebooks/3-grading/visualization/main.py` after activating the conda environment.

---

## 🌐 Unified Visualization Platform
To centralize and visualize the results of all three parts, we developed a **web application** with:
- **Frontend**: [argument-frontend](https://github.com/edgar-demeude/argument-frontend)
- **Backend**: [argument-backend](https://github.com/edgar-demeude/argument-backend)
- **Live Demo**: [Arguments Visualisation on Vercel](https://arguments-visualisation.vercel.app/relations)

---

## 🚀 Quick Start Guide

### Prerequisites

- **Conda** installed (see Miniconda installation).
- **WSL** (if on Windows) with Ubuntu/Debian.
- **Git** installed and configured.

### 1. Clone the Repository

```bash
git clone git@github.com:edgar-demeude/DDC-project.git
cd DDC-project
```

### 3. Install System Dependencies (WSL / Linux)

These are required for Chrome / Selenium:

```bash
sudo apt update
sudo apt install -y wget unzip xvfb libxi6 libgconf-2-4
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

Optional: xvfb allows running Chrome headless with a virtual display if needed.

### 3. Set Up the Conda Environment
Create and activate the Conda environment:

```bash
conda env create --name ddc_project --file=environment.yml
```

Or manually:

```bash
conda create --name ddc_project python=3.11 -y
conda activate ddc_project
pip install -r requirements.txt
```

### 4. Install Additional Dependencies
For **Selenium** (if using Chrome):

- Download **ChromeDriver** and place it in `DDC-project/bin/`.
- Ensure Chrome is installed on your system.

### 5. Launch Jupyter Notebooks

```bash
jupyter notebook
```

Open the notebooks in notebooks/ in the order:

- `1_kialo_scraping.ipynb`
- `2_kialo_classification.ipynb`
- `3_h_categorizer.ipynb`

### 6. Environment Variables
Create a .env file in the root directory for sensitive data (e.g., API keys):

```bash
touch .env
```

Add your variables (e.g., `KIALO_API_KEY=your_key`).

## 🛠️ Tech Stack

- **Python** (Jupyter Notebooks)  
- **Pandas / NumPy / Scikit-learn** (data processing & ML)  
- **Transformers (HuggingFace)** (optional, advanced classifier)  
- **Matplotlib / Plotly** (visualization)  
- **Next.js + Vercel** (Part 1 ABA web app)

---

## 🚀 Roadmap

### Setup
- [x] Create central repo `DDC-project`  
- [x] Add base structure and README  

### Part 1 – ABA Generator (separate repo)
- [x] Set up Next.js project for ABA generator  
- [x] Deploy online application on Vercel  
- [x] Implement ABA generator
- [x] Provide usage instructions in the app

### Part 2 – Argument Mining (Part 2)
- [x] Implement Kialo scraping (`1_kialo_scraping.ipynb`)  
- [x] Perform data exploration (EDA)  
- [x] Preprocess arguments into pairs (`processed_pairs.csv`)  
- [x] Train and evaluate classifier (`2_classification_training.ipynb`)  
- [x] Save trained model(s) in `models/`  

### Part 3 – Gradual Semantics (Part 3)
- [x] Implement weighted h-categorizer semantics (`3_h_categorizer.ipynb`)  
- [x] Add convergence with ε  
- [x] Visualize convex hulls  

### Reporting & Finalization
- [x] Write **report.pdf** (≤15 pages, with figures and code excerpts)  
- [x] Write **contribution.pdf** (1 page, signed by all members)  
- [x] Package submission as `zip_submission.zip`  

---

## 👥 Collaboration Guidelines
- Use **branches per task** (`part2-data`, `part2-classifier`, `part3-semantics`, `report`)  
- Submit changes via **Pull Requests** → reviewed before merging into `main`  
- Keep **notebook outputs** (do not clear cells) to ease correction  
- Mention sources when using **open-source code**, and describe modifications  

---

## ✅ Deliverables
At submission, the repository must contain:
1. `report.pdf` – max 15 pages, complete answers  
2. `zip_submission.zip` – notebooks, data, models  
3. `contribution.pdf` – 1 page, signed, with member roles  

---
