Here’s the corrected and improved README file in Markdown (`.md`) format:

# Face Recognition System for Operator Management

This project is a face recognition-based operator management system that enables:
- **Admin Login**: For administrators to access and manage the system.
- **Face Scanning**: Real-time face capture and recognition for operator attendance.
- **API Server**: Backend API to support data exchange and integration.
- **Entry/Departure Signal**: Interactive interface for operators to log their arrival or departure.

---

## Features

- **Real-Time Face Scanning**: Uses a camera to capture faces and match them against a database of registered operators.
- **Flexible Command Execution**: Supports running multiple modes (e.g., admin login, API server, face scanning) in parallel using threading.
- **Operator Management**: Allows operators to log their arrival or departure with face recognition.
- **Admin Login Interface**: Provides a graphical user interface (GUI) for administrators to access the system.
- **REST API Support**: Offers an API server to handle external system integrations.

---

## System Requirements

- Python 3.8+
- Libraries:
  - `cv2` (OpenCV)
  - `flask` (for API server)
  - `uuid` (for unique file naming)
  - `os`, `threading` (for file and thread management)
  - Any additional dependencies required by your specific modules (e.g., `functions`, `Arrival`, `Departure`, `session`, etc.)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/face-recognition-system.git
   cd face-recognition-system
```

2. Install required libraries:
   ```bash
   pip install -r requirements.txt
```

3. Ensure the following directories are set up:
   - `captured_images/`: Directory for saving captured images.
   - `models/`: Directory containing pre-trained face recognition models (if applicable).

4. Configure your database connection and tables if using SQLAlchemy:
   - Tables:
     - `Arrival`: Stores operator arrival data.
     - `Departure`: Stores operator departure data.
   - Update the database session setup in `functions.py`.

---

## Usage

Run the main script:
```bash
python main.py
```

### Available Commands
- `admin`: Launches the admin login page.
- `scan`: Starts the face scanning module to capture operator faces in real time.
- `api`: Starts the backend API server on `http://0.0.0.0:8080`.
- `signal`: Prompts the user to log an operator’s arrival or departure via the graphical interface.
- `help`: Displays help information about available commands.

You can run multiple commands simultaneously by separating them with commas:
```bash
Enter mode(s): admin, scan, api
```

---

## File Structure

```
project/
├── api/
│   └── app.py             # API server implementation
├── cam/
│   ├── detect.py          # Face detection and recognition module
│   └── interface.py       # User interface for arrival/departure
├── ui/
│   └── login.py           # Admin login GUI
├── functions.py           # Core functions (e.g., face comparison, database operations)
├── main.py                # Entry point for the application
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
└── captured_images/       # Directory for saving captured images
```

---

## How It Works

### Admin Login
- Launch the admin page by running the `admin` command.
- The administrator can manage operator profiles, view logs, or perform other administrative tasks.

### Face Scanning
- Runs in real time to capture and process operator faces.
- Matches the captured face with registered operators in the database.

### API Server
- Serves as the backend for data management and external system integration.
- Hosts REST endpoints for handling operator data, logs, and other queries.

### Signal Interface
- Prompts the user to select arrival or departure.
- Uses face recognition to match the operator and register their attendance.

---

## Example Scenarios

### Admin Login
```bash
Enter mode(s): admin
```
Opens the admin login GUI for management.

### Start API Server and Face Scanning Simultaneously
```bash
Enter mode(s): api, scan
```
Runs the API server and starts the face scanning module.

### Signal Entry/Departure
```bash
Enter mode(s): signal
```
Launches an interactive GUI for operator attendance.

---

## Extending the Project

### Adding New Features
- **New Commands**:
  - Add a new command in the `command_map` dictionary in `main.py`.
  - Define the corresponding function for the new mode.
- **Database Enhancements**:
  - Add new tables or fields in the database.
  - Update SQLAlchemy models and modify queries in `functions.py`.
- **UI Customization**:
  - Update the GUI for admin login or signaling by modifying `ui/login.py` or `cam/interface.py`.

### Scaling the System
- Use asynchronous processing (e.g., `asyncio` or `concurrent.futures`) for better performance.
- Deploy the API server on a cloud platform like AWS, Azure, or Google Cloud for accessibility.
- Use Docker for containerizing the application.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributors

- **Your Name**: Djiatsa Dunamis
- Open for contributions! Feel free to fork the project and submit pull requests.

---

## Support

If you encounter any issues, please open an issue in the GitHub repository or contact the maintainer.
