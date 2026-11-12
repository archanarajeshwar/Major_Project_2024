# AnemiCheck

AnemiCheck is a student project that combines image-based anemia screening with complete blood count (CBC) report analysis and health recommendations. It also includes a Flask portal for user accounts and related services.

> **Medical notice:** This project is for educational and demonstration purposes only. Its image-based screening, report summaries, anemia classifications, and AI-generated recommendations are not medical diagnoses or treatment advice. Results may be inaccurate; consult a qualified healthcare professional.

## Features

- **Image-based screening:** Processes an uploaded image with OpenCV and a YOLOv5 model, then estimates hemoglobin using image color values and a threshold.
- **CBC report analysis:** Extracts text and differential counts from uploaded PDF reports.
- **Personalized recommendations:** Uses the OpenAI API to generate a report summary, anemia information, dietary suggestions, activity ideas, and preventive measures based on CBC data and user-provided details.
- **User portal:** Flask pages for signup, sign-in, profile, image screening, CBC upload, and hospital lookup.
- **Charts and interface:** HTML/CSS/JavaScript templates, Bootstrap, and Chart.js.

## Technologies

| Area | Technologies |
| --- | --- |
| Web application | Python, Flask, Jinja templates, Flask-CORS |
| Database | MySQL, PyMySQL, MySQL Connector/Python |
| Image processing and screening | OpenCV, NumPy, YOLOv5, PyTorch |
| CBC PDF extraction | pdfplumber |
| AI-generated recommendations | OpenAI API |
| Hospital lookup | Requests and SerpAPI |
| Frontend | HTML, CSS, JavaScript, Bootstrap, Chart.js |

## Project layout

```text
.
├── app.py                 # Main Flask portal
├── address.py             # Hospital search integration
├── data_extraction.py     # CBC PDF text and value extraction
├── maksad_khatam1.py      # Image processing and YOLOv5 screening
├── prompt.py              # OpenAI prompts for CBC recommendations
├── templates/             # Flask/Jinja pages
├── static/                # CSS, JavaScript, and static assets
├── recommendation/        # Standalone CBC report app
└── yolov5/                # YOLOv5 Git submodule
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/archanarajeshwar/Major_Project_2024.git
cd Major_Project_2024
git submodule update --init --recursive
```

Use Python 3.10 or another version supported by the installed YOLOv5/PyTorch dependencies. Create and activate a virtual environment, then install the project dependencies:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install Flask PyMySQL numpy pandas requests pdfplumber openai
```

Install the PyTorch version appropriate for your operating system and hardware, and install the YOLOv5 submodule's dependencies as described in its documentation.

### 2. Configure environment variables

Copy `.env.example` to `.env` as a reference, then set the variables in your shell or deployment environment. The application reads environment variables directly; it does not automatically load `.env`.

Required variables for the main portal:

- `OPENAI_API_KEY` — OpenAI API key for CBC recommendations.
- `SERPAPI_API_KEY` — SerpAPI key for hospital search.
- `FLASK_SECRET_KEY` — long, random secret for Flask sessions.
- `DB_PASSWORD` — password for the MySQL account.

Optional database variables default to `localhost`, user `root`, and database `anemia_detection`:

- `DB_HOST`
- `DB_USER`
- `DB_NAME`

For example, set these in PowerShell for the current terminal session:

```powershell
$env:OPENAI_API_KEY = "your-key"
$env:SERPAPI_API_KEY = "your-key"
$env:FLASK_SECRET_KEY = "your-random-secret"
$env:DB_PASSWORD = "your-database-password"
```

Create and initialize the MySQL database and tables expected by the portal before starting it. Database schema/migrations are not included in this repository.

### 3. Prepare the screening model and local directories

The image-screening code expects a trained model at `yolov5/runs/train/exp/weights/best.pt`. Supply or train the project-specific weights at that location before using image screening. The repository-level `best.pt` file is also included, but the current screening code uses the path inside the YOLOv5 submodule.

Uploaded PDFs and generated images are stored locally in the `uploads/`, `input_img/`, `output_img/`, and `edit_img/` folders. These folders are excluded from Git to avoid committing personal or medical data.

### 4. Run the application

Start the main portal from the repository root:

```powershell
python app.py
```

Open [http://localhost:5000](http://localhost:5000).

The standalone CBC recommendation app is in `recommendation/`. It also requires `OPENAI_API_KEY`:

```powershell
cd recommendation
python app.py
```

## Important notes

- Uploaded CBC reports and health-related images can contain sensitive personal information. Do not commit or publicly share real patient data.
- Keep API keys, database passwords, and Flask secrets out of source control. `.env` is ignored by Git; `.env.example` contains placeholders only.
- AI output and image-based estimates can be incomplete or wrong. A clinician should interpret CBC results and recommend care.
- Dependency versions and a database schema are not fully pinned/provided yet; local setup may require adjustments for your Python, PyTorch, and MySQL versions.
