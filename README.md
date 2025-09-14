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

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd health-chatbot-backend
   ```

2. Install dependencies:
   ```bash
   pip install fastapi uvicorn pandas
   ```

3. Run the backend server:
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd health-chatbot-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

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