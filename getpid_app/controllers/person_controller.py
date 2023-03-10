from .func_query import query
from dotenv import dotenv_values

config_env = dotenv_values(".env")


def person(cid):
    results = None
    if cid is not None:
        sql = "SELECT person.HOSPCODE,PID,TYPEAREA,concat('(',DISCHARGE,')',cdischarge.dischargedesc) AS dc_status,D_UPDATE " \
              "FROM person INNER JOIN cdischarge on cdischarge.dischargecode = person.DISCHARGE " \
              "WHERE CID = '" + cid + "' ORDER BY D_UPDATE DESC"
        results = query(sql)

    return results


def hoscode(hoscode):
    results = None
    if hoscode is not None:
        sql = "SELECT chospital.hoscode,chospital.hosname,chospital.hdc_regist,chospital.`status`, " \
                    "chostype.hostypename,campur.ampurname,ctambon.tambonname " \
                    "FROM chospital " \
                    "INNER JOIN chostype ON chospital.hostype = chostype.hostypecode " \
                    "INNER JOIN campur ON concat(chospital.provcode,chospital.distcode) = campur.ampurcodefull " \
                    "INNER JOIN ctambon ON concat(chospital.provcode,chospital.distcode,chospital.subdistcode) = ctambon.tamboncodefull " \
                    "WHERE hoscode = '" + hoscode + "'"
        results = query(sql)

    return results


def provider(cid):
    results = None
    if cid is not None:
        sql = "SELECT provider.*,cprovidertype.providertype FROM provider " \
                "INNER JOIN cprovidertype ON provider.PROVIDERTYPE = cprovidertype.id_providertype " \
                "WHERE cid = '" + cid + "' ORDER BY D_UPDATE DESC"
        results = query(sql)

    return results
