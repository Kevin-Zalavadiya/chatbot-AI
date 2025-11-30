<<<<<<< HEAD
# Health Chatbot

A web-based health chatbot that provides homeopathy medicines and home remedies based on diseases and symptoms.

## Features

- **Treatment Types**: Homeopathy medicines and home remedies
- **Disease Selection**: Choose from available diseases
- **Symptom Matching**: Select symptoms to get targeted treatments
- **Source Information**: Includes sources for all recommendations

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React.js
- **Data**: CSV files with disease, symptom, and treatment information

## Project Structure

```
chatbot/
├── health-chatbot-backend/
│   ├── main.py
│   ├── sample_20_diseases_detailed_symptoms_homeopathy_sources.csv
│   └── home_remedies.csv
├── health-chatbot-frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── ...
│   ├── public/
│   └── package.json
└── README.md
```

## Quick Start

### One-Command Setup

**Option 1: Using Batch File (Recommended for Windows)**
```bash
start.bat
```

**Option 2: Using PowerShell**
```powershell
.\start.ps1
```

Both commands will:
- Start the backend server at `http://localhost:8000`
- Start the frontend server at `http://localhost:3000`
- Open both in separate terminal windows

### Manual Setup (if needed)

#### Backend Setup
1. Install Python dependencies:
   ```bash
   cd health-chatbot-backend
   pip install fastapi uvicorn pandas
   python main.py
   ```

#### Frontend Setup
1. Install and start React app:
   ```bash
   cd health-chatbot-frontend
   npm install
   npm start
   ```

## API Endpoints

- `GET /` - Health check
- `GET /get_diseases?type={homeopathy|remedies}` - Get list of diseases
- `GET /get_symptoms?disease={disease}&type={type}` - Get symptoms for a disease
- `GET /get_treatment?disease={disease}&type={type}&selected_symptoms={symptoms}` - Get treatment recommendations

## Usage

1. Select treatment type (Homeopathy or Home Remedies)
2. Choose a disease from the dropdown
3. Select at least 2 symptoms
4. Click "Get Treatment" to receive recommendations

## Disclaimer

This chatbot is for informational purposes only and should not replace professional medical advice. Always consult with healthcare professionals for medical concerns.

## Contributing

Feel free to contribute by:
- Adding more diseases and treatments
- Improving the UI/UX
- Adding new features
- Fixing bugs

## License

This project is open source and available under the MIT License.
=======
# -chatbot-
>>>>>>> 810625a23365d40c17ca95e4c7a41734e1cb5cb9
