# Multi-Channel Customer Query Router with AI-Powered NLP

## 🎯 Project Overview

An intelligent customer support ticket routing system that uses Natural Language Processing (NLP) and Retrieval Augmented Generation (RAG) to automatically classify, route, and respond to customer queries across multiple channels (email, chat, forms).

## ✨ Key Features

- **AI-Powered Intent Classification**: Uses Google Gemini AI to semantically understand customer queries
- **Automatic Ticket Routing**: Routes tickets to appropriate teams (Tech Support, Compliance, Sales, etc.) based on NLP analysis
- **Multi-Channel Support**: Handles queries from email, chat, and web forms
- **RAG-Based Response Generation**: Generates personalized responses using HTML knowledge base
- **Learning System**: Adapts and improves routing accuracy over time
- **Real-time Dashboard**: Web interface for monitoring tickets and routing decisions
- **Sentiment Analysis**: Detects urgency and sentiment to prioritize critical issues

## 🏗️ Architecture

```
Customer Query (Email/Chat/Form)
    ↓
NLP Classification (Intent, Urgency, Sentiment, Entities)
    ↓
Smart Routing Decision
    ↓
RAG Response Generation (from HTML knowledge base)
    ↓
Ticket Creation & Team Assignment
    ↓
Auto-Response & Escalation Handling
```

## 🛠️ Technology Stack

- **Backend**: Python 3.11+, Flask
- **AI/ML**: Google Gemini AI (Generative AI)
- **Database**: SQLite
- **Frontend**: HTML, JavaScript, CSS
- **NLP**: Custom intent classification with entity extraction
- **RAG**: Semantic search with HTML knowledge base

## 📋 Prerequisites

- Python 3.11 or higher
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))
- pip (Python package manager)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Agnethink
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 5. Initialize the System

```bash
python init_system.py
```

### 6. Run the Application

```bash
python app.py
```

Or use the startup script:

```bash
python start.py
```

The web interface will be available at: `http://localhost:8000`

## 📁 Project Structure

```
Agnethink/
├── agent/                      # Core agent components
│   ├── router_agent.py        # Main RouterAgent class
│   ├── intent_classifier.py   # NLP classification
│   ├── rag_system.py          # RAG response generation
│   ├── learning_system.py     # Learning & adaptation
│   ├── ticket_manager.py      # Ticket management
│   ├── database.py            # Database operations
│   └── config.py              # Configuration
├── templates/                  # HTML templates
│   ├── index.html            # Main dashboard
│   ├── email_channel.html    # Email interface
│   └── debug_tickets.html    # Ticket debugging
├── pages/                     # RAG knowledge base (HTML)
│   ├── kyc_pending.html
│   ├── api_error_403.html
│   └── ...
├── app.py                     # Flask application
├── requirements.txt           # Python dependencies
├── init_system.py            # System initialization
└── README.md                 # This file
```

## 🔌 API Endpoints

### Submit Query
```bash
POST /api/submit_query
Content-Type: application/json

{
  "channel": "email",
  "message": "API error 403 blocking payments",
  "sender": "dev@company.com",
  "subject": "Urgent: API Issue"
}
```

### Submit Email
```bash
POST /api/submit_email
Content-Type: application/json

{
  "from": "customer@example.com",
  "subject": "Billing dispute",
  "body": "Invoice shows incorrect charge"
}
```

### Get Tickets
```bash
GET /api/tickets?status=open
```

### Get Statistics
```bash
GET /api/stats
```

## 🧪 Testing

Run the demo:
```bash
python demo.py
```

Run specific tests:
```bash
python test_auto_routing.py
python test_nlp_routing.py
```

## 📊 Features Explained

### 1. Intent Classification
- Analyzes customer messages semantically
- Classifies into categories: technical_support, billing_finance, kyc_verification, etc.
- Extracts key entities (error codes, amounts, dates)
- Determines urgency level (critical, high, medium, low)

### 2. Smart Routing
- Routes to appropriate teams based on intent
- Handles edge cases (disputes → Compliance Team)
- Low confidence queries → Triage Team
- Escalates critical/high urgency tickets

### 3. RAG Response Generation
- Uses HTML pages as knowledge base
- Semantic search for relevant context
- Generates personalized responses using Gemini AI
- Includes templates and use cases

### 4. Learning System
- Learns from routing decisions
- Updates classification patterns
- Improves accuracy over time

## 🔧 Configuration

Edit `agent/config.py` to customize:
- Team assignments
- Urgency levels
- Response time SLAs
- Escalation rules

## 📝 Database

The system uses SQLite database (`query_router.db`). View database:
```bash
python view_database.py
```

## 🐛 Troubleshooting

### API Key Issues
- Ensure `GOOGLE_API_KEY` is set in `.env`
- Verify API key is valid and has quota

### Port Already in Use
- Default port is 8000
- Use `python app.py <port>` to specify different port

### Database Errors
- Run `python init_system.py` to reinitialize
- Check file permissions for database file

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

See [DATA_ATTRIBUTION.txt](DATA_ATTRIBUTION.txt) for acknowledgments of open-source tools, datasets, and APIs used.

## 👥 Team

[Your Team Name]
- [Team Member 1]
- [Team Member 2]
- [Team Member 3]

## 📧 Contact

For questions or support, please contact: [your-email@example.com]

## 🔗 Links

- GitHub Repository: [Your Repository URL]
- Demo Video: [Link to demo video]
- Presentation: [Link to presentation deck]

---

**Built for AgenThink Hackathon 2025**

