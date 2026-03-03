# Projeto Sompo - Tax Management System

A robust web application developed to manage, calculate, and report tax obligations. This system automates complex fiscal workflows, ensuring compliance with Brazilian tax regulations through a structured data processing pipeline.

## 🚀 Features

- **Tax Calculation Engine:** Automated modules for PIS, COFINS, IRPJ, CSLL, and PSL.
- **Balance Sheet Management:** Tools for uploading, listing, and analyzing "Balancetes".
- **Fiscal Reporting:** Generation of detailed reports for auditing and tax filing.
- **User Authentication:** Secure access control with profile management and password reset flows.
- **Responsive Dashboard:** A clean UI built with Bootstrap for financial monitoring.

## 🛠 Tech Stack

- **Backend:** Python / [Django Framework](https://www.djangoproject.com/)
- **Frontend:** HTML5, CSS3, JavaScript (jQuery), Bootstrap
- **Database:** PostgreSQL / SQLite (Development)
- **Architecture:** MVC (Model-View-Controller)

## 📁 Project Structure

The core logic is located within the `ibs` application:
- `models.py`: Defines the fiscal data structure (Calculations, Users, and Reports).
- `views.py`: Contains the business logic for tax apuration.
- `templates/`: Custom UI components for tax forms and lists.

##📄 License
This project is developed for internal tax management purposes. All rights reserved.
