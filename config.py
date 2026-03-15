from utils.matching import (
    output_map_group1,
    output_map_group2,
    output_map_group3,
    output_map_group4,
)

INPUT_FOLDER = r"C:\Users\112585631\Documents\Pessoal\MBA\Proj Final\Input Files"
RESULTS_FOLDER = r"C:\Users\112585631\Documents\Pessoal\MBA\Proj Final\Results"
CACHE_FOLDER = r"C:\Users\112585631\Documents\Pessoal\MBA\Proj Final\Cache Files"

MATCH_LIMIT = 20
HIGH_CONFIDENCE_THRESHOLD = 90
MID_CONFIDENCE_THRESHOLD = 50

RUN_BENCHMARK = False
DEFAULT_EXECUTION_MODE = "sequential"   # options: "sequential", "parallel"

GROUP_CONFIG = {
    "Group 1": {
        "acct_list_ids": [1861, 1862, 1864, 1863],
        "acct_list_names": [
            "Enterprise Client Expansion",
            "Enterprise Non-Client Expansion",
            "Strategic Non-Client Expansion",
            "Strategic Client Expansion",
        ],
        "output_map": output_map_group1,
        "uses_full_df": True,
        "extra_args_key": "gbl_buy_grp_count",
    },
    "Group 2": {
        "acct_list_ids": [1865, 1916],
        "acct_list_names": [
            "Horizon EMEA",
            "Horizon - non-EMEA",
        ],
        "output_map": output_map_group2,
        "uses_full_df": True,
        "extra_args_key": None,
    },
    "Group 3": {
        "acct_list_ids": [1860, 1878, 1895],
        "acct_list_names": [
            "Activate",
            "Growth",
            "BP WW CEID",
        ],
        "output_map": output_map_group3,
        "uses_full_df": False,
        "extra_args_key": "gbl_dom_count",
    },
    "Group 4": {
        "acct_list_ids": [1913],
        "acct_list_names": [
            "Activate Unassigned",
        ],
        "output_map": output_map_group4,
        "uses_full_df": False,
        "extra_args_key": "gbl_dom_count",
    },
}