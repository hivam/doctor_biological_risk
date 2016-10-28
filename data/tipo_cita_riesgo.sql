INSERT INTO doctor_appointment_type	
    (create_date, write_date, duration, name)
SELECT now(), now(), 15, 'Riesgo Biologico'
WHERE
    NOT EXISTS (
        SELECT name FROM doctor_appointment_type WHERE name='Riesgo Biologico'
    );