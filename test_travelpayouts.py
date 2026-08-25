"""
Quick connectivity test for the Travelpayouts API.

Usage:
    python3 test_travelpayouts.py
    TRAVELPAYOUTS_TOKEN=xxxx python3 test_travelpayouts.py   # also tests an authenticated endpoint

Get a free API token at https://www.travelpayouts.com/programs/100/tools/api
(Affiliate account -> API tools -> Token).
"""

import os
import sys
import requests

TIMEOUT = 10


def check(name, method, url, **kwargs):
    print(f"\n[{name}]")
    print(f"  GET {url}")
    try:
        resp = method(url, timeout=TIMEOUT, **kwargs)
        print(f"  Status: {resp.status_code}")
        ct = resp.headers.get("Content-Type", "")
        body_preview = resp.text[:300]
        print(f"  Content-Type: {ct}")
        print(f"  Body preview: {body_preview}")
        ok = resp.ok
        print(f"  Result: {'OK' if ok else 'FAILED'}")
        return ok
    except requests.exceptions.RequestException as e:
        print(f"  Result: FAILED ({e})")
        return False


def main():
    results = {}

    # 1. Public endpoint, no API token required — proves basic network
    #    connectivity to Travelpayouts' infrastructure.
    results["autocomplete (public)"] = check(
        "Autocomplete (public, no token)",
        requests.get,
        "https://autocomplete.travelpayouts.com/places2",
        params={"term": "Bangkok", "locale": "en", "types[]": "city"},
    )

    # 2. Public static reference data — also token-free.
    results["airlines data (public)"] = check(
        "Data API: airlines.json (public, no token)",
        requests.get,
        "https://api.travelpayouts.com/data/en/airlines.json",
    )

    token = os.environ.get("TRAVELPAYOUTS_TOKEN")
    if token:
        # 3. Authenticated Data API call — needs a real token.
        results["latest prices (authenticated)"] = check(
            "Data API: latest prices (authenticated)",
            requests.get,
            "https://api.travelpayouts.com/v2/prices/latest",
            params={
                "currency": "usd",
                "origin": "BKK",
                "destination": "HKT",
                "token": token,
                "limit": 1,
            },
        )
    else:
        print(
            "\n[Data API: latest prices (authenticated)]\n"
            "  Skipped — set TRAVELPAYOUTS_TOKEN to also test an authenticated endpoint."
        )

    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)
    for name, ok in results.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")

    if not token:
        print("  SKIP  latest prices (authenticated) - no TRAVELPAYOUTS_TOKEN set")

    all_ok = all(results.values())
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
