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
    load_dotenv()
    config: dict[str, str] = {
        "mode": os.getenv("MATRIX_MODE", "development"),
        "db_url": os.getenv("DATABASE_URL", ""),
        "apy_key": os.getenv("APY_KEY", ""),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "zion_url": os.getenv("ZION_ENDPOINT", "")
    }

    if config["mode"] not in VALID_MODES:
        raise ValueError(f"Unknown Matrix Mode: {config['mode']}")

    required_keys: set[str] = {"DATABASE_URL", "API_KEY", "ZION_ENDPOINT"}
    missing = [key for key in required_keys if not config[key]]

    if missing:
        raise EnvironmentError(
            f"Mainframe access denied. Missing: {', '.join(missing)}"
        )

def main() -> None:
    validate_cofig()
    

print(config)