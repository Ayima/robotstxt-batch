# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import csv

OUTPUT_FILE_NAME = "test.results.csv"


def main(robots_file, url_file, user_agent):
    urls = _load_url_file(url_file)
    print(
        f"Loaded {len(urls)} pages to test "
        f"against robots file: {robots_file} "
        f"with user agent: {user_agent}"
    )
    batch_lookup_results = _run_batch_lookup(urls, robots_file, user_agent)
    _write_results(batch_lookup_results, OUTPUT_FILE_NAME)
    print(f"Wrote results to {OUTPUT_FILE_NAME}")


def _run_batch_lookup(urls, robots_file, user_agent):
    results = []
    for url in urls:
        terminal_lookup_output = _run_url_lookup(url, robots_file, user_agent)
        lookup_result = _parse_lookup_result(terminal_lookup_output)
        results.append(
            {"User-Agent": user_agent, "page": url, "robots_result": lookup_result}
        )
    return results


def _run_url_lookup(url, robots_file, user_agent):
    process = Popen(
        ["robots", robots_file, user_agent, f"'{url}'"], stdout=PIPE, stderr=PIPE
    )
    stdout, stderr = process.communicate()
    stdout = stdout.decode("utf-8")
    print(stdout.rstrip("\n"))
    if stderr:
        raise Exception(stderr)
    return stdout


def _parse_lookup_result(lookup_terminal_output):
    """
    Parse result ALLOWED or DISALOWED from terminal output

    e.g. user-agent 'GoogleBot' with URI 'https://example.com/page/1': DISALLOWED
    """
    parsed_res = lookup_terminal_output.replace("\n", "").strip().split()[-1]

    if parsed_res not in ("ALLOWED", "DISALLOWED"):
        raise ValueError(
            f"Invalid parsed result: {parsed_res} for terminal output:\n{lookup_terminal_output}"
        )
    return parsed_res


def _load_url_file(fp):
    with open(fp, "r") as f:
        urls = f.read().splitlines()

    urls = [url.strip() for url in urls if url.strip()]
    return urls


def _write_results(json_rows, output_file_name):
    column_names = list(json_rows[0].keys())
    with open(output_file_name, mode="w") as f:
        writer = csv.DictWriter(f, fieldnames=column_names)
        writer.writeheader()
        for row in json_rows:
            writer.writerow(row)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--robots-file", required=True, help="Local path to robots.txt file to test"
    )
    parser.add_argument(
        "--url-file", required=True, help="Local path to text file with pages to test"
    )
    parser.add_argument(
        "--user-agent",
        default="GoogleBot",
        help="User-Agent to use when running the test",
    )
    args = parser.parse_args()
    main(args.robots_file, args.url_file, args.user_agent)
