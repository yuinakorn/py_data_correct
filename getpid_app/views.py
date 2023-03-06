from django.shortcuts import render
from .forms import SearchForm
from .controllers import ncd_controller, person_controller


# NCD
def search_ncd(request):
    global color
    if 'cid' not in request.POST:
        show = False
        return render(request, 'getpid_app/ncd.html', {'show': show})
    else:
        rows = ncd_controller.ncd(request.POST.get('cid', None))
        # show = True
        cid = request.POST.get('cid', None)

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

        if len(chronic) == 0 and len(diagnosis_opd_i10) == 0 and len(diagnosis_ipd_i10) == 0 and len(diagnosis_opd_e10) == 0 and len(diagnosis_ipd_e10) == 0:
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


def search_person(request):
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
        print(my_list)
        context = {'my_list': my_list}
        context.update({'hoscode': str(hoscode), 'cid': str(cid)})

        return render(request, 'getpid_app/person.html', context)


def index(request):
    return render(request, 'getpid_app/index.html', {})
