import pandas as pd

from config import MATCH_LIMIT, GROUP_CONFIG
from utils.normalize import normalize_name
from utils.summary import build_summary


def prepare_group_jobs(df_db, df_input):
    gbl_buy_grp_count = df_db.groupby("cov_type_id")["gbl_buy_grp"].nunique().to_dict()

    group34_ids = (
        GROUP_CONFIG["Group 3"]["acct_list_ids"] +
        GROUP_CONFIG["Group 4"]["acct_list_ids"]
    )

    df_db_group34 = df_db[df_db["acct_list_id"].isin(group34_ids)].copy()
    df_db_group34.reset_index(drop=True, inplace=True)
    df_db_group34["cust_legal_name_norm"] = df_db_group34["cust_legal_name"].apply(normalize_name)

    gbl_dom_count = df_db_group34.groupby("gbl_buy_grp")["dom_buy_grp"].nunique().to_dict()

    jobs = {}

    for group_name, cfg in GROUP_CONFIG.items():
        extra_args = None

        if cfg["extra_args_key"] == "gbl_buy_grp_count":
            extra_args = {"gbl_buy_grp_count": gbl_buy_grp_count}
        elif cfg["extra_args_key"] == "gbl_dom_count":
            extra_args = {"gbl_dom_count": gbl_dom_count}

        jobs[group_name] = {
            "df": df_db if cfg["uses_full_df"] else df_db_group34,
            "df_input": df_input,
            "acct_list_ids": cfg["acct_list_ids"],
            "acct_list_names": cfg["acct_list_names"],
            "output_map": cfg["output_map"],
            "limit": MATCH_LIMIT,
            "extra_args": extra_args,
        }

    return jobs


def append_unmatched_companies(matches, df_input):
    matched_companies = {
        m.get("Company")
        for m in matches
        if m.get("ACCT LEVEL") and m.get("ACCT LEVEL") != "Customer not found"
    }

    unmatched_rows = []
    for company in df_input["Company"].dropna().astype(str).str.strip().unique():
        if company not in matched_companies:
            unmatched_rows.append({
                "Company": company,
                "ACCT LEVEL": "Customer not found",
                "ACCT": None,
                "ACCT NAME": None,
                "Probability": None,
                "COV_TYPE_ID": None,
                "COV_NAME": None,
                "GBL_BUY_GRP": None,
                "GBL_BUY_GRP_NAME": None,
                "DOM_BUY_GRP": None,
                "DOM_BUY_GRP_NAME": None,
                "GBL_CLIENT_ID": None,
                "GBL_CLIENT_NAME": None,
                "acct_list_id": None,
                "acct_list_name": None,
                "MATCH_SOURCE": None,
                "Group": None,
                "CUST NAME": None,
                "Industry": None,
            })

    if unmatched_rows:
        df_unmatched = pd.DataFrame(unmatched_rows)
        df_unmatched = df_unmatched.loc[:, df_unmatched.notna().any()]

        df_matches = pd.DataFrame(matches)
        df_matches = df_matches.loc[:, df_matches.notna().any()]

        df_details = pd.concat([df_matches, df_unmatched], ignore_index=True)
    else:
        df_details = pd.DataFrame(matches)

    return df_details


def finalize_details(df_details, df_input):
    df_details.sort_values(by="Company", inplace=True)

    desired_subset = [
        "Company", "ACCT LEVEL", "ACCT", "ACCT NAME",
        "COV_TYPE_ID", "COV_NAME", "DOM_BUY_GRP", "DOM_BUY_GRP_NAME",
        "GBL_CLIENT_ID", "GBL_CLIENT_NAME", "acct_list_id", "acct_list_name",
        "Group", "CUST NAME"
    ]
    actual_subset = [col for col in desired_subset if col in df_details.columns]
    df_details.drop_duplicates(subset=actual_subset, inplace=True)

    df_summary = build_summary(df_details, df_input)

    desired_order = [
        "Company", "ACCT LEVEL", "ACCT", "ACCT NAME", "Probability",
        "acct_list_id", "acct_list_name", "MATCH_SOURCE", "CUST NAME",
        "COV_TYPE_ID", "COV_NAME", "GBL_BUY_GRP", "GBL_BUY_GRP_NAME",
        "DOM_BUY_GRP", "DOM_BUY_GRP_NAME", "GBL_CLIENT_ID",
        "GBL_CLIENT_NAME", "Industry", "Group"
    ]
    actual_order = [col for col in desired_order if col in df_details.columns]
    df_details = df_details[actual_order]

    actual_order_summary = [
        col for col in desired_order
        if col in df_summary.columns and col != "Group"
    ]
    df_summary = df_summary[actual_order_summary]

    return df_summary, df_details