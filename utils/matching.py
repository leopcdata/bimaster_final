from rapidfuzz import fuzz, process
import collections

from utils.normalize import normalize_name


def build_base_output(row, score, company):
    return {
        "Company": company,
        "Probability": score,
        "acct_list_id": row.get("acct_list_id"),
        "acct_list_name": row.get("acct_list_name"),
        "CUST NAME": row.get("cust_legal_name"),
        "Industry": row.get("industry_name"),
        "COV_TYPE_ID": row.get("cov_type_id"),
        "COV_NAME": row.get("cov_name"),
        "GBL_BUY_GRP": row.get("gbl_buy_grp"),
        "GBL_BUY_GRP_NAME": row.get("gbl_buy_grp_name"),
    }


def output_map_group1(row, score, company, gbl_buy_grp_count=None):
    base = build_base_output(row, score, company)
    base.update({
        "ACCT LEVEL": "COV_TYPE_ID",
        "ACCT": row.get("cov_type_id"),
        "ACCT NAME": row.get("cov_name"),
        "Group": "Group 1",
        "MATCH_SOURCE": row.get("acct_list_name"),
    })

    if gbl_buy_grp_count is not None:
        count = gbl_buy_grp_count.get(row.get("cov_type_id"), 0)
        if count == 1:
            base["GBL_BUY_GRP"] = "Unique GBG under the Coverage"
            base["GBL_BUY_GRP_NAME"] = ""

    return base


def output_map_group2(row, score, company):
    base = build_base_output(row, score, company)
    base.update({
        "ACCT LEVEL": "COV_TYPE_ID",
        "ACCT": row.get("cov_type_id"),
        "ACCT NAME": row.get("cov_name"),
        "Group": "Group 2",
        "MATCH_SOURCE": row.get("acct_list_name"),
    })
    return base


def output_map_group3(row, score, company, gbl_dom_count):
    base = build_base_output(row, score, company)

    if gbl_dom_count.get(row.get("gbl_buy_grp"), 0) == 1:
        dom_buy_grp = "Unique DOM_BUY_GRP under the GBG"
        dom_buy_grp_name = ""
    else:
        dom_buy_grp = row.get("dom_buy_grp")
        dom_buy_grp_name = row.get("dom_buy_grp_name")

    acct_val = str(row.get("gbl_buy_grp", "")).strip()
    if (len(acct_val) in [3, 4]) and acct_val.upper().startswith("ST"):
        base.update({
            "ACCT LEVEL": "DOM_BUY_GRP",
            "ACCT": acct_val,
            "ACCT NAME": f"{str(row.get('industry_name', '')).strip()} {acct_val} {str(row.get('cov_name', '')).strip()}".strip(),
        })
    else:
        base.update({
            "ACCT LEVEL": "GBL_BUY_GRP",
            "ACCT": row.get("gbl_buy_grp"),
            "ACCT NAME": row.get("gbl_buy_grp_name"),
        })

    base.update({
        "DOM_BUY_GRP": dom_buy_grp,
        "DOM_BUY_GRP_NAME": dom_buy_grp_name,
        "GBL_CLIENT_ID": row.get("gbl_client_id"),
        "GBL_CLIENT_NAME": row.get("gbl_client_name"),
        "Group": "Group 3",
        "MATCH_SOURCE": row.get("acct_list_name"),
    })
    return base


def output_map_group4(row, score, company, gbl_dom_count):
    # Mantém a mesma lógica do Group 3, mas marca como Group 4
    base = build_base_output(row, score, company)

    if gbl_dom_count.get(row.get("gbl_buy_grp"), 0) == 1:
        dom_buy_grp = "Unique DOM_BUY_GRP under the GBG"
        dom_buy_grp_name = ""
    else:
        dom_buy_grp = row.get("dom_buy_grp")
        dom_buy_grp_name = row.get("dom_buy_grp_name")

    acct_val = str(row.get("gbl_buy_grp", "")).strip()
    if (len(acct_val) in [3, 4]) and acct_val.upper().startswith("ST"):
        base.update({
            "ACCT LEVEL": "DOM_BUY_GRP",
            "ACCT": acct_val,
            "ACCT NAME": f"{str(row.get('industry_name', '')).strip()} {acct_val} {str(row.get('cov_name', '')).strip()}".strip(),
        })
    else:
        base.update({
            "ACCT LEVEL": "GBL_BUY_GRP",
            "ACCT": row.get("gbl_buy_grp"),
            "ACCT NAME": row.get("gbl_buy_grp_name"),
        })

    base.update({
        "DOM_BUY_GRP": dom_buy_grp,
        "DOM_BUY_GRP_NAME": dom_buy_grp_name,
        "GBL_CLIENT_ID": row.get("gbl_client_id"),
        "GBL_CLIENT_NAME": row.get("gbl_client_name"),
        "Group": "Group 4",
        "MATCH_SOURCE": row.get("acct_list_name"),
    })
    return base


