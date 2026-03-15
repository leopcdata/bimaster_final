import logging
import pandas as pd

from config import (
    INPUT_FOLDER,
    RESULTS_FOLDER,
    RUN_BENCHMARK,
    DEFAULT_EXECUTION_MODE,
)
from benchmark import (
    run_groups_parallel,
    run_groups_sequential,
    flatten_group_matches,
)
from utils.db_utils import fetch_data
from utils.summary import write_summary_excel
from utils.io_utils import select_input_file, get_country_code, build_output_path
from utils.metrics import build_metrics_df
from utils.process_utils import (
    prepare_group_jobs,
    append_unmatched_companies,
    finalize_details,
)


def choose_execution(group_jobs):
    if RUN_BENCHMARK:
        logging.info("Running parallel benchmark")
        parallel_matches_dict, parallel_timings, parallel_total = run_groups_parallel(group_jobs)

        logging.info("Running sequential benchmark")
        sequential_matches_dict, sequential_timings, sequential_total = run_groups_sequential(group_jobs)

        if parallel_total <= sequential_total:
            logging.info("Using PARALLEL results (%.2fs vs %.2fs)", parallel_total, sequential_total)
            return (
                parallel_matches_dict,
                flatten_group_matches(parallel_matches_dict),
                {
                    "parallel_total": parallel_total,
                    "parallel_timings": parallel_timings,
                    "sequential_total": sequential_total,
                    "sequential_timings": sequential_timings,
                    "selected_mode": "parallel",
                }
            )

        logging.info("Using SEQUENTIAL results (%.2fs vs %.2fs)", sequential_total, parallel_total)
        return (
            sequential_matches_dict,
            flatten_group_matches(sequential_matches_dict),
            {
                "parallel_total": parallel_total,
                "parallel_timings": parallel_timings,
                "sequential_total": sequential_total,
                "sequential_timings": sequential_timings,
                "selected_mode": "sequential",
            }
        )

    if DEFAULT_EXECUTION_MODE == "parallel":
        logging.info("Running in PARALLEL mode")
        matches_dict, timings, total = run_groups_parallel(group_jobs)
        return matches_dict, flatten_group_matches(matches_dict), {
            "selected_mode": "parallel",
            "parallel_total": total,
            "parallel_timings": timings,
        }

    logging.info("Running in SEQUENTIAL mode")
    matches_dict, timings, total = run_groups_sequential(group_jobs)
    return matches_dict, flatten_group_matches(matches_dict), {
        "selected_mode": "sequential",
        "sequential_total": total,
        "sequential_timings": timings,
    }


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    input_file = select_input_file(INPUT_FOLDER)
    country_code = get_country_code()

    logging.info("Reading input file: %s", input_file)
    df_input = pd.read_excel(input_file)
    df_input["Company"] = df_input["Company"].astype(str).str.strip()

    logging.info("Fetching database data for country code %s", country_code)
    df_db = fetch_data(country_code)

    logging.info("Preparing group jobs")
    group_jobs = prepare_group_jobs(df_db, df_input)

    group_matches_dict, matches, perf_info = choose_execution(group_jobs)
    matches = [m for m in matches if m is not None]

    logging.info("Appending unmatched companies")
    df_details = append_unmatched_companies(matches, df_input)

    logging.info("Building summary and final details")
    df_summary, df_details = finalize_details(df_details, df_input)

    metrics_df = build_metrics_df(perf_info, group_matches_dict, df_input, df_summary)

    output_file = build_output_path(RESULTS_FOLDER, input_file)
    write_summary_excel(df_summary, df_details, output_file, metrics_df=metrics_df)

    print("Wrote Summary, Details and Metrics sheets to:", output_file)
    print("\nExecution summary:")
    print(perf_info)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")