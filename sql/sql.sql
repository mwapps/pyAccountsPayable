
drop user IF EXISTS ap_demo;
drop SCHEMA IF EXISTS ap_demo;
drop database IF EXISTS ap_demo;

create user ap_demo with encrypted password 'mwapps54321';
create SCHEMA ap_demo AUTHORIZATION ap_demo;
create database ap_demo;
GRANT CONNECT ON DATABASE ap_demo TO ap_demo;
grant all privileges on database ap_demo to ap_demo;


drop TABLE IF EXISTS movements;
drop TABLE IF EXISTS users;
drop TABLE IF EXISTS rules;
drop TABLE IF EXISTS documents;
drop TABLE IF EXISTS suppliers;
drop TABLE IF EXISTS companies;

CREATE TABLE users (
    user_id serial PRIMARY KEY,
    user_name VARCHAR ( 15 ) NOT NULL,
    user_email VARCHAR ( 120 ) NOT NULL,
    user_pass VARCHAR ( 120 ) NOT NULL
);

CREATE TABLE companies (
	company_id serial PRIMARY KEY,
	business_name VARCHAR ( 50 ) NOT NULL
);

CREATE TABLE suppliers (
	supplier_id serial PRIMARY KEY,
	supplier_name VARCHAR ( 50 ) NOT NULL
);

CREATE TABLE documents (
    company_id integer NOT NULL,
	supplier_id integer NOT NULL,
	document_number VARCHAR ( 12 ) NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE,
    reference VARCHAR(12),
    previous_balance money,
    total_debits money,
    total_credits money,

    PRIMARY KEY (company_id, supplier_id, document_number),
	FOREIGN KEY (company_id)
      REFERENCES companies (company_id),
	FOREIGN KEY (supplier_id)
      REFERENCES suppliers (supplier_id)
);

CREATE TABLE rules(
	rule_id serial PRIMARY KEY,
    rule_description VARCHAR(50) NOT NULL,
    action_over_document VARCHAR(1) NOT NULL,  --C=create / U=update / A=any
    movement_type VARCHAR(1) NOT NULL,         --D=debit / C=credit / N=not affected
    update_issue_date VARCHAR(1) NOT NULL,     --Y=yes / N=no
    update_due_date VARCHAR(1) NOT NULL,       --Y=yes / N=no
    update_reference VARCHAR(1) NOT NULL      --Y=yes / N=no
);

CREATE TABLE movements (
	movement_id serial NOT NULL,
    movement_date DATE NOT NULL,
    company_id integer NOT NULL,
	supplier_id integer NOT NULL,
	document_number VARCHAR ( 12 ) NOT NULL,
    rule_id integer NOT NULL,
    amount money NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE,
    reference VARCHAR(12),
    user_id integer NOT NULL,

    PRIMARY KEY (movement_id),
	FOREIGN KEY (company_id)
      REFERENCES companies (company_id),
	FOREIGN KEY (supplier_id)
      REFERENCES suppliers (supplier_id),
	FOREIGN KEY (rule_id)
      REFERENCES rules (rule_id),
	FOREIGN KEY (company_id, supplier_id, document_number)
      REFERENCES documents (company_id, supplier_id, document_number),
	FOREIGN KEY (user_id)
      REFERENCES users (user_id)
);
