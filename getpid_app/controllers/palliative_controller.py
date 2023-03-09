from .func_query import query


def palliative(cid):
    results = None
    if cid is not None:
        sql = "SELECT * FROM tmp_pallitive WHERE cid = '" + cid + "'"

        results = query(sql)
    # print(results)
    return results
