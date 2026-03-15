import time
import logging
from concurrent.futures import ThreadPoolExecutor
from utils.matching import process_group


def run_groups_sequential(group_jobs):
    start_total = time.perf_counter()
    timings = {}
    all_matches = {}

    for job_name, job in group_jobs.items():
        start = time.perf_counter()
        matches = process_group(
            df=job["df"],
            df_input=job["df_input"],
            acct_list_ids=job["acct_list_ids"],
            acct_list_names=job["acct_list_names"],
            output_map=job["output_map"],
            limit=job["limit"],
            extra_args=job["extra_args"],
        )
        elapsed = time.perf_counter() - start
        timings[job_name] = elapsed
        all_matches[job_name] = matches

        logging.info(
            "%s finished in %.2f seconds (sequential) | rows=%s | matches=%s",
            job_name,
            elapsed,
            len(job["df"]),
            len(matches),
        )

    total_elapsed = time.perf_counter() - start_total
    return all_matches, timings, total_elapsed


def run_groups_parallel(group_jobs):
    start_total = time.perf_counter()
    timings = {}
    all_matches = {}

    def timed_group(job_name, job):
        start = time.perf_counter()
        matches = process_group(
            df=job["df"],
            df_input=job["df_input"],
            acct_list_ids=job["acct_list_ids"],
            acct_list_names=job["acct_list_names"],
            output_map=job["output_map"],
            limit=job["limit"],
            extra_args=job["extra_args"],
        )
        elapsed = time.perf_counter() - start
        return job_name, matches, elapsed, len(job["df"])

    with ThreadPoolExecutor(max_workers=len(group_jobs)) as executor:
        futures = [executor.submit(timed_group, job_name, job) for job_name, job in group_jobs.items()]

        for future in futures:
            job_name, matches, elapsed, row_count = future.result()
            timings[job_name] = elapsed
            all_matches[job_name] = matches

            logging.info(
                "%s finished in %.2f seconds (parallel) | rows=%s | matches=%s",
                job_name,
                elapsed,
                row_count,
                len(matches),
            )

    total_elapsed = time.perf_counter() - start_total
    return all_matches, timings, total_elapsed


def flatten_group_matches(group_matches_dict):
    all_matches = []
    for matches in group_matches_dict.values():
        all_matches.extend(matches)
    return all_matches


def build_match_count_metrics(group_matches_dict):
    rows = []
    for group_name, matches in group_matches_dict.items():
        rows.append({
            "Group": group_name,
            "Match Count": len(matches),
        })
    return rows