"""Supabase client wrapper. Uses the anon key for everything — see
docs/decisions/0002-anon-key-no-rls.md for why that's an acceptable trade-off
for this project's 100% public data."""

import os
from functools import lru_cache


@lru_cache(maxsize=1)
def get_client():
    from supabase import create_client

    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_KEY"]
    return create_client(url, key)
