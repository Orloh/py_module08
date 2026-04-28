# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#   construct.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#   By: orhernan <orhernan@student.42.fr>          +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#   Created: 2026/04/20 17:29:01 by orhernan          #+#    #+#              #
#   Updated: 2026/04/21 16:24:55 by orhernan         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import sys
import os
import site


def is_virtual_env() -> bool:
    return sys.prefix != sys.base_prefix


def print_outside_construct() -> None:
    print("MATRIX STATUS: You're still plugged in")

    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()

    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()

    print("To enter the construct, run:")
    print("python -m venv my_venv")
    print("source my_venv/bin/activate # On Unix")
    print("my_venv\\Scripts\\activate # On Windows")
    print()

    print("Then run this program again.")


def print_inside_construct() -> None:
    env_path = sys.prefix
    env_name = os.path.basename(env_path)

    try:
        packages_path = site.getsitepackages()[0]
    except AttributeError:
        packages_path = os.path.join(
            env_path,
            "lib",
            f"python{sys.version_info.major}.{sys.version_info.minor}",
            "site-packages"
        )

    print("MATRIX STATUS: Welcome to the construct")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {env_name}")
    print(f"Environment Path: {env_path}")
    print()

    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting the global system.")
    print()

    print("Package installation path:")
    print(packages_path)


def main() -> None:
    try:
        if is_virtual_env():
            print_inside_construct()
        else:
            print_outside_construct()
    except Exception as error:
        print(f"CRITICAL ERROR: Data stream corrupted. {error}")

    print(site.getsitepackages())


if __name__ == "__main__":
    main()
