from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import sqlalchemy
from werkzeug.utils import secure_filename
from Display import results
from flask_migrate import Migrate
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# MODEL
class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String, unique=True)
    plate_number = db.Column(db.String, unique=True)
    make = db.Column(db.String)
    model = db.Column(db.String)
    year = db.Column(db.Integer)
    color = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    owner = db.relationship("Owner", back_populates="vehicles")

class LicensePlate(db.Model):
    __tablename__ = 'license_plates'
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String, unique=True)
    plate_id = db.Column(db.String)
    plate_image = db.Column(db.String)

class Owner(db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    contact_number = db.Column(db.String)
    address = db.Column(db.String)
    vehicles = db.relationship("Vehicle", order_by=Vehicle.id, back_populates="owner")

# CONTROLLER
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file:
            # Save the file to the upload folder
            filename = secure_filename(file.filename)
            file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_url)
            plate_number = str(results(file_url))

            # Query the database for the vehicle information
            vehicle = Vehicle.query.filter_by(plate_number=plate_number).first()
            if vehicle is not None:
                # Get the owner information for the vehicle
                owner = vehicle.owner
                
                if owner is None:
                    print("No owner found for plate number:", plate_number)
                else:
                    print("Owner found:", owner.first_name, owner.last_name)
                resultWithImage = {
                    'result': plate_number,
                    'img_url': file_url,
                    'img_name': filename,
                    'make': owner.vehicles[0].make,
                    'model': owner.vehicles[0].model,
                    'year': owner.vehicles[0].year,
                    'color': owner.vehicles[0].color,
                    'owner_first_name': owner.first_name,
                    'owner_last_name': owner.last_name,
                    'owner_contact_number': owner.contact_number,
                    'owner_address': owner.address,
                }
                print(resultWithImage)
                # VIEW
                return render_template('front.html', resultWithImage=resultWithImage)
            else:
                print("error happened")
                errorMsg = {
                    "img_url" : file_url,
                    'img_name': filename,
                    "error_message": "No vehicle information found for the uploaded image."
                }
                return render_template('front.html', errorMsg=errorMsg)
    return render_template('front.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/admin_upload', methods=['GET', 'POST'])
def admin_upload():
    if request.method == 'POST':
        # Get the data from the form
        registration_number = request.form.get('registration_number')
        plate_number = request.form.get('plate_number')
        plate_id = request.form.get('plate_id')
        make = request.form.get('make')
        model = request.form.get('model')
        year = request.form.get('year')
        color = request.form.get('color')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        contact_number = request.form.get('contact_number')
        address = request.form.get('address')

        # Create new Owner and Vehicle objects
        owner = Owner(first_name=first_name, last_name=last_name, contact_number=contact_number, address=address)
        vehicle = Vehicle(registration_number=registration_number, plate_number=plate_number, make=make, model=model, year=year, color=color, owner=owner)
        license_plate = LicensePlate(plate_number=plate_number, plate_id=plate_id, plate_image="none")

        try:
            db.session.add(owner)
            db.session.add(vehicle)
            db.session.add(license_plate)
            db.session.commit()
            message = 'Data uploaded successfully!'
            status = 'success'
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            message = 'Database error: Duplicate entry.'
            status = 'error'

        return render_template('admin_upload.html', message=message, status=status, data=request.form)

    # If not a POST request, render the upload form
    return render_template('admin_upload.html')

@app.route('/view_all', methods=['GET'])
def view_all():
    vehicles = Vehicle.query.all()
    return render_template('view_all.html', vehicles=vehicles)

@app.route('/admin_edit/<vehicle_id>', methods=['GET', 'POST'])
def admin_edit(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if request.method == 'POST':
        # Get the data from the form
        registration_number = request.form.get('registration_number')
        plate_number = request.form.get('plate_number')
        make = request.form.get('make')
        model = request.form.get('model')
        year = request.form.get('year')
        color = request.form.get('color')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        contact_number = request.form.get('contact_number')
        address = request.form.get('address')

        # Update the Owner, Vehicle and LicensePlate objects
        vehicle.owner.first_name = first_name
        vehicle.owner.last_name = last_name
        vehicle.owner.contact_number = contact_number
        vehicle.owner.address = address

        vehicle.registration_number = registration_number
        vehicle.plate_number = plate_number
        vehicle.make = make
        vehicle.model = model
        vehicle.year = year
        vehicle.color = color

        license_plate = LicensePlate.query.filter_by(plate_number=plate_number).first()
        if license_plate:
            license_plate.plate_id = request.form.get('plate_id')  # assuming 'plate_id' comes from the form
        else:
            license_plate = LicensePlate(plate_number=plate_number, plate_id=request.form.get('plate_id'), plate_image="none")
            db.session.add(license_plate)
        
        try:
            db.session.commit()
            msg = "Successfully updated"
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            msg = "Error occured while updating to db"
        return redirect(url_for('view_all', msg=msg))
    else:
        # render the admin_edit.html template with the vehicle data
        return render_template('admin_edit.html', vehicle=vehicle)

@app.route('/admin_delete/<int:vehicle_id>', methods=['GET'])
def admin_delete(vehicle_id):
    # fetch the vehicle by id
    vehicle = Vehicle.query.get(vehicle_id)

    # if no vehicle is found with the provided id, return a 404 error
    if vehicle is None:
        return redirect(url_for('view_all'))

    # delete the vehicle
    db.session.delete(vehicle)
    db.session.commit()

    # redirect the user to the view_all page
    return redirect(url_for('view_all'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