def _build_candidate_index(series):
    candidate_to_indices = collections.defaultdict(list)
    for idx, name in series.fillna("").astype(str).str.strip().str.lower().items():
        if name:
            candidate_to_indices[name].append(idx)
    return candidate_to_indices


def _get_blocked_candidates(candidate_dict, first_token):
    if not first_token:
        return list(candidate_dict.keys())
    blocked = [cand for cand in candidate_dict.keys() if first_token in cand]
    return blocked if blocked else list(candidate_dict.keys())


def _append_results(group_matches, results, candidate_dict, df_filtered, output_map, company, extra_args, min_score, seen_keys):
    for candidate, score, _ in results:
        if score < min_score:
            continue

        for idx in candidate_dict[candidate]:
            row = df_filtered.iloc[idx]
            output_row = (
                output_map(row, score, company)
                if not extra_args
                else output_map(row, score, company, **extra_args)
            )

            dedupe_key = (
                output_row.get("Company"),
                output_row.get("Group"),
                output_row.get("ACCT LEVEL"),
                output_row.get("ACCT"),
                output_row.get("acct_list_id"),
                round(float(output_row.get("Probability", 0)), 4),
            )

            if dedupe_key not in seen_keys:
                seen_keys.add(dedupe_key)
                group_matches.append(output_row)


def process_group(df, df_input, acct_list_ids, acct_list_names, output_map, limit=20, extra_args=None):
    if "acct_list_id" in df.columns:
        df_filtered = df[df["acct_list_id"].isin(acct_list_ids)].copy()
    else:
        df_filtered = df[df["acct_list_name"].isin(acct_list_names)].copy()

    if df_filtered.empty:
        return []

    df_filtered.reset_index(drop=True, inplace=True)

    df_filtered["cust_legal_name_raw"] = df_filtered["cust_legal_name"].fillna("").astype(str).str.strip()
    df_filtered["cust_legal_name_norm"] = df_filtered["cust_legal_name_raw"].apply(normalize_name)

    raw_candidate_to_indices = _build_candidate_index(df_filtered["cust_legal_name_raw"])
    norm_candidate_to_indices = _build_candidate_index(df_filtered["cust_legal_name_norm"])

    group_matches = []
    seen_keys = set()

    for company in df_input["Company"].dropna().astype(str).str.strip().unique():
        comp_lower = company.lower().strip()
        if not comp_lower:
            continue

        first_token_raw = comp_lower.split()[0] if comp_lower else ""
        blocked_raw = _get_blocked_candidates(raw_candidate_to_indices, first_token_raw)
        raw_results = process.extract(comp_lower, blocked_raw, scorer=fuzz.ratio, limit=limit)

        _append_results(
            group_matches=group_matches,
            results=raw_results,
            candidate_dict=raw_candidate_to_indices,
            df_filtered=df_filtered,
            output_map=output_map,
            company=company,
            extra_args=extra_args,
            min_score=80,
            seen_keys=seen_keys,
        )

        normalized_company = normalize_name(company)
        first_token_norm = normalized_company.split()[0] if normalized_company else ""
        blocked_norm = _get_blocked_candidates(norm_candidate_to_indices, first_token_norm)
        norm_results = process.extract(normalized_company, blocked_norm, scorer=fuzz.ratio, limit=limit)

        high_norm = [(cand, sc, ix) for cand, sc, ix in norm_results if 80 <= sc <= 100]
        _append_results(
            group_matches=group_matches,
            results=high_norm,
            candidate_dict=norm_candidate_to_indices,
            df_filtered=df_filtered,
            output_map=output_map,
            company=company,
            extra_args=extra_args,
            min_score=80,
            seen_keys=seen_keys,
        )

        if not high_norm:
            low_norm = [(cand, sc, ix) for cand, sc, ix in norm_results if 60 <= sc < 80]
            _append_results(
                group_matches=group_matches,
                results=low_norm,
                candidate_dict=norm_candidate_to_indices,
                df_filtered=df_filtered,
                output_map=output_map,
                company=company,
                extra_args=extra_args,
                min_score=60,
                seen_keys=seen_keys,
            )

    return group_matches