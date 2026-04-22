# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#   loading.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#   By: orhernan <orhernan@student.42.fr>          +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#   Created: 2026/04/20 18:13:31 by orhernan          #+#    #+#              #
#   Updated: 2026/04/22 17:38:23 by orhernan         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import sys
from importlib import metadata


REQUIRED_PACKAGES = {
    "pandas": "Data manipulation",
    "numpy": "Numerical Computation",
    "matplotlib": "Visualization"
}

OPTIONAL_PACKAGES = {
    "requests": "Network access"
}


def check_dependencies() -> tuple[dict[str, str], list[str]]:
    installed: dict[str, str] = {}
    missing: list[str] = []

    for pkg in REQUIRED_PACKAGES:
        try:
            installed[pkg] = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            missing.append(pkg)

    return installed, missing


def check_optional_packages() -> dict[str, str]:
    optional_installed: dict[str, str] = {}

    for pkg in OPTIONAL_PACKAGES:
        try:
            optional_installed[pkg] = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            pass
    
    return optional_installed


def print_loading_status(
        installed: dict[str, str],
        missing: list[str],
        optional_installed: dict[str, str]
    ) -> None:
    print("LOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")
    
    for pkg, desc in REQUIRED_PACKAGES.items():
        if pkg in installed:
            print(f"[OK] {pkg} ({installed[pkg]}) - {desc} ready")
        else:
            print(f"[MISSING] {pkg}")

    for pkg, desc in OPTIONAL_PACKAGES.items():
        if pkg in optional_installed:
            print(f"[OK] {pkg} ({installed[pkg]}) - {desc} ready")
        else:
            print(f"[MISSING] {pkg} - not required")

    print()
    
    if missing:
        print("ERROR: Missing required dependencies.")
        print("To enter the construct with pip, run:")
        print("  pip install -r requirements.txt")
        print("To enter the construct with Poetry, run:")
        print("  poetry install")
        sys.exit(1)


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


def run_analysis(optional_installed: dict[str, str]) -> None:
    import pandas as pd

    url = "https://dummyjson.com/products?limit=50"
    data_points = []
    world = ""

    if "requests" in optional_installed:
        import requests
        
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
        
        if not data_points:
            print(f"Generating Matrix data...")
            data_points = generate_matrix_data(1000)
            print(f"Generated {len(data_points)} data points.")
            world = "Matrix"

    print(f"Analyzing {world} data...")
    print(f"Processing {len(data_points)} data points...")
    df = pd.DataFrame(data_points, columns=['price', 'rating'])
    save_data_viz(df)

def main() -> None:
    try:
        installed, missing = check_dependencies()
        optional_installed = check_optional_packages()
        print_loading_status(installed, missing, optional_installed)
        run_analysis(optional_installed)
    except Exception as e:
        print(f"CRITICAL ERROR: Matrix glitch detected. {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()