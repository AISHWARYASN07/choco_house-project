Create a Simple Python Application for a fictional chocolate house that uses
SQLite to manage,
● Seasonal flavor offerings
● Ingredient inventory
● Customer flavor suggestions and allergy concerns



# Chocolate House Application

Welcome to the Chocolate House application! This web application allows users to manage seasonal chocolate flavors, ingredient inventory, customer suggestions, and allergy concerns for a delightful chocolate experience.

## Features

- **Seasonal Flavors Management**: Add, update, or delete seasonal chocolate flavors.
- **Ingredient Inventory**: Keep track of ingredients used in chocolate production.
- **Customer Suggestions**: Collect and manage customer feedback and suggestions.
- **Allergy Concerns**: Submit and manage allergy concerns while checking for related flavors.


## Technologies Used

- **Backend**: Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript
- **Development Tools**: Python 3.9+ Visual Studio Code



## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>

2. Navigate to the project directory:

   cd chocolate-house

3 .Activate the virtual environment:

      On Windows:
      bash
   
      venv\Scripts\activate

      On macOS/Linux:
      bash

      source venv/bin/activate

4.Install the required packages:

         bash
        
         pip install -r requirements.txt


5. Running the Application
Set the environment variable for Flask:

      bash

      export FLASK_APP=app.py
      (On Windows, use set instead of export.)

Run the application:

     bash

     flask run

     
Open your browser and navigate to http://127.0.0.1:5000 to view the application.
   
