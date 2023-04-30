from flask import Flask, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from Display import results
from flask_migrate import Migrate
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
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

                return render_template('front.html', resultWithImage=resultWithImage)
            else:
                return render_template('front.html', error='No vehicle information found for the uploaded image.')
    return render_template('front.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
