from django.shortcuts import render, redirect
from .controllers import ncd_controller, labor_controller, palliative_controller, person_controller
from django.contrib.auth import authenticate, login
import json
from django.db import connection

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect

# from .decorators import custom_login_required
from dotenv import dotenv_values

config = dotenv_values(".env")

def handler404(request, exception):
    return render(request, 'getpid_app/404.html')


# Index
def index(request):
    title = 'Data Correct'
    user_info = request.session.get('user_info', '0')
    return render(request, 'getpid_app/index.html', {'title': title, 'user_info': user_info})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:

            sql = """SELECT id, username, firstname, lastname, officename as hoscode  FROM sys_member 
            WHERE username = %s AND password = md5(%s) AND status = 'yes' LIMIT 1 """

            with connection.cursor() as cursor:
                cursor.execute(sql, (username, password))
                user = cursor.fetchone()
                if user:
                    # Creating session for the user
                    request.session['user_info'] = {
                        'username': user[1],
                        'firstname': user[2],
                        'lastname': user[3],
                        'hoscode': user[4]
                    }
                    return redirect('home')
                else:
                    user_info = '0'
                    return render(request, 'login.html', {'error': 'Invalid username or password', 'user_info': user_info})
    user_info = request.session.get('user_info', '0')

    return render(request, 'login.html', {'user_info': user_info})


def custom_login_required(function):
    def wrap(request, *args, **kwargs):
        if 'username' in request.session:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login')  # Redirect to the index page if not logged in
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


@custom_login_required
def my_protected_view(request):
    # Your protected view logic here
    return render(request, 'protected.html')


def logout_view(request):
    # Clear all session data
    request.session.flush()
    return redirect('login')


def home(request):
    # print session data
    # print(request.session.get('username'))
    session_user = request.session.get('user_info')
    username = session_user['username']
    hoscode = session_user['hoscode']
    fullname = session_user['firstname'] + ' ' + session_user['lastname']
    user_info = request.session.get('user_info') if request.session.get('user_info') else None
    return render(request, 'getpid_app/home.html', {'username': username, 'fullname': fullname, 'hoscode': hoscode, 'user_info': user_info})


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


def person(request):
    global color
    if 'cid' not in request.POST:
        return render(request, 'getpid_app/person.html', {})
    else:
        rows = person_controller.person(request.POST.get('cid', None))
        dicts = []
        cid = request.POST.get('cid', None)

        for row in rows:
            processed_row = {
                'HOSPCODE': row[0],
                'PID': row[1],
                'TYPEAREA': row[2],
                'DC_STATUS': row[3],
                'D_UPDATE': str(row[4]) if row[4] is not None else None
            }
            dicts.append(processed_row)

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
            processed_row = {
                'hoscode': row[0],
                'hosname': row[1].replace('โรงพยาบาลส่งเสริมสุขภาพตำบล', 'รพ.สต.'),
                'hdc_regist': 'เปิดใช้งาน' if row[2] == 1 else 'ปิดใช้งาน',
                'status': 'เปิดใช้งาน' if row[3] == 1 else 'ปิดใช้งาน',
                'hostypename': row[4],
                'ampurname': row[5],
                'tambonname': row[6]
            }
            dicts.append(processed_row)

        if len(dicts) == 0:
            color = 'red'
            show = False
        else:
            color = 'green'
            show = True

        context = {'my_list': dicts, 'color': color, 'show': show, 'hoscode': str(request.POST.get('hoscode', None))}
        return render(request, 'getpid_app/hoscode.html', context)


def provider(request):
    if 'cid' not in request.POST:
        return render(request, 'getpid_app/provider.html', {})
    else:
        rows = person_controller.provider(request.POST.get('cid', None))
        dicts = []
        cid = request.POST.get('cid', None)

        for row in rows:
            row['D_UPDATE'] = str(row['D_UPDATE']) if row['D_UPDATE'] is not None else None
            row['STARTDATE'] = str(row['STARTDATE']) if row['STARTDATE'] is not None else None
            dicts.append(row)

        if len(dicts) == 0:
            color = 'red'
            show = False
        else:
            color = 'green'
            show = True

        context = {'my_list': dicts, 'color': color, 'show': show, 'cid': str(cid)}
        return render(request, 'getpid_app/provider.html', context)
