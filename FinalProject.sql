USE mtc;
-- Create tables


-- Drop views
DROP VIEW IF EXISTS ProjectDevicesView;
DROP VIEW IF EXISTS CustomerEmployeeView;


-- Drop transaction
DROP Procedure IF EXISTS PerformMaintenance;

-- Drop tables
DROP TABLE IF EXISTS customer_employee_link;
DROP TABLE IF EXISTS employee_account_link;
DROP TABLE IF EXISTS customer_account_link;
DROP TABLE IF EXISTS `file`;
DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS production_records;
DROP TABLE IF EXISTS device_program;
DROP TABLE IF EXISTS production_info;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS maintenance_info;
DROP TABLE IF EXISTS training;
DROP TABLE IF EXISTS after_sales_analysis;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS employee_account;
DROP TABLE IF EXISTS customer_account;


CREATE TABLE customer_account(
	customer_id INT PRIMARY KEY NOT NULL auto_increment,
    username VARCHAR(255) NOT NULL,
    `password` varchar(255) NOT NULL
);

CREATE TABLE employee_account(
	employee_id INT PRIMARY KEY NOT NULL auto_increment,
    username VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL
);




CREATE TABLE customer (
    customer_id INT PRIMARY KEY NOT NULL auto_increment,
    contact_person VARCHAR(255),
    company_name VARCHAR(255),
    contact_info VARCHAR(255)
);
CREATE TABLE after_sales_analysis (
    analysis_id INT NOT NULL PRIMARY KEY,
    customer_id INT,
    after_sales_person_id INT,
    processing_time DATETIME,
    customer_satisfaction VARCHAR(255),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);
CREATE TABLE employee (
    employee_id INT PRIMARY KEY NOT NULL auto_increment,
    customer_id INT,
    employee_name VARCHAR(50),
    role VARCHAR(50),
    password VARCHAR(50),
    permissions_access VARCHAR(50)

);

CREATE TABLE customer_account_link (
    link_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT ,
    customer_id INT NOT NULL,
    account_id INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (account_id) REFERENCES customer_account(customer_id)
);

CREATE TABLE employee_account_link (
    link_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT ,
    employee_id INT NOT NULL,
    account_id INT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
    FOREIGN KEY (account_id) REFERENCES employee_account(employee_id)
);

CREATE TABLE customer_employee_link (
    link_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT ,
    customer_id INT NOT NULL,
    employee_id INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer_account_link(customer_id),
    FOREIGN KEY (employee_id) REFERENCES employee_account_link(employee_id)
);

CREATE TABLE training (
    training_id INT PRIMARY KEY NOT NULL auto_increment,
    training_content TEXT,
    upload_time DATETIME,
    training_type VARCHAR(255)
);

CREATE TABLE maintenance_info (
    maintenance_info_id INT PRIMARY KEY NOT NULL auto_increment,
    maintenance_type VARCHAR(255),
    maintenance_time DATETIME,
    notes TEXT
);

