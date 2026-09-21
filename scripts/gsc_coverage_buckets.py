#!/usr/bin/env python3
"""
gsc_coverage_buckets.py

Inspects every URL in a sitemap via the Google Search Console URL Inspection
API and groups the results by coverage state ("reason bucket"), so you can
see exactly which URLs sit behind each row in the Search Console
"Page indexing" report (e.g. "Crawled - currently not indexed") instead of
just the aggregate count.

Usage:
    python gsc_coverage_buckets.py \
        --site-url "https://aitoolalternatives.com/" \
        --sitemap-url "https://aitoolalternatives.com/sitemap.xml"

Auth:
    Expects a service-account JSON key with access to the GSC property,
    either at the path in GSC_SERVICE_ACCOUNT_JSON (env var containing the
    raw JSON, used by the GitHub Actions workflow) or via
    --credentials-file pointing at a JSON key file on disk.

    The service account's email must be added as a user under
    Search Console > Settings > Users and permissions for this property
    (Full or Restricted is fine — inspection is read-only).

Notes on --site-url:
    Use the EXACT property identifier as it appears in Search Console:
      - Domain property:      sc-domain:aitoolalternatives.com
      - URL-prefix property:  https://aitoolalternatives.com/
    Check the property switcher in the top-left of Search Console to see
    which type this is. Using the wrong form returns a 403/404 from the API.
"""

import argparse
import json
import os
import sys
import time
from collections import defaultdict
from xml.etree import ElementTree as ET

import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def load_credentials(credentials_file: str | None):
    if credentials_file:
        return service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES
        )
    raw = os.environ.get("GSC_SERVICE_ACCOUNT_JSON")
    if not raw:
        sys.exit(
            "No credentials found. Pass --credentials-file or set "
            "GSC_SERVICE_ACCOUNT_JSON."
        )
    info = json.loads(raw)
    return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)


def fetch_sitemap_urls(sitemap_url: str) -> list[str]:
    """Fetches a sitemap (or sitemap index, one level deep) and returns URLs."""
    resp = requests.get(sitemap_url, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)

    # Sitemap index: recurse one level into each child sitemap.
    sitemap_locs = [
        el.text.strip()
        for el in root.findall(".//sm:sitemap/sm:loc", SITEMAP_NS)
        if el.text
    ]
    if sitemap_locs:
        urls = []
        for loc in sitemap_locs:
            urls.extend(fetch_sitemap_urls(loc))
        return urls

    return [
        el.text.strip()
        for el in root.findall(".//sm:url/sm:loc", SITEMAP_NS)
        if el.text
    ]


def inspect_url(service, site_url: str, page_url: str, retries: int = 3) -> dict:
    body = {"inspectionUrl": page_url, "siteUrl": site_url}
    for attempt in range(1, retries + 1):
        try:
            result = service.urlInspection().index().inspect(body=body).execute()
            return result.get("inspectionResult", {})
        except Exception as e:
            if attempt == retries:
                return {"error": str(e)}
            time.sleep(2 * attempt)
    return {"error": "unreachable"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-url", required=True, help="GSC property identifier")
    parser.add_argument(
        "--sitemap-url", required=True, help="Sitemap (or sitemap index) URL"
    )
    parser.add_argument(
        "--credentials-file",
        default=None,
        help="Path to service-account JSON key (falls back to "
        "GSC_SERVICE_ACCOUNT_JSON env var)",
    )
    parser.add_argument(
        "--output",
        default="gsc_coverage_report.json",
        help="Where to write the full per-URL JSON report",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only inspect the first N URLs (useful for a quick test run)",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=1.0,
        help="Seconds to sleep between requests (API quota is limited)",
    )
    args = parser.parse_args()

    creds = load_credentials(args.credentials_file)
    service = build("searchconsole", "v1", credentials=creds)

    print(f"Fetching sitemap: {args.sitemap_url}")
    urls = fetch_sitemap_urls(args.sitemap_url)
    urls = sorted(set(urls))
    if args.limit:
        urls = urls[: args.limit]
    print(f"Found {len(urls)} URLs to inspect.\n")

    buckets = defaultdict(list)
    per_url_results = {}

    for i, url in enumerate(urls, 1):
        result = inspect_url(service, args.site_url, url)
        per_url_results[url] = result

        index_status = result.get("indexStatusResult", {})
        verdict = index_status.get("verdict", "UNKNOWN")
        coverage_state = index_status.get("coverageState", "No coverage state")

        if "error" in result:
            bucket_key = f"ERROR: {result['error'][:80]}"
        else:
            bucket_key = f"{verdict} — {coverage_state}"

        buckets[bucket_key].append(url)

        print(f"[{i}/{len(urls)}] {bucket_key}  <-  {url}")
        time.sleep(args.sleep)

    with open(args.output, "w") as f:
        json.dump(per_url_results, f, indent=2)
    print(f"\nFull per-URL results written to {args.output}")

    print("\n" + "=" * 70)
    print("COVERAGE BUCKETS")
    print("=" * 70)
    for bucket_key, bucket_urls in sorted(
        buckets.items(), key=lambda kv: -len(kv[1])
    ):
        print(f"\n{bucket_key}  ({len(bucket_urls)} URLs)")
        # Print up to 15 example URLs per bucket, plus a path-pattern hint
        for u in bucket_urls[:15]:
            print(f"  - {u}")
        if len(bucket_urls) > 15:
            print(f"  ... and {len(bucket_urls) - 15} more")

    # Quick path-pattern summary to spot-check for systemic issues
    print("\n" + "=" * 70)
    print("PATH-SEGMENT BREAKDOWN FOR THE LARGEST NOT-INDEXED BUCKET")
    print("=" * 70)
    not_indexed_buckets = {
        k: v for k, v in buckets.items() if "PASS" not in k.upper()
    }
    if not_indexed_buckets:
        biggest_key = max(not_indexed_buckets, key=lambda k: len(not_indexed_buckets[k]))
        segment_counts = defaultdict(int)
        for u in not_indexed_buckets[biggest_key]:
            path = u.split("aitoolalternatives.com", 1)[-1]
            first_segment = path.strip("/").split("/")[0] if path.strip("/") else "(root)"
            segment_counts[first_segment] += 1
        print(f"For bucket: {biggest_key}\n")
        for seg, count in sorted(segment_counts.items(), key=lambda kv: -kv[1]):
            print(f"  /{seg}/  -> {count} URLs")


if __name__ == "__main__":
    main()
