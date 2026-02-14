# 📖 NAHB - Not Another Hero's Book

A Django + Flask web application for creating and playing interactive **Choose Your Own Adventure** stories.

## 🎯 Project Overview

**NAHB** is a progressive web application that allows authors to create branching narratives and readers to play through interactive stories with meaningful choices. The application features user authentication, role-based permissions, story statistics, and a medieval book-themed aesthetic.

### Architecture
- **Flask REST API** — Story content management and narrative engine
- **Django Web App** — User interface, gameplay tracking, and authentication
- **SQLite Databases** — Separate storage for Flask (stories) and Django (users/plays)

---

## 📊 Feature Levels

### ✅ Level 10/20 — MVP (Complete)
- Anonymous story browsing and playing
- Story creation, editing, publishing
- Page and choice management
- Play tracking and basic statistics
- Ending distribution analytics

### ✅ Level 13/20 — Advanced UX (Complete)
- Named endings with labels
- Ending distribution percentages
- Draft/Published story visibility
- Delete confirmations on all destructive actions
- Improved UI/UX with book aesthetic

### ✅ Level 16/20 — Security & Permissions (Complete)
- User registration and authentication
- Role-based access (Reader/Author/Admin)
- Story ownership enforcement
- Admin story suspension
- Protected author tools (login required)
- Play records linked to users

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.13+
- Git
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/NAHB.git
cd NAHB
```

### 2. Set Up Flask API

```bash
cd FlaskAPI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo API_KEY=nahb-secret-key-2026 > .env
echo FLASK_ENV=development >> .env

# Run Flask API (port 5000)
python app.py
```

Flask API will start at: **http://localhost:5000/api**

### 3. Set Up Django App

In a **new terminal**:

```bash
cd DjangoApp

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DEBUG=True
SECRET_KEY=django-insecure-dev-key
FLASK_API_URL=http://localhost:5000/api
FLASK_API_KEY=nahb-secret-key-2026
ALLOWED_HOSTS=localhost,127.0.0.1
EOF

# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Enter username, email, password when prompted

# Collect static files
python manage.py collectstatic --noinput

