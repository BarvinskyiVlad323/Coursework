from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.patients import bp
from app.patients.forms import PatientForm, MedicalHistoryForm
from app.models import Patient, MedicalHistory

@bp.route('/patients')
@login_required
def patient_list():
    page = request.args.get('page', 1, type=int)
    patients = Patient.query.order_by(Patient.last_name).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('patients/list.html', title='Patients', patients=patients)

@bp.route('/patient/new', methods=['GET', 'POST'])
@login_required
def new_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            contact_number=form.contact_number.data,
            email=form.email.data,
            address=form.address.data
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient record created successfully.', 'success')
        return redirect(url_for('patients.patient_list'))
    return render_template('patients/edit.html', title='New Patient', form=form)

@bp.route('/patient/<int:id>')
@login_required
def patient_detail(id):
    patient = Patient.query.get_or_404(id)
    return render_template('patients/detail.html', title='Patient Details', patient=patient)

@bp.route('/patient/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    form = PatientForm(obj=patient)
    if form.validate_on_submit():
        patient.first_name = form.first_name.data
        patient.last_name = form.last_name.data
        patient.date_of_birth = form.date_of_birth.data
        patient.gender = form.gender.data
        patient.contact_number = form.contact_number.data
        patient.email = form.email.data
        patient.address = form.address.data
        db.session.commit()
        flash('Patient record has been updated.', 'success')
        return redirect(url_for('patients.patient_detail', id=patient.id))
    return render_template('patients/edit.html', title='Edit Patient', form=form)

@bp.route('/patient/<int:id>/history/new', methods=['GET', 'POST'])
@login_required
def new_medical_history(id):
    patient = Patient.query.get_or_404(id)
    form = MedicalHistoryForm()
    if form.validate_on_submit():
        history = MedicalHistory(
            patient_id=patient.id,
            diagnosis=form.diagnosis.data,
            treatment=form.treatment.data,
            prescription=form.prescription.data,
            notes=form.notes.data,
            next_appointment=form.next_appointment.data,
            created_by=current_user.id
        )
        db.session.add(history)
        db.session.commit()
        flash('Medical history record added successfully.', 'success')
        return redirect(url_for('patients.patient_detail', id=patient.id))
    return render_template('patients/medical_history.html', title='New Medical Record',
                         form=form, patient=patient)

@bp.route('/patient/<int:id>/delete', methods=['POST'])
@login_required
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Пацієнта успішно видалено.', 'success')
    return redirect(url_for('patients.patient_list')) 