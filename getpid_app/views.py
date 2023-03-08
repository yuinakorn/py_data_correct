from django.shortcuts import render
from .controllers import ncd_controller, person_controller, labor_controller


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
    if 'hoscode' not in request.POST:
        return render(request, 'getpid_app/person.html', {})
    else:
        rows = person_controller.person(request.POST.get('hoscode', None), request.POST.get('cid', None))
        dicts = []

        hoscode = request.POST.get('hoscode', None)
        cid = request.POST.get('cid', None)

        for row in rows:
            dicts.append(row)
        my_list = dicts

        if len(my_list) == 0:
            color = 'red'
            show = False
        else:
            color = 'green'
            show = True

        context = {'my_list': my_list, 'color': color, 'show': show}
        context.update({'hoscode': str(hoscode), 'cid': str(cid)})
        print(context)
        return render(request, 'getpid_app/person.html', context)


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

        context = {'labor_dicts': dicts, 'show': show, 'colors': colors, 'cid': cid}

    return render(request, 'getpid_app/labor.html', context)
