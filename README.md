# Appium Manager

## Overview

Django Appium Manager is a web application designed to manage and automate the testing of Android APKs. This application allows users to upload Android APK files, run automated UI tests using Appium, and manage the results. The app also supports accessibility features and multilingual functionality.

## Features

1. **User Authentication and Management**
   - Users can register, log in, and manage their accounts securely.
2. **App Management**

   - Users can upload, list, update, and delete Android APK files.
   - APKs are automatically evaluated using Appium when a user triggers a test.
   - Test results, including screenshots, UI hierarchy, and logs, are stored and displayed.

3. **App Evaluation with Appium**

   - Automated tests run on an Android emulator:
     - Launch the emulator.
     - Install the APK.
     - Capture UI elements on the initial screen.
     - Simulate a click on the first button and detect screen changes.
     - Save screenshots, video recordings, and UI hierarchy.
   - Test results are stored in the database.

4. **Accessibility Features**

   - Options to increase font size and switch to high contrast mode for better visibility.
   - Accessible design practices are implemented across the application.

5. **Multilingual Support**
   - The application supports English and French languages.
   - Users can dynamically switch between languages.

## Technology Stack

- **Backend**: Django, MySQL
- **Frontend**: Django Templates, HTML, CSS, JavaScript
- **Testing**: Appium
- **Deployment**: Docker

## Installation

### Prerequisites

1. **Python** (3.8+)
2. **Node.js and npm** (for Appium)
3. **Appium** (installed globally)
4. **Java Development Kit (JDK)**
5. **Android SDK and AVD Manager** (for Android emulators)
6. **MySQL** (database)
7. **Docker** (optional, for containerized deployment)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/essam5/Appium-Manager.git
   cd appium_manager
   ```

# Django Appium Manager

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Set Up the Database

```bash
python manage.py migrate
```

## Create a Superuser

```bash
python manage.py createsuperuser
```

## Start the Django Development Server

```bash
python manage.py runserver
```

## Set Up Appium and Start Appium Server

1. **Install Appium globally if not already installed:**

```bash
npm install -g appium
appium
```

3. **Set Up an Android Emulator**:

   Use Android Studio to create and launch an Android Virtual Device (AVD).
   Ensure the emulator is running before testing.

## Testing

1. **Upload an APK** - Log in to the application. - Navigate to the "Manage Apps" section and upload an APK file.

2. **Run Tests**

   - Click on the "Run Test" button next to the uploaded APK. - The test will run on the connected Android emulator. - View the results, including screenshots, video recordings, and UI hierarchy, in the app.

3. **Check Accessibility Features**

   - Test the accessibility features by increasing the font size or switching to high contrast mode.

4. **Switch Language**
   - Use the language switcher to toggle between English and French.

## Deployment

## Using Docker

1. **Build the Docker Image**

```bash
docker build -t django-appium-manager .
```

2. **Run the Docker Container**

```bash
docker-compose up -d
```

3. **Access the Application**
   - The application will be accessible at http://localhost:8000.