# Run Django dev server (port 8000)
python manage.py runserver
```

Django app will start at: **http://localhost:8000**

### 4. Test the Application

1. **Visit** http://localhost:8000
2. **Register** as a new user (choose Reader or Author role)
3. **Create a story** (if Author role):
   - Click "Write" → "Begin Your Tale"
   - Enter title and description
   - Save
4. **Add pages** to your story:
   - Click "Edit Story"
   - Click "Add New Page"
   - Write scene description
   - Mark as ending if applicable
5. **Create choices** linking pages together:
   - Click "Add Choice" on a page
   - Write choice text
   - Select destination page
6. **Publish** your story:
   - Edit story → Set Status to "Published"
   - Save Changes
7. **Play stories**:
   - Browse published stories
   - Click "Play" to start
   - Make choices to progress through the story
8. **View statistics**:
   - Click "Stats" to see global play data
   - View individual story stats on story detail page

---

## 📁 Project Structure

```
NAHB/
├── FlaskAPI/                          # REST API for story content
│   ├── app.py                         # Flask application entry point
│   ├── config.py                      # Configuration management
│   ├── requirements.txt                # Python dependencies
│   ├── .env                            # Environment variables (local only)
│   ├── models/
│   │   ├── __init__.py                # SQLAlchemy database setup
│   │   └── flaskModel.py              # Story, Page, Choice models
│   ├── services/
│   │   └── story_service.py           # Business logic for stories
│   ├── controllers/
│   │   └── story_controller.py        # Request handlers
│   └── routes/
│       └── story_routes.py            # API endpoint routing
│
├── DjangoApp/                         # Web application & UI
│   ├── manage.py                      # Django management
│   ├── requirements.txt                # Python dependencies
│   ├── .env                            # Environment variables (local only)
│   ├── NovelPlayer/                   # Main Django project
│   │   ├── settings.py                # Django configuration
│   │   ├── urls.py                    # URL routing
│   │   └── wsgi.py                    # WSGI application (production)
│   ├── game/                          # Main Django app
│   │   ├── models.py                  # Play, UserProfile models
│   │   ├── views.py                   # View logic
│   │   ├── urls.py                    # App URL routing
│   │   ├── services.py                # Flask API client
│   │   ├── auth_views.py              # Authentication views
│   │   └── templates/                 # HTML templates
│   │       ├── base.html              # Base template with styling
│   │       ├── auth/                  # Login/Register pages
│   │       ├── stories/               # Story browsing pages
│   │       ├── play/                  # Gameplay pages
│   │       ├── stats/                 # Statistics pages
│   │       └── author/                # Story creation/editing pages
│   └── static/                        # CSS, JavaScript (production)
│
└── README.md                          # This file
```

---

## 🔌 Flask API Endpoints

### Stories (Public Read)
```
GET  /api/stories              — List all stories
GET  /api/stories?status=published  — List published stories only
GET  /api/stories/<id>         — Get story details
GET  /api/stories/<id>/start    — Get story's starting page
GET  /api/stories/<id>/pages   — Get all pages in a story
```

### Stories (Protected Write - Requires API Key)
```
POST   /api/stories            — Create new story
PUT    /api/stories/<id>       — Update story details
DELETE /api/stories/<id>       — Delete story
```

### Pages (Protected Write)
```
GET  /api/pages/<id>                  — Get page details with choices
POST /api/stories/<id>/pages          — Create new page
DELETE /api/pages/<id>                — Delete page
```

### Choices (Protected Write)
```
POST   /api/pages/<id>/choices        — Create choice on a page
DELETE /api/choices/<id>              — Delete choice
```

---

## 🔐 Authentication & Roles

### User Roles

**Reader** (Default)
- Browse and play published stories
- View story statistics
- Play history tracking

**Author**
- Create, edit, delete own stories
- Create pages and choices
- View own story statistics
- Cannot modify other authors' stories

**Admin** (is_staff=True)
- All Author permissions
- View global statistics
- Suspend stories (hide from public)
- Modify any story
- Access Django admin panel

### Login Credentials (Local Dev)

Create via registration or:
```bash
python manage.py createsuperuser
```

---

## 🗄️ Database Models

### Flask (story content only)

**Story**
```
- id (Primary Key)
- title (String)
- description (String)
- status (draft/published/suspended)
- author_id (Username of creator)
- start_page_id (Foreign Key to Page)
```

**Page**
```
- id (Primary Key)
- story_id (Foreign Key to Story)
- text (String, 4096 chars max)
- is_ending (Boolean)
- ending_label (String, optional)
```

**Choice**
```
- id (Primary Key)
- page_id (Foreign Key to Page)
- text (String)
- next_page_id (Foreign Key to Page)
```

### Django (gameplay & users only)

**User** (Django built-in)
```
- id, username, email, password
- is_staff (for admin role)
```

**UserProfile**
```
- user (One-to-One with User)
- role (reader/author/admin)
```

**Play**
```
- id (Primary Key)
- user (Foreign Key to User, optional for anonymous)
- story_id (Integer, references Flask story)
- ending_page_id (Integer)
- ending_label (String)
- created_at (Timestamp)
```

---

## 🎨 Styling & UI

The application features a **medieval book aesthetic** with:
- Parchment-colored backgrounds (#f5e6d3)
- Brown leather tones (#8b4513)
- Serif fonts (Georgia, Garamond)
- Golden accents (#ffd700)
- Responsive grid layouts
- Book-themed icons and typography

All styling is in `base.html` and inherited by all templates.

---

## 🚀 Production Deployment (PythonAnywhere)

### 1. Upload to GitHub
```bash
git add .
git commit -m "NAHB Level 16 Complete"
git push origin main
```

### 2. Create PythonAnywhere Account
- Go to https://www.pythonanywhere.com
- Sign up (free tier available)

### 3. Deploy Flask API
1. Web tab → Add new web app → Manual configuration → Python 3.13
2. Edit WSGI file:
```python
import sys
path = '/home/yourusername/mysite/FlaskAPI'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```
3. Set environment variables in Web settings:
   - `API_KEY=nahb-secret-key-2026`

### 4. Deploy Django App
1. Web tab → Add new web app → Django → Python 3.13
2. Project path: `/home/yourusername/mysite/DjangoApp`
3. In console:
```bash
cd /home/yourusername/mysite/DjangoApp
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```
4. Set environment variables:
```
FLASK_API_URL=https://yourusername.pythonanywhere.com/api
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourusername.pythonanywhere.com
```
5. Reload web app

### 5. Access Your App
- **Flask API:** https://yourusername.pythonanywhere.com/api
- **Django App:** https://yourusername.pythonanywhere.com

---

## 🧪 Testing the API

### Using cURL

**Get published stories:**
```bash
curl http://localhost:5000/api/stories?status=published
```

**Create a story:**
```bash
curl -X POST http://localhost:5000/api/stories \
  -H "Content-Type: application/json" \
  -d '{"title":"My Story","description":"A great adventure","author_id":"testuser"}'