CREATE TABLE project (
    project_id INT PRIMARY KEY NOT NULL auto_increment,
    customer_id INT,
    project_name VARCHAR(255),
    project_status VARCHAR(255),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE production_info (
    production_info_id INT PRIMARY KEY NOT NULL auto_increment,
    project_id INT,
    output VARCHAR(255),
    runtime INT,
    power_consumption DECIMAL(10, 2),
    FOREIGN KEY (project_id) REFERENCES project(project_id)
);

CREATE TABLE device_program (
    program_id INT PRIMARY KEY NOT NULL auto_increment,
    program_name VARCHAR(255),
    program_version VARCHAR(255),
    expiration_status VARCHAR(255)
);

CREATE TABLE production_records (
    production_records_id INT PRIMARY KEY NOT NULL auto_increment,
    project_id INT,
    issue_description VARCHAR(255),
    status VARCHAR(255),
    completion_time DATETIME,
    FOREIGN KEY (project_id) REFERENCES project(project_id)
);

CREATE TABLE device (
    device_id INT PRIMARY KEY NOT NULL auto_increment,
    project_id INT,
    production_records_id INT,
    production_info_id INT,
    maintenance_info_id INT,
    training_id INT,
    program_id INT,
    device_name VARCHAR(255),
    production_region VARCHAR(255),
    current_location VARCHAR(255),
    sales_status VARCHAR(255),
    person_in_charge VARCHAR(255),
    FOREIGN KEY (project_id) REFERENCES project(project_id),
    FOREIGN KEY (production_records_id) REFERENCES production_records(production_records_id),
    FOREIGN KEY (production_info_id) REFERENCES production_info(production_info_id),
    FOREIGN KEY (maintenance_info_id) REFERENCES maintenance_info(maintenance_info_id),
    FOREIGN KEY (training_id) REFERENCES training(training_id),
    FOREIGN KEY (program_id) REFERENCES device_program(program_id)
);

CREATE TABLE file (
    file_id INT PRIMARY KEY NOT NULL auto_increment,
    device_id INT,
    file_name VARCHAR(255),
    file_type VARCHAR(255),
    upload_time DATETIME,
    FOREIGN KEY (device_id) REFERENCES device(device_id)
);


-- Insert sample data into tables
use mtc;
INSERT INTO customer_account (username, `password`)
VALUES ('zhoudingzhi', '123456789'),
	   ('Chenyang', 'I Love You'),
       ('Dmitriy', 'You Love DB');

INSERT INTO employee_account(username,  `password`)
VALUES ('alexfj6', 'password123' ),
	   ('EmmaT462', 'abc123'),
       ('SarahA3g','gepwd');



INSERT INTO customer (contact_person, company_name, contact_info) VALUES
('Xiaocheng', 'Emerson', 'xiaocheng.ma@emerson.com'),
('Jane', 'Siemens', 'jane.smith@siemens.com'),
('Michael', 'GE', 'michael.johnson@ge.com'),
('Emily', 'ABB', 'emily.davis@abb.com'),
('Chris', 'Westinghouse', 'chris.wilson@westinghouse.com');

INSERT INTO employee (customer_id, employee_name, role, password, permissions_access) VALUES
(1, 'Alex', 'Engineer', 'password123', 'admin'),
(1, 'Emma', 'Technician', 'abc123', 'limited'),
(2, 'Mark', 'Manager', 'pass1234', 'admin'),
( 3, 'Sarah', 'Analyst', 'gepwd', 'limited'),
( 4, 'Ryan', 'Supervisor', 'abbpass', 'admin');

INSERT INTO after_sales_analysis (analysis_id, customer_id, after_sales_person_id, processing_time, customer_satisfaction) VALUES
(1, 1, 1, '2024-03-15 08:30:00', 'Satisfied'),
(2, 2, 3, '2024-03-16 10:45:00', 'Neutral'),
(3, 3, 4, '2024-03-17 13:20:00', 'Dissatisfied'),
(4, 4, 5, '2024-03-18 15:55:00', 'Satisfied'),
(5, 5, 2, '2024-03-19 18:10:00', 'Very Satisfied');

INSERT INTO training (training_id, training_content, upload_time, training_type) VALUES
(1, 'Safety Procedures', '2024-03-01 09:00:00', 'Onsite'),
(2, 'Equipment Maintenance', '2024-03-02 10:30:00', 'Remote'),
(3, 'Quality Control Standards', '2024-03-03 11:45:00', 'Onsite'),
(4, 'Product Training', '2024-03-04 13:15:00', 'Remote'),
(5, 'Customer Service Techniques', '2024-03-05 14:45:00', 'Onsite');

INSERT INTO maintenance_info (maintenance_info_id, maintenance_type, maintenance_time, notes) VALUES
(1, 'Routine Inspection', '2024-03-10 08:00:00', 'Performed regular checkup'),
(2, 'Emergency Repair', '2024-03-11 10:30:00', 'Fixed malfunctioning component'),
(3, 'Preventive Maintenance', '2024-03-12 12:45:00', 'Replaced worn-out parts'),
(4, 'Scheduled Service', '2024-03-13 14:15:00', 'Updated software firmware'),
(5, 'Calibration', '2024-03-14 15:45:00', 'Adjusted sensor accuracy');

INSERT INTO project (project_id, customer_id, project_name, project_status) VALUES
(1, 1, 'Power Plant Upgrade', 'Ongoing'),
(2, 2, 'Factory Automation', 'Completed'),
(3, 3, 'Renewable Energy Initiative', 'Pending'),
(4, 4, 'Grid Modernization', 'Ongoing'),
(5, 5, 'Nuclear Reactor Expansion', 'Planned');

INSERT INTO production_info (production_info_id, project_id, output, runtime, power_consumption) VALUES
(1, 1, '500 MW', 720, 1200.50),
(2, 2, '1000 units/hour', 480, 800.75),
(3, 3, '200 MW', 1440, 2200.25),
(4, 4, '300 MW', 960, 1500.80),
(5, 5, '1000 MW', 2880, 4000.00);

INSERT INTO device_program (program_id, program_name, program_version, expiration_status) VALUES
(1, 'Control System Software', 'v2.0', 'Active'),
(2, 'Monitoring Application', 'v1.5', 'Active'),
(3, 'Diagnostic Tool', 'v3.2', 'Expired'),
(4, 'Firmware Update', 'v4.1', 'Active'),
(5, 'Security Patch', 'v2.3', 'Active');

INSERT INTO production_records (production_records_id, project_id, issue_description, status, completion_time) VALUES
(1, 1, 'Overheating in turbine', 'Resolved', '2024-03-10 08:30:00'),
(2, 2, 'Sensor malfunction', 'Resolved', '2024-03-11 10:45:00'),
(3, 3, 'Power fluctuation', 'Pending', NULL),
(4, 4, 'Communication error', 'Resolved', '2024-03-13 14:30:00'),
(5, 5, 'Equipment calibration', 'Pending', NULL);

INSERT INTO device (device_id, project_id, production_records_id, production_info_id, maintenance_info_id, training_id, program_id, device_name, production_region, current_location, sales_status, person_in_charge) VALUES
(1, 1, 1, 1, 1, 1, 1, 'Turbine Control System', 'North America', 'Site A', 'Active', 'Alex Brown'),
(2, 2, 2, 2, 2, 2, 2, 'Automated Conveyor System', 'Europe', 'Site B', 'Active', 'Emma Lee'),
(3, 3, 3, 3, 3, 3, 3, 'Solar Panel Array', 'Asia', 'Site C', 'Inactive', 'Mark Johnson'),
(4, 4, 4, 4, 4, 4, 4, 'Smart Grid Controller', 'South America', 'Site D', 'Active', 'Sarah Miller'),
(5, 5, 5, 5, 5, 5, 5, 'Nuclear Reactor Core', 'Australia', 'Site E', 'Inactive', 'Ryan Davis');

INSERT INTO file (file_id, device_id, file_name, file_type, upload_time) VALUES
(1, 1, 'Turbine Manual.pdf', 'PDF', '2024-03-10 09:00:00'),
(2, 2, 'Conveyor Troubleshooting Guide.docx', 'Document', '2024-03-11 11:00:00'),
(3, 3, 'Solar Panel Maintenance Checklist.xlsx', 'Spreadsheet', '2024-03-12 13:00:00'),
(4, 4, 'Smart Grid Software Update.exe', 'Executable', '2024-03-13 15:00:00'),
(5, 5, 'Nuclear Safety Regulations.pdf', 'PDF', '2024-03-14 17:00:00');

-- Create indexes

CREATE INDEX idx_contact_person ON customer(contact_person);
CREATE INDEX idx_company_name ON customer(company_name);
CREATE INDEX idx_device_name ON device(device_name);
CREATE INDEX idx_program_name ON device_program(program_name);
CREATE INDEX idx_employee_name ON employee(employee_name);
CREATE INDEX idx_file_name ON file(file_name);
CREATE INDEX idx_file_type ON file(file_type);
CREATE INDEX idx_maintenance_type ON maintenance_info(maintenance_type);
CREATE INDEX idx_project_name ON project(project_name);
CREATE INDEX idx_project_status ON project(project_status);


-- Create views

CREATE VIEW ProjectDevicesView AS
SELECT
    d.device_id,
    d.device_name,
    d.production_region,
    d.current_location,
    d.sales_status,
    d.person_in_charge
FROM
    device d
JOIN
    project p ON d.project_id = p.project_id;

CREATE VIEW CustomerEmployeeView AS
SELECT
    c.customer_id,
    c.company_name,
    c.contact_person,
    e.employee_id,
    e.employee_name,
    e.role
FROM
    customer c
JOIN
    employee e ON c.customer_id = e.customer_id;


-- Create transaction

DELIMITER //

DELIMITER $$

CREATE PROCEDURE PerformMaintenance(IN maintenanceId INT, IN deviceId INT, OUT result VARCHAR(100))
BEGIN
    -- Declare a variable for conditional error handling
    DECLARE exit handler for sqlexception
    BEGIN
        -- Rollback and set result in case of error
        ROLLBACK;
        SET result = 'Maintenance transaction failed.';
        RESIGNAL; -- Resignals the error
    END;

    -- Start transaction
    START TRANSACTION;

    -- Perform INSERT operation
    INSERT INTO maintenance_info (maintenance_info_id, maintenance_type, maintenance_time, notes)
    VALUES (maintenanceId, 'Routine maintenance', NOW(), 'Performed routine maintenance tasks');

    -- Perform UPDATE operation
    UPDATE device
    SET sales_status = 'Maintenance'
    WHERE device_id = deviceId;

    -- If everything went well, commit the transaction
    COMMIT;

    -- Set success result
    SET result = 'Maintenance transaction completed successfully.';
END$$

DELIMITER ;

SELECT * FROM customer_account;
