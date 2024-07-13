import mysql.connector
from mysql.connector import Error

class Patient:
    def __init__(self, patient_id, name, age, gender, disease, doctor_id=None):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.disease = disease
        self.doctor_id = doctor_id

    def __str__(self):
        return f"Patient[ID: {self.patient_id}, Name: {self.name}, Age: {self.age}, Gender: {self.gender}, Disease: {self.disease}, Doctor ID: {self.doctor_id}]"


class Doctor:
    def __init__(self, doctor_id, name, specialization):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization

    def __str__(self):
        return f"Doctor[ID: {self.doctor_id}, Name: {self.name}, Specialization: {self.specialization}]"


class HospitalManagementSystem:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='HospitalDB',
                user='root',  # Change to your MySQL username
                password='root'  # Change to your MySQL password
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    def add_patient(self, patient):
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO Patients (patient_id, name, age, gender, disease, doctor_id) VALUES (%s, %s, %s, %s, %s, %s)",
                        (patient.patient_id, patient.name, patient.age, patient.gender, patient.disease, patient.doctor_id))
            self.connection.commit()
            print("Patient added successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def update_patient(self, patient_id, **kwargs):
        cursor = self.connection.cursor()
        try:
            updates = ', '.join([f"{key} = %s" for key in kwargs])
            values = tuple(kwargs.values()) + (patient_id,)
            cursor.execute(f"UPDATE Patients SET {updates} WHERE patient_id = %s", values)
            self.connection.commit()
            print("Patient updated successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def delete_patient(self, patient_id):
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM Patients WHERE patient_id = %s", (patient_id,))
            self.connection.commit()
            print("Patient deleted successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def add_doctor(self, doctor):
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO Doctors (doctor_id, name, specialization) VALUES (%s, %s, %s)",
                        (doctor.doctor_id, doctor.name, doctor.specialization))
            self.connection.commit()
            print("Doctor added successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def update_doctor(self, doctor_id, **kwargs):
        cursor = self.connection.cursor()
        try:
            updates = ', '.join([f"{key} = %s" for key in kwargs])
            values = tuple(kwargs.values()) + (doctor_id,)
            cursor.execute(f"UPDATE Doctors SET {updates} WHERE doctor_id = %s", values)
            self.connection.commit()
            print("Doctor updated successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def assign_doctor_to_patient(self, patient_id, doctor_id):
        cursor = self.connection.cursor()
        try:
            cursor.execute("UPDATE Patients SET doctor_id = %s WHERE patient_id = %s", (doctor_id, patient_id))
            self.connection.commit()
            print("Doctor assigned to patient successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def generate_patient_report_by_doctor(self, doctor_id):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT patient_id, name, age, gender, disease FROM Patients WHERE doctor_id = %s", (doctor_id,))
            patients = cursor.fetchall()
            report = [f"Patient[ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Gender: {row[3]}, Disease: {row[4]}]" for row in patients]
            return report
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()


def main():
    hms = HospitalManagementSystem()

    while True:
        print("\nHospital Management System")
        print("1. Add Patient")
        print("2. Update Patient")
        print("3. Delete Patient")
        print("4. Add Doctor")
        print("5. Update Doctor")
        print("6. Assign Doctor to Patient")
        print("7. Generate Patient Report by Doctor")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                patient_id = int(input("Enter patient ID: "))
                name = input("Enter patient name: ")
                age = int(input("Enter patient age: "))
                gender = input("Enter patient gender: ")
                disease = input("Enter patient disease: ")
                patient = Patient(patient_id, name, age, gender, disease)
                hms.add_patient(patient)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '2':
            try:
                patient_id = int(input("Enter patient ID to update: "))
                print("Enter new details (leave blank to keep unchanged):")
                name = input("Enter new name: ")
                age = input("Enter new age: ")
                gender = input("Enter new gender: ")
                disease = input("Enter new disease: ")
                kwargs = {}
                if name:
                    kwargs['name'] = name
                if age:
                    kwargs['age'] = int(age)
                if gender:
                    kwargs['gender'] = gender
                if disease:
                    kwargs['disease'] = disease
                hms.update_patient(patient_id, **kwargs)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '3':
            try:
                patient_id = int(input("Enter patient ID to delete: "))
                hms.delete_patient(patient_id)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '4':
            try:
                doctor_id = int(input("Enter doctor ID: "))
                name = input("Enter doctor name: ")
                specialization = input("Enter doctor specialization: ")
                doctor = Doctor(doctor_id, name, specialization)
                hms.add_doctor(doctor)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '5':
            try:
                doctor_id = int(input("Enter doctor ID to update: "))
                print("Enter new details (leave blank to keep unchanged):")
                name = input("Enter new name: ")
                specialization = input("Enter new specialization: ")
                kwargs = {}
                if name:
                    kwargs['name'] = name
                if specialization:
                    kwargs['specialization'] = specialization
                hms.update_doctor(doctor_id, **kwargs)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '6':
            try:
                patient_id = int(input("Enter patient ID: "))
                doctor_id = int(input("Enter doctor ID: "))
                hms.assign_doctor_to_patient(patient_id, doctor_id)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '7':
            try:
                doctor_id = int(input("Enter doctor ID to generate report: "))
                report = hms.generate_patient_report_by_doctor(doctor_id)
                print(f"Patients assigned to Doctor ID {doctor_id}:")
                for patient in report:
                    print(patient)
            except ValueError as e:
                print(f"Error: {e}")


        elif choice == '8':
            print("Exiting...")
            hms.close_connection()
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
