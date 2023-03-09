from django.shortcuts import render
from .controllers import ncd_controller, person_controller, labor_controller, palliative_controller
import json


def handler404(request, exception):
    return render(request, 'getpid_app/404.html')


# Index
def index(request):
    title = 'Data Correct'
    return render(request, 'getpid_app/index.html', {'title': title})


# NCD
def ncd(request):
    global color
    if 'cid' not in request.POST:
        show = False
        return render(request, 'getpid_app/ncd.html', {'show': show})
    else:
        rows = ncd_controller.ncd(request.POST.get('cid', None))
        # show = True
        cid = request.POST.get('cid', None)
        print(cid)  # to check error cid

        # chronic
        dicts = []
        for row in rows['results1']:
            row['date_diag'] = str(row['date_diag']) if row['date_diag'] is not None else None
            dicts.append(row)
        chronic = dicts

        # diagnosis_opd ความดัน ผู้ป่วยนอก
        dicts = []
        for row in rows['results2']:
            row['date_serv'] = str(row['date_serv']) if row['date_serv'] is not None else None
            dicts.append(row)
        diagnosis_opd_i10 = dicts

        # diagnosis_opd ความดัน ผู้ป่วยใน
        dicts = []
        for row in rows['results3']:
            row['datetime_admit'] = str(row['datetime_admit']) if row['datetime_admit'] is not None else None
            dicts.append(row)
        diagnosis_ipd_i10 = dicts

        # diagnosis_opd เบาหวาน ผู้ป่วยนอก
        dicts = []
        for row in rows['results4']:
            row['date_serv'] = str(row['date_serv']) if row['date_serv'] is not None else None
            dicts.append(row)
        diagnosis_opd_e10 = dicts

        # diagnosis_opd เบาหวาน ผู้ป่วยใน
        dicts = []
        for row in rows['results5']:
            row['datetime_admit'] = str(row['datetime_admit']) if row['datetime_admit'] is not None else None
            dicts.append(row)
        diagnosis_ipd_e10 = dicts

        if len(chronic) == 0 and len(diagnosis_opd_i10) == 0 and len(diagnosis_ipd_i10) == 0 and len(
                diagnosis_opd_e10) == 0 and len(diagnosis_ipd_e10) == 0:
            show = False
            color = 'red'
        else:
            show = True
            color = 'green'

        context = {
            'show': show,
            'color': color,
            'cid': cid,
            'chronic': chronic,
            'diagnosis_opd_i10': diagnosis_opd_i10,
            'diagnosis_ipd_i10': diagnosis_ipd_i10,
            'diagnosis_opd_e10': diagnosis_opd_e10,
            'diagnosis_ipd_e10': diagnosis_ipd_e10,
        }

        return render(request, 'getpid_app/ncd.html', context)


def person(request):
    global color
    if 'cid' not in request.POST:
        return render(request, 'getpid_app/person.html', {})
    else:
        rows = person_controller.person(request.POST.get('cid', None))
        dicts = []
        cid = request.POST.get('cid', None)

        for row in rows:
            row['D_UPDATE'] = str(row['D_UPDATE']) if row['D_UPDATE'] is not None else None
            dicts.append(row)

        if len(dicts) == 0:
            color = 'red'
            show = False
        else:
            color = 'green'
            show = True

        context = {'my_list': dicts, 'color': color, 'show': show, 'cid': str(cid)}
        return render(request, 'getpid_app/person.html', context)


def hoscode(request):
    if 'hoscode' not in request.POST:
        return render(request, 'getpid_app/hoscode.html', {})
    else:
        rows = person_controller.hoscode(request.POST.get('hoscode', None))
        dicts = []

        for row in rows:
            row['status'] = 'เปิดใช้งาน' if row['status'] == 1 else 'ปิดใช้งาน'
            row['hdc_regist'] = 'เปิดใช้งาน' if row['hdc_regist'] == 1 else 'ปิดใช้งาน'
            row['hosname'] = row['hosname'].replace('โรงพยาบาลส่งเสริมสุขภาพตำบล', 'รพ.สต.')
            dicts.append(row)

        if len(dicts) == 0:
            color = 'red'
            show = False
        else:
            color = 'green'
            show = True

        context = {'my_list': dicts, 'color': color, 'show': show, 'hoscode': str(request.POST.get('hoscode', None))}
        return render(request, 'getpid_app/hoscode.html', context)


def labor(request):
    if 'cid' not in request.POST:
        show = False
        return render(request, 'getpid_app/labor.html', {'show': show})
    else:
        rows = labor_controller.labor(request.POST.get('cid', None))
        cid = request.POST.get('cid', None)
        dicts = []
        for row in rows:
            row['BDATE'] = row['BDATE'].strftime('%Y-%m-%d') if row['BDATE'] is not None else None
            row['LMP'] = row['LMP'].strftime('%Y-%m-%d') if row['LMP'] is not None else None
            row['EDC'] = row['EDC'].strftime('%Y-%m-%d') if row['EDC'] is not None else None
            row['LBORN'] = int(row['LBORN']) if row['LBORN'] is not None else None
            dicts.append(row)

        if len(dicts) == 0:
            show = False
            colors = 'red'
        else:
            show = True
            colors = 'green'

        # print(dicts)
        context = {'labor_dicts': dicts, 'show': show, 'colors': colors, 'cid': cid}

    return render(request, 'getpid_app/labor.html', context)


def palliative(request):
    g_list = ''
    pharma_list = ''
    careplan_list = ''
    if 'cid' not in request.POST:
        show = False
        return render(request, 'getpid_app/palliative.html', {'show': show})
    else:
        rows = palliative_controller.palliative(request.POST.get('cid', None))
        if len(rows) > 0:
            cid = request.POST.get('cid', None)
            g_list = [rows[0].get('g_code', None)]
            pharma_list = [rows[0].get('pharma_code', None)]
            careplan_list = [rows[0].get('careplan_code', None)]

            g_list = json.loads(str(g_list).replace('[\'', '[').replace('\']', ']'))
            pharma_list = json.loads(str(pharma_list).replace('[\'', '[').replace('\']', ']'))
            careplan_list = json.loads(str(careplan_list).replace('[\'', '[').replace('\']', ']'))

            show = True
            colors = 'green'
        else:
            cid = request.POST.get('cid', None)
            show = False
            colors = 'red'

        context = {
            'cid': cid,
            'show': show,
            'colors': colors,
            'gcode_dicts': g_list,
            'pharma_list': pharma_list,
            'careplan_list': careplan_list,
        }

    return render(request, 'getpid_app/palliative.html', context)
