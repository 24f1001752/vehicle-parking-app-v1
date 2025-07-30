# vehicle-parking-app-v1
This is a dummy project that manages different parking lots, parking spots and parked vehicles

# 🚗 Vehicle Parking App Project

## 👨‍💻 Author

- **Name**: Anish Abhyankar  
- **Roll Number**: 24F1001752  
- **Student Email**: 24f1001752@ds.study.iitm.ac.in  


## 📄 Description

**Vehicle Parking App** is a web-based system for managing and reserving parking spots.  
Users can register, log in, and reserve parking spots from various lots. They can also view their profile, reservation history, and usage summary.  
Admins have extended privileges like adding, editing, and deleting parking lots and spaces, along with full access to user functions.


## 📁 Project Structure

vehicle-parking-app/
├── app.py # Main Flask app initialization
├── config.py # Configuration using environment variables
├── models.py # SQLAlchemy database models
├── routes.py # All application routes and logic
├── requirements.txt # Python dependencies
├── README.md # Project documentation (this file)
├── instance/
│ └── db.sqlite3 # SQLite database file
├── static/
│ ├── parking_lot_summary.png # Admin chart image
│ └── user_parking_history.png # User chart image
├── templates/
│ ├── layout.html # Base HTML layout
│ ├── nav-bar.html # Navigation bar
│ ├── signin.html, signup.html # Authentication pages
│ ├── admin_home.html # Admin dashboard
│ ├── admin_user.html # Admin user list
│ ├── admin_summary.html # Admin chart view
│ ├── user_summary.html # User chart view
│ ├── home.html # User home with lot search
│ ├── profile.html # User profile page
│ ├── parked_history.html # User booking history
│ ├── delete_lot.html # Lot deletion confirmation
│ ├── parkinglot/ # Lot management templates
│ │ ├── add.html, edit.html, show.html
│ └── parking_spot/ # Spot booking/releasing templates
│ ├── book_parking.html, leave_spot.html, delete.html


## 🛠️ Technologies Used

1. **Flask** – Lightweight web framework for handling routing, views, and responses.
2. **Flask-SQLAlchemy** – ORM for interacting with the SQLite database using Python classes.
3. **SQLite** – Serverless, lightweight relational database for storing user, lot, and booking data.
4. **Werkzeug Security** – Used for hashing and verifying passwords securely.
5. **Jinja2** – Templating engine for rendering dynamic HTML with Python syntax.
6. **Bootstrap 5** – For building responsive and styled UI components.
7. **Matplotlib** – For generating admin and user dashboard bar charts.
8. **Flask-Dotenv** – Loads configuration securely from a `.env` file.



## 🧱 Database Schema and Table Descriptions

### 1) User Table
- **Id**: Primary Key, unique identifier for each user  
- **Username**: Unique login credential, not nullable  
- **Passhash**: Secure hashed password, not nullable  
- **Name**: User's full name, nullable  
- **Email**: Unique email ID, nullable  
- **Address**: Address, nullable  
- **Pincode**: Address pincode, nullable  
- **Isadmin**: Boolean flag to indicate if user is an admin  
- **Relationship**: One-to-many with `Reserveparkingspot`  

**Purpose**: Stores personal and account information of all users.



### 2) Parkinglot Table
- **Id**: Primary Key  
- **Primary_location_name**: Unique location name, not nullable  
- **Price**: Price per hour, not nullable  
- **Address**: Lot address, not nullable  
- **Pin_code**: Pincode, not nullable  
- **Maximum_number_of_spots**: Configured capacity of the lot  
- **Relationship**: One-to-many with `Parkingspace` and `Reserveparkingspot`  

**Purpose**: Stores data for different parking lot locations and pricing.



### 3) Parkingspace Table
- **Id**: Primary Key  
- **Lot_id**: Foreign Key referencing `Parkinglot`, not nullable  
- **Status**: Current status (`available` or `occupied`), not nullable  
- **Relationship**: One-to-many with `Reserveparkingspot`  

**Purpose**: Tracks each parking space and its availability status.


### 4) Reserveparkingspot Table
- **Id**: Primary Key  
- **Lot_id**: Foreign Key referencing `Parkinglot`, not nullable  
- **Spot_id**: Foreign Key referencing `Parkingspace`, not nullable  
- **User_id**: Foreign Key referencing `User`, not nullable  
- **Vehicle_number**: User’s vehicle number, not nullable  
- **Parking_timestamp**: Start time, not nullable  
- **Leaving_timestamp**: End time, nullable  
- **Parking_cost**: Calculated cost, nullable  
- **Relationship**: Many-to-one with `User`, `Parkinglot`, `Parkingspace`  

**Purpose**: Records all parking reservations and billing information.


## 🏗️ Architecture

The project follows a **Model-View-Controller (MVC)**-style structure:

- `app.py`: Initializes the Flask app and loads configuration.
- `models.py`: Defines the data models using SQLAlchemy.
- `routes.py`: Contains all route logic for users and admins.
- `templates/`: Jinja2 HTML templates (home, dashboard, booking pages, etc.)
- `config.py`: Loads settings from `.env` using Flask-Dotenv.


## 🌟 Core Features

- Secure **user authentication** with hashed passwords and sessions.
- **Admin dashboard** to add, edit, or delete lots and parking spots.
- **User interface** for booking and releasing parking spots.
- Real-time update of **spot availability status** (`available` / `occupied`).
- **Search** parking lots by name or pincode.
- **Summary charts** using Matplotlib for admin and user dashboards.
- **Responsive UI** using Bootstrap.

