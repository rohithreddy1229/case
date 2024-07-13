CREATE DATABASE HospitalDB;

USE HospitalDB;
CREATE TABLE Doctors (
    doctor_id INT PRIMARY KEY,
    name VARCHAR(100),
    specialization VARCHAR(100)
);

CREATE TABLE Patients (
    patient_id INT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    disease VARCHAR(100),
    doctor_id INT,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
);
SELECT * FROM patients;
SELECT * FROM doctors;

-- 1) to find the total number of patients assigned to each doctor.
SELECT doctor_id, COUNT(*) AS total_patients
FROM Patients
GROUP BY doctor_id;

-- 2) to find the names of doctors and the total number of patients assigned to them.
SELECT d.name AS doctor_name, COUNT(p.patient_id) AS total_patients
FROM Doctors d
LEFT JOIN Patients p ON d.doctor_id = p.doctor_id
GROUP BY d.doctor_id, d.name;

-- 3) to find the names of patients who have not been assigned a doctor.
SELECT name 
FROM Patients
WHERE doctor_id IS NULL;

-- 4) to find the specializations of doctors who have more than 10 patients assigned.
SELECT d.specialization
FROM Doctors d
JOIN Patients p ON d.doctor_id = p.doctor_id
GROUP BY d.doctor_id, d.specialization
HAVING COUNT(p.patient_id) > 10;

-- 5)to find the patient names and their corresponding diseases for patients assigned to a specific doctor.
SELECT p.name AS patient_name, p.disease
FROM Patients p
WHERE p.doctor_id = 101;  -- can give any doctor_id

