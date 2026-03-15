import pandas as pd

def build_metrics_df(perf_info, group_matches_dict, df_input, df_summary):
    rows = []

    total_input_companies = df_input["Company"].dropna().astype(str).str.strip().nunique()
    not_found_count = (df_summary["ACCT LEVEL"] == "Customer not found").sum()
    found_count = total_input_companies - not_found_count

    found_pct = round((found_count / total_input_companies) * 100, 2) if total_input_companies else 0
    not_found_pct = round((not_found_count / total_input_companies) * 100, 2) if total_input_companies else 0

    summary_probs = df_summary["Probability"].dropna() if "Probability" in df_summary.columns else pd.Series(dtype=float)
    high_conf_count = (summary_probs >= 90).sum() if not summary_probs.empty else 0
    high_conf_pct = round((high_conf_count / len(summary_probs)) * 100, 2) if len(summary_probs) > 0 else 0

    multiple_summary_companies = 0
    if "Company" in df_summary.columns:
        multiple_summary_companies = int((df_summary["Company"].value_counts() > 1).sum())

    selected_mode = perf_info.get("selected_mode")
    selected_total_time = None
    if selected_mode == "sequential":
        selected_total_time = perf_info.get("sequential_total")
    elif selected_mode == "parallel":
        selected_total_time = perf_info.get("parallel_total")

    time_per_company = round(selected_total_time / total_input_companies, 4) if selected_total_time and total_input_companies else None

    # Bloco 1 - visão geral
    rows.append({"Section": "Overview", "Metric": "Selected Mode", "Value": selected_mode})
    rows.append({"Section": "Overview", "Metric": "Input Companies", "Value": total_input_companies})
    rows.append({"Section": "Overview", "Metric": "Summary Rows", "Value": len(df_summary)})
    rows.append({"Section": "Overview", "Metric": "Companies Found", "Value": found_count})
    rows.append({"Section": "Overview", "Metric": "Companies Found %", "Value": found_pct})
    rows.append({"Section": "Overview", "Metric": "Customers Not Found", "Value": not_found_count})
    rows.append({"Section": "Overview", "Metric": "Customers Not Found %", "Value": not_found_pct})
    rows.append({"Section": "Overview", "Metric": "Companies with Multiple Summary Results", "Value": multiple_summary_companies})
    rows.append({"Section": "Overview", "Metric": "Summary Matches with Probability >= 90", "Value": int(high_conf_count)})
    rows.append({"Section": "Overview", "Metric": "Summary Matches with Probability >= 90 %", "Value": high_conf_pct})

    if selected_total_time is not None:
        rows.append({"Section": "Overview", "Metric": "Selected Mode Total Seconds", "Value": round(selected_total_time, 2)})
    if time_per_company is not None:
        rows.append({"Section": "Overview", "Metric": "Seconds per Company", "Value": time_per_company})

    rows.append({"Section": "", "Metric": "", "Value": ""})

    # Bloco 2 - tempos
    if "sequential_total" in perf_info:
        rows.append({"Section": "Timing", "Metric": "Sequential Total Seconds", "Value": round(perf_info["sequential_total"], 2)})
    if "parallel_total" in perf_info:
        rows.append({"Section": "Timing", "Metric": "Parallel Total Seconds", "Value": round(perf_info["parallel_total"], 2)})

    if "sequential_timings" in perf_info:
        for group_name, timing in perf_info["sequential_timings"].items():
            rows.append({"Section": "Timing", "Metric": f"{group_name} Sequential Seconds", "Value": round(timing, 2)})

    if "parallel_timings" in perf_info:
        for group_name, timing in perf_info["parallel_timings"].items():
            rows.append({"Section": "Timing", "Metric": f"{group_name} Parallel Seconds", "Value": round(timing, 2)})

    rows.append({"Section": "", "Metric": "", "Value": ""})

    # Bloco 3 - matches por grupo
    total_group_matches = sum(len(matches) for matches in group_matches_dict.values())

    for group_name, matches in group_matches_dict.items():
        match_count = len(matches)
        match_pct = round((match_count / total_group_matches) * 100, 2) if total_group_matches else 0
        rows.append({"Section": "Group Distribution", "Metric": f"{group_name} Match Count", "Value": match_count})
        rows.append({"Section": "Group Distribution", "Metric": f"{group_name} Match %", "Value": match_pct})

    rows.append({"Section": "", "Metric": "", "Value": ""})

    # Bloco 4 - distribuição de confiança no summary
    if not summary_probs.empty:
        rows.append({"Section": "Confidence", "Metric": "Average Summary Probability", "Value": round(summary_probs.mean(), 2)})
        rows.append({"Section": "Confidence", "Metric": "Min Summary Probability", "Value": round(summary_probs.min(), 2)})
        rows.append({"Section": "Confidence", "Metric": "Max Summary Probability", "Value": round(summary_probs.max(), 2)})

        rows.append({"Section": "Confidence", "Metric": "Summary Probability >= 90", "Value": int((summary_probs >= 90).sum())})
        rows.append({"Section": "Confidence", "Metric": "Summary Probability 80-89.99", "Value": int(((summary_probs >= 80) & (summary_probs < 90)).sum())})
        rows.append({"Section": "Confidence", "Metric": "Summary Probability 50-79.99", "Value": int(((summary_probs >= 50) & (summary_probs < 80)).sum())})
        rows.append({"Section": "Confidence", "Metric": "Summary Probability < 50", "Value": int((summary_probs < 50).sum())})

    return pd.DataFrame(rows)