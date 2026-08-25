# Test-

## Travelpayouts API connectivity test

`test_travelpayouts.py` checks whether this environment can reach the
Travelpayouts API.

```bash
pip install requests
python3 test_travelpayouts.py
```

It tests two public endpoints that need no API token (autocomplete,
airlines reference data). To also test an authenticated endpoint (flight
prices), set `TRAVELPAYOUTS_TOKEN` to an API token from your
[Travelpayouts affiliate account](https://www.travelpayouts.com/programs/100/tools/api):

```bash
TRAVELPAYOUTS_TOKEN=your_token_here python3 test_travelpayouts.py
```

Exit code `0` means all tests passed.
