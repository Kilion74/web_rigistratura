from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# Данные о пациентах и врачах
patients = []
doctors = [
    {"name": "Иванов И.И.", "specialization": "Терапевт", "schedule": []},
    {"name": "Петрова А.С.", "specialization": "Кардиолог", "schedule": []},
    {"name": "Сидоров Д.В.", "specialization": "Хирург", "schedule": []},
    {"name": "Парамонова И.В.", "specialization": "Стоматолог", "schedule": []},
    {"name": "Петрик Т.П.", "specialization": "ЛОР", "schedule": []},
    {"name": "Аванесова Л.Х.", "specialization": "Педиатр", "schedule": []},
    {"name": "Михельсон В.А.", "specialization": "Невролог", "schedule": []},
    {"name": "Храмова С.М.", "specialization": "Психиатр", "schedule": []},
]


# Функция регистрации пациента
@app.route('/register', methods=['GET', 'POST'])
def register_patient():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        doctor_name = request.form['doctor_name']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']

        # Проверяем доступность врача в указанное время
        doctor = next((d for d in doctors if d['name'] == doctor_name), None)
        if doctor and (appointment_date, appointment_time) not in doctor['schedule']:
            patient = {'first_name': first_name, 'last_name': last_name, 'doctor_name': doctor_name,
                       'appointment_date': appointment_date, 'appointment_time': appointment_time}
            patients.append(patient)
            doctor['schedule'].append((appointment_date, appointment_time))
            return redirect(url_for('index'))
        else:
            return render_template('register.html', doctors=doctors, error='Врач недоступен в указанное время')

    return render_template('register.html', doctors=doctors)


# Функция удаления пациента
@app.route('/delete/<int:index>', methods=['GET'])
def delete_patient(index):
    if index < len(patients):
        patient = patients[index]
        doctor = next((d for d in doctors if d['name'] == patient['doctor_name']), None)
        doctor['schedule'].remove((patient['appointment_date'], patient['appointment_time']))
        patients.pop(index)
    return redirect(url_for('index'))


# Функция просмотра свободных врачей
@app.route('/')
def index():
    return render_template('index.html', patients=patients, doctors=doctors)


if __name__ == '__main__':
    app.run(debug=True)
