import os
os.add_dll_directory(r"C:\Program Files\IBM\SQLLIB\BIN")
import datetime
import pandas as pd
import ibm_db

from utils.cmdw_config import get_db_credentials
from config import CACHE_FOLDER

current_year = datetime.datetime.now().year


def fetch_data(country_code):
    os.makedirs(CACHE_FOLDER, exist_ok=True)
    cache_file = os.path.join(CACHE_FOLDER, f"db_cache_{country_code}.csv")

    if os.path.exists(cache_file):
        print(f"Loading SQL results from cache for country {country_code}...")
        df_db = pd.read_csv(cache_file, low_memory=False)
        df_db.columns = df_db.columns.str.lower()
        if "cust_legal_name" in df_db.columns:
            df_db["cust_legal_name"] = df_db["cust_legal_name"].astype(str).str.strip()
        return df_db

    print("Cache not found. Connecting to the database and executing the SQL query for provided country")
    db_params = get_db_credentials()
    dsn = ";".join([f"{key}={value}" for key, value in db_params.items()])
    conn = ibm_db.connect(dsn, "", "")

    if not conn:
        raise Exception("Unable to connect to database")

    sql_query = f"""
    SELECT DISTINCT 
        CCA.CTRYNUM, 
        CCA.COV_REGION_CD, 
        CCA.COV_TYPE, 
        CCA.COV_TYPE || CCA.COV_ID as cov_type_id, 
        CCA.COV_NAME,
        CCA.GBL_BUY_GRP, 
        GBG.GBL_BUY_GRP_NAME, 
        BG.DOM_BUY_GRP_NAME, 
        CCA.DOM_BUY_GRP, 
        CCA.GBL_CLIENT_ID, 
        gc.gbl_client_name,
        CCA.CUST_LEGAL_NAME,
        al.acct_list_id,
        al.acct_list_name,
        cca.quota_acct_cd, 
        qa.quota_acct_name, 
        ind.industry_name
    FROM ww.fmst_o_cust_all_2601_p2 cca
    LEFT JOIN ww.FMST_R_QA_GBL_BUY_GRP_2601_P2 gbg 
        ON gbg.GBL_BUY_GRP_CODE = CCA.GBL_BUY_GRP AND gbg.APPR_STATUS = 'Approved'
    LEFT JOIN ww.FMST_R_QA_DOM_BUY_GRP_2601_P2 bg 
        ON bg.DOM_BUY_GRP_CODE = CCA.DOM_BUY_GRP AND bg.APPR_STATUS = 'Approved'
    LEFT JOIN ww.FMST_R_QA_GBL_CLIENT_2601_P2 gc 
        ON gc.GBL_CLIENT_CODE = cca.GBL_CLIENT_ID AND gc.APPR_STATUS = 'Approved'
    LEFT JOIN ww.FMST_R_QT_QUOTA_ACCT_2601_P1 qa 
        ON cca.quota_acct_cd = qa.quota_acct_cd AND cca.ctrynum = qa.fin_ctrynum
    LEFT JOIN ww.FMST_R_QT_ACCT_TYPE_LIST atl 
        ON CCA.ACCT_TYPE_ID = atl.ACCT_TYPE_ID 
    LEFT JOIN ww.FMST_R_QT_ACCT_LIST al 
        ON atl.ACCT_LIST_ID = al.ACCT_LIST_ID 
    LEFT JOIN ww.FMST_R_QT_ACCT_LIST_GRP alg 
        ON al.ACCT_LIST_GRP_ID = alg.ACCT_LIST_GRP_ID
    LEFT JOIN WW.FMST_R_ITT_INDUSTRY IND
        ON CCA.WW_IND = IND.INDUSTRY_CODE
        AND IND.APPR_STATUS = 'Approved'
        AND IND.EFFC_DATE >= '{current_year}-01-01'
    WHERE 1=1
      AND cca.active_indc = 'Y'
      AND cca.cov_type IN ('A', 'I', 'T')
      AND alg.acct_list_grp_id = 537
      AND CCA.CI_CUST_NBR IS NOT NULL
      AND al.acct_list_ID IN (1864, 1878, 1865, 1913, 1895, 1860, 1861, 1862, 1863, 1916)
      AND cca.ctrynum IN ({country_code})
    """

    stmt = ibm_db.exec_immediate(conn, sql_query)
    db_rows = []

    row = ibm_db.fetch_assoc(stmt)
    while row:
        db_rows.append(row)
        row = ibm_db.fetch_assoc(stmt)

    df_db = pd.DataFrame(db_rows)
    df_db.columns = df_db.columns.str.lower()

    if "cust_legal_name" in df_db.columns:
        df_db["cust_legal_name"] = df_db["cust_legal_name"].astype(str).str.strip()

    df_db.to_csv(cache_file, index=False)
    ibm_db.close(conn)
    return df_db