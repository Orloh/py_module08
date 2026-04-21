# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    loading.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: orhernan <orhernan@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/04/20 18:13:31 by orhernan          #+#    #+#              #
#    Updated: 2026/04/21 17:42:19 by orhernan         ###   ########.fr        #
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

def fetch_rw_api_data(url: str) -> list[tuple[float, float]]:
    import requests

    response = requests.get(url, timeout=5)
    response.raise_for_status()
    api_data = response.json()
    data = [
        (float(p["price"]), float(p["rating"])) for p in api_data['products']
    ]
    return data

def generate_matrix_data(count: int = 1000) -> list[tuple[float, float]]:
    import numpy as np

    price = np.random.uniform(10, 2000, count)
    rating = np.random.uniform(1.0, 5.0, count)
    data = list(zip(price, rating))
    return data 

def save_data_viz(df: 'pd.DataFrame') -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    print("Generating visualization...")
    
    plt.figure(figsize=(8,6))
    ax = plt.axes()
    ax.set_facecolor("black")

    color_palette = ['#00FF41', '#008F11', '#003B00']
    colors = np.random.choice(color_palette, size=len(df))

    plt.scatter(
        df['price'],
        df['rating'],
        alpha=0.7,
        c=colors,
        edgecolors='black'
    )

    plt.title("Live Node Analysis (Price vs Rating)")
    plt.xlabel("Node Cost (Price)")
    plt.ylabel("Node Availability (Rating)")
    plt.grid(True, linestyle="--", alpha=0.5)

    file_name = "matrix_analysis.png"
    plt.savefig(file_name)

    print("Analysis complete!")
    print(f"Results saved to: {file_name}")

def run_analysis() -> None:
    import pandas as pd
    import requests

    url = "https://dummyjson.com/products?limit=50"
    data_points = []
    world = ""

    print("Trying to access the real world...")
    try:
        data_points = fetch_rw_api_data(url)
        print("Succesfuly loaded real world data.")
        print(f"Successfully loaded {len(data_points)} data points.")
        world = "Real World"
    except requests.exceptions.RequestException as e:
        print(f"NETWORK ERROR: Failed to fetch data from the real world. {e}")
        print()

        print(f"You're still inside The Matrix.")
        print()
        
        print(f"Generating Matrix data...")
        data_points = generate_matrix_data(1000)
        print(f"Generated {len(data_points)} data points.")
        world = "Matrix"

    print(f"Analyzing {world} data...")
    df = pd.DataFrame(data_points, columns=['price', 'rating'])
    save_data_viz(df)

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