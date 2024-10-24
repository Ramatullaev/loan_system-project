CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    dob DATE NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    work VARCHAR(100) NOT NULL,
    salary NUMERIC NOT NULL,
    debts NUMERIC NOT NULL,
    loan_amount NUMERIC NOT NULL,
    repayment_amount NUMERIC NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
