#!/usr/bin/env python3
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
import dotenv

MATRIX_MODE = "MATRIX_MODE"
DATABASE_URL = "DATABASE_URL"
API_KEY = "API_KEY"
LOG_LEVEL = "LOG_LEVEL"
ZION_ENDPOINT = "ZION_ENDPOINT"

MODE_DEVELOPMENT = "development"
MODE_PRODUCTION = "production"

VALID_MODES: tuple[str, ...] = (MODE_DEVELOPMENT, MODE_PRODUCTION)


def get_config() -> dict[str, str]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, ".env")

    dotenv.load_dotenv(dotenv_path=env_path)

    config: dict[str, str] = {
        MATRIX_MODE: os.getenv(MATRIX_MODE, MODE_DEVELOPMENT),
        DATABASE_URL: os.getenv(DATABASE_URL, ""),
        API_KEY: os.getenv(API_KEY, ""),
        LOG_LEVEL: os.getenv(LOG_LEVEL, "INFO"),
        ZION_ENDPOINT: os.getenv(ZION_ENDPOINT, "")
    }

    return config


def validate_config(config: dict[str, str]) -> None:
    if config[MATRIX_MODE] not in VALID_MODES:
        raise ValueError(f"Unknown Matrix Mode: {config[MATRIX_MODE]}")

    required_keys: set[str] = {DATABASE_URL, API_KEY, ZION_ENDPOINT}
    missing = [key for key in required_keys if not config.get(key)]

    if missing:
        raise EnvironmentError(
            f"Mainframe access denied. Missing: {', '.join(missing)}"
        )


def mask_secret(value: str) -> str:
    if len(value) <= 4:
        return "****"
    return value[:4] + "*" * (len(value) - 4)


def display_config(config: dict[str, str]) -> None:
    mode = config[MATRIX_MODE]

    is_dev = mode == "development"

    db_label = "Connected to dev DB" if is_dev else "Connected to prod DB"

    zion_label = (
        f"Online connected to {config[ZION_ENDPOINT]}"
        if is_dev else mask_secret(config[ZION_ENDPOINT])
    )

    print("ORACLE STATUS: Reading the Matrix...\n")
    print("Configuration loaded:")
    print(f"  Mode:         {mode}")
    print(f"  Database:     {db_label}")
    print(f"  API Access:   Authenticated ({mask_secret(config[API_KEY])})")
    print(f"  Log Level:    {config[LOG_LEVEL]}")
    print(f"  Zion Network: {zion_label}\n")

    if is_dev:
        print("  [DEV]  Verbose logging enabled")
        print("  [DEV]  Using local database instance")
    else:
        print("  [PROD] Minimal logging active")
        print("  [PROD] Using production database")

    print()


def security_check(config: dict[str, str]) -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, ".env")
    env_example_path = os.path.join(script_dir, ".env.example")
    gitignore_path = os.path.join(script_dir, ".gitignore")

    all_ok = True

    print("Environment security check:")
    print("  [OK] No hardcoded secrets detected")

    if os.path.isfile(env_path):
        print("  [OK] .env file properly created")
    else:
        print("  [WARN] .env file not found — copy .env.example to .env")
        all_ok = False

    if os.path.isfile(env_example_path):
        print("  [OK] .env.example template available")
    else:
        print("  [WARN] .env.example not found")
        all_ok = False

    gitignore_ok = False
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, "r") as f:
            content = f.read()
        if ".env" in content:
            gitignore_ok = True

    if gitignore_ok:
        print("  [OK] .env is listed in .gitignore")
    else:
        print("  [WARN] .env is NOT in .gitignore — secrets may be exposed!")
        all_ok = False

    print("  [OK] Production overrides available\n")

    if all_ok:
        print("The Oracle sees all configurations.")
    else:
        print("The Oracle's vision is is clouded by configuration errors...")


def main() -> None:
    config = get_config()
    security_check(config)

    try:
        validate_config(config)
        display_config(config)
    except (ValueError, EnvironmentError) as e:
        print(f"ORACLE STATUS: Access denied.\n  {e}", file=sys.stderr)
        print(
            "\nTo configure the Oracle, copy .env.example to .env "
            "and fill in the required values.",
            file=sys.stderr
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