```

**Publish a story:**
```bash
curl -X PUT http://localhost:5000/api/stories/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"published"}'
```

**Get story start page:**
```bash
curl http://localhost:5000/api/stories/1/start
```

---

## 📋 Checklist for Level 16 Completion

### Authentication
- [x] User registration with role selection
- [x] User login/logout
- [x] Password hashing (Django built-in)
- [x] Session management

### Roles & Permissions
- [x] Reader role (play stories)
- [x] Author role (create stories)
- [x] Admin role (moderate content)
- [x] Story ownership enforcement
- [x] Protected author pages (@login_required)

### Data
- [x] Play.user linked to User model
- [x] UserProfile with role field
- [x] Story.author_id field

### Security
- [x] API structure for key protection
- [x] CSRF tokens on forms
- [x] SQL injection prevention (ORM usage)

### Moderation
- [x] Story suspension (status field)
- [x] Suspended stories hidden from readers
- [x] Can't play suspended stories
- [x] Admin can suspend via dropdown

---

## 🐛 Troubleshooting

### Flask Won't Start
```
Error: Module not found
→ Check virtual environment is activated
→ Run: pip install -r requirements.txt
```

### Django Migration Issues
```
Error: table "game_play" does not exist
→ Run: python manage.py migrate
```

### Static Files Not Loading
```
Error: CSS/images missing in production
→ Run: python manage.py collectstatic --noinput
→ Check STATIC_ROOT in settings.py
```

### API Connection Error
```
Error: Failed to connect to Flask API
→ Check Flask is running (http://localhost:5000/api/stories)
→ Verify FLASK_API_URL in Django .env
```

### Login Redirects Keep Happening
```
→ Check LOGIN_URL setting in settings.py
→ Ensure user.is_authenticated in templates
→ Clear browser cookies
```

---

## 📚 Key Technologies

- **Python 3.13** — Programming language
- **Flask 2.3** — Lightweight REST API framework
- **Django 4.2** — Full-featured web framework
- **SQLAlchemy 2.0** — ORM for Flask
- **SQLite** — Lightweight database
- **Gunicorn** — WSGI HTTP server (production)
- **Bootstrap/CSS3** — Styling

---

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Django Documentation](https://docs.djangoproject.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [REST API Design](https://restfulapi.net/)

---

## 📝 License

This project is created for educational purposes as a school assignment.

---

## 👥 Contributors

- **Student Name** — Full Stack Development
- **Project Start:** February 2026
- **Deadline:** February 14, 2026

---

## 🎮 Example Story

**Title:** The Lost Kingdom

**Story Flow:**
```
Page 1: You wake in a dark forest
├─ Choice A: "Go left" → Page 2
└─ Choice B: "Go right" → Page 3

Page 2: You find a castle
└─ Choice: "Enter the castle" → Page 4 (Ending: "Noble Ending")

Page 3: You meet a stranger
└─ Choice: "Trust them" → Page 5 (Ending: "Strange Alliance")
```

---

## 🔗 Quick Links

- Flask API: `http://localhost:5000/api`
- Django App: `http://localhost:8000`
- Admin Panel: `http://localhost:8000/admin`
- GitHub Repo: `https://github.com/yourusername/NAHB`

---

**Last Updated:** February 14, 2026  
**Status:** Level 16/20 Complete ✅