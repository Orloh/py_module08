# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    loading.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: orhernan <orhernan@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/04/20 18:13:31 by orhernan          #+#    #+#              #
#    Updated: 2026/04/20 19:08:06 by orhernan         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
from importlib import metadata

REQUIRED_PACKAGES = {
    "pandas": "Data manipulation",
    "numpy": "Numerical Computation",
    "requests": "Network access",
    "matplotlib": "Visualization"
}

def check_dependencies() -> tuple[dict[str, str], list[str]]:
    installed = {}
    missing = []

    for pkg in REQUIRED_PACKAGES:
        try:
            installed[pkg] = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            missing.append(pkg)

    return installed, missing

def print_loading_status(installed: dict[str, str], missing: list[str]) -> None:
    print("LOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")
    
    for pkg in REQUIRED_PACKAGES:
        if pkg in installed:
            print(f"[OK] {pkg} ({installed[pkg]})")
        else:
            print(f"[MISSING] {pkg}")
            
    print() # Empty line for formatting
    
    if missing:
        print("ERROR: Missing required dependencies.")
        print("To enter the construct with pip, run:")
        print("  pip install -r requirements.txt")
        print("To enter the construct with Poetry, run:")
        print("  poetry install")
        sys.exit(1)
        
    for pkg, desc in REQUIRED_PACKAGES.items():
        if pkg in installed:
            print(f"{desc} ready")
    print()

def run_analysis() -> None:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import requests

    print("Accessing external Matrix nodes via API...")
    url = "https://dummyjson.com/products?limit=50"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        api_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"NETWORK ERROR: Failed to fetch data from the API. {e}")
        return
    
    print(f"Successfully loaded {len(api_data['products'])} data points.")
    
    print("Analyzing Matrix data...")
    
    df = pd.DataFrame(api_data['products'])

    color_palette = ['#00FF41', '#008F11', '#003B00', 'cyan', 'purple']
    np.random.seed(42)
    random_colors = np.random.choice(color_palette, size=len(df))

    print("Generating visualization...")
    plt.figure(figsize=(8,6))

    plt.scatter(
        df['price'],
        df['rating'],
        alpha=0.7,
        c=random_colors,
        edgecolors='black'
    )

    plt.title("Live Matrix Node Analysis (Price vs Rating)")
    plt.xlabel("Node Cost (Price)")
    plt.ylabel("Node Availability (Rating)")
    plt.grid(True, linestyle="--", alpha=0.5)

    file_name = "matrix_analysis.png"
    plt.savefig(file_name)

    print("Analysis complete!")
    print(f"Results saved to: {file_name}")

def main() -> None:
    try:
        installed, missing = check_dependencies()
        print_loading_status(installed, missing)
        run_analysis()
    except Exception as e:
        print(f"CRITICAL ERROR: Matrix glitch detected. {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()