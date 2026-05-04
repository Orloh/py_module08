# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#   oracle.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#   By: orhernan <orhernan@student.42.fr>          +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#   Created: 2026/04/28 16:10:06 by orhernan          #+#    #+#              #
#   Updated: 2026/04/28 16:10:06 by orhernan         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import os
import sys
from dotenv import load_dotenv

VALID_MODES: tuple[str, ...] = ("development", "production")

def get_config() -> dict[str, str]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, ".env")
    
    load_dotenv(dotenv_path=env_path)
    print("we are here")
    config: dict[str, str] = {
        "mode": os.getenv("MATRIX_MODE", "development"),
        "db_url": os.getenv("DATABASE_URL", ""),
        "api_key": os.getenv("API_KEY", ""),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "zion_url": os.getenv("ZION_ENDPOINT", "")
    }

    print(config)

    if config["mode"] not in VALID_MODES:
        raise ValueError(f"Unknown Matrix Mode: {config['mode']}")

    required_keys: set[str] = {"db_url", "api_key", "zion_url"}
    missing = [key for key in required_keys if not config.get(key)]

    if missing:
        raise EnvironmentError(
            f"Mainframe access denied. Missing: {', '.join(missing)}"
        )
    
    return config

def main() -> None:

    config = get_config()
    print(config)


if __name__ == "__main__":
    main()