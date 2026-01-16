# 🌍 LUP - Local Up Platform

A comprehensive Django-based platform for community engagement, service reviews, and local resource management.

## 📋 Project Overview

**LUP** is a full-featured platform that enables communities to:
- 🏪 Discover and review local services and businesses
- 💬 Engage in community forums and discussions
- 📍 Report issues and request services at the local level
- 👥 Build user profiles and connect with neighbors
- 🔍 Search and filter local resources

## 🏗️ Architecture

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Web Framework** | Django | 4.2.20 |
| **Database** | PostgreSQL + PostGIS | 15 |
| **Search Engine** | Elasticsearch | 7.17.9 |
| **Cache/Queue** | Redis | 7+ |
| **Task Queue** | Celery | 5.3.4 |
| **WSGI Server** | Gunicorn | 21.2.0 |
| **Containerization** | Docker | 20+ |
| **Frontend** | Bootstrap 3 | 3.4 |

### Core Apps

```
src/lup/
├── core/           # User profiles, notifications, activity logs
├── forum/          # Discussion forums and community threads
├── profiles/       # Local entities and service providers
├── reporting/      # Issue reporting and tracking
├── review/         # Reviews and ratings system
├── notifications/  # Real-time notifications
└── search/         # Full-text search via Haystack
```

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone repository
git clone <repo-url>
cd lup

# 2. Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r src/lup/requirements.txt

# 4. Configure database
cp .env.example .env
# Edit .env with your database credentials

# 5. Run migrations
cd src/lup
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Build search index
python manage.py rebuild_index --noinput

# 8. Start development server
python manage.py runserver
```

Visit: http://localhost:8000

### Docker Deployment

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with production settings

# 2. Build and run
docker-compose up --build

# 3. Create superuser
docker-compose exec web python manage.py createsuperuser

# 4. Access
# Web: http://localhost:8000
# Admin: http://localhost:8000/admin
```

## 📦 Installation & Configuration

### Prerequisites
- Python 3.9+
- PostgreSQL 13+ with PostGIS extension
- Redis 6+
- Elasticsearch 7.17
- Node.js (optional, for frontend asset building)

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Critical
DEBUG=False
SECRET_KEY=your-very-secure-random-string
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=lup_db
DB_USER=lup_user
DB_PASSWORD=strong_password_here
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Elasticsearch
ELASTICSEARCH_URL=http://localhost:9200/
SKIP_ELASTICSEARCH_SIGNALS=False

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=app-password-here

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 🎯 Key Features

### User Management
- ✅ User registration and authentication
- ✅ Profile customization
- ✅ Activity logging
- ✅ Email verification

### Forum System
- ✅ Create topics and discussions
- ✅ Comments and replies
- ✅ Category-based organization
- ✅ Sticky and announcement posts

### Reporting System
- ✅ Report local issues
- ✅ Track resolution status
- ✅ Assign to authorities
- ✅ Community voting

### Review System
- ✅ Rate services (1-5 stars)
- ✅ Written reviews with photos
- ✅ Verified reviewer badges
- ✅ Helpful/unhelpful votes

### Search Capabilities
- ✅ Full-text search via Elasticsearch
- ✅ Real-time indexing
- ✅ Advanced filtering
- ✅ Search suggestions

### Notifications
- ✅ Real-time notifications
- ✅ Email digests
- ✅ Notification preferences
- ✅ Mention system (@username)

## 🔧 Management Commands

```bash
cd src/lup

# Database
python manage.py migrate                 # Run migrations
python manage.py makemigrations          # Create migrations
python manage.py dbshell                 # Open database shell

# Search
python manage.py rebuild_index --noinput # Rebuild Elasticsearch index
python manage.py clear_index             # Clear all search indices

# Users
python manage.py createsuperuser         # Create admin user
python manage.py changepassword username # Change user password

# Maintenance
python manage.py collectstatic           # Collect static files
python manage.py clearsessions           # Clear expired sessions
python manage.py shell                   # Python shell with Django context

# Development
python manage.py runserver 0.0.0.0:8000  # Start dev server
python manage.py test                    # Run tests
python manage.py check --deploy          # Check production readiness
```

## 📊 Admin Interface

Access at: `/admin`

Default superuser created during setup.

**Registered Models:**
- Users & Profiles
- Forum (Categories, Topics, Posts, Comments)
- Reporting (Reports, Status, Assignments)
- Reviews (Reviews, Ratings, Comments)
- Notifications (Notifications, Activity Logs)
- Profiles (Entities, Municipalities, Entity Types)

## 🔐 Security Features

- ✅ CSRF protection
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection
- ✅ Secure password hashing (PBKDF2)
- ✅ Rate limiting
- ✅ SSL/TLS support
- ✅ CORS configuration
- ✅ Content Security Policy headers
- ✅ Session security
- ✅ Database access control

## 📈 Performance Optimization

### Caching Strategy
- Django-Redis for session and query caching
- Cache key: `django:cache:<key>`
- TTL: Configurable per view

### Database Optimization
- Strategic indexes on frequently queried fields
- Connection pooling (CONN_MAX_AGE=600)
- Query optimization with select_related/prefetch_related

### Search Performance
- Elasticsearch for real-time search
- Batch indexing for large datasets
- Search result pagination (20 per page)

### Task Queuing
- Celery with Redis broker
- Async email sending
- Periodic notification digests
- Background data processing

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific app tests
pytest core.tests

# With coverage
pytest --cov=. --cov-report=html

# Specific test class
pytest core.tests.test_models::UserProfileTest
```

## 📝 API Documentation

### Available Endpoints

**Forum:**
- `GET /forum/` - List forums
- `GET /forum/topics/` - List topics
- `POST /forum/topics/` - Create topic
- `GET /forum/topics/<id>/` - Get topic detail

**Reporting:**
- `GET /reporting/` - List reports
- `POST /reporting/` - Create report
- `GET /reporting/<id>/` - Get report detail

**Reviews:**
- `GET /review/` - List reviews
- `POST /review/` - Create review
- `GET /review/<id>/` - Get review detail

**Search:**
- `GET /search/?q=<query>` - Search platform
- `GET /search/suggestions/?q=<query>` - Get suggestions

## 🚨 Troubleshooting

### Database Connection
```bash
# Check connection
python manage.py dbshell

# Migrate issues
python manage.py migrate --fake-initial
```

### Static Files
```bash
# Rebuild static files
python manage.py collectstatic --noinput --clear

# Check static directory
ls -la src/lup/staticfiles/
```

### Celery Tasks
```bash
# Check Celery status
celery -A lup inspect active

# Clear task queue
celery -A lup purge
```

### Elasticsearch Issues
```bash
# Check cluster health
curl http://localhost:9200/_cluster/health

# Rebuild index
python manage.py rebuild_index --noinput
```

## 📚 Documentation

- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Production deployment guide
- **[Django Documentation](https://docs.djangoproject.com/)** - Framework docs
- **[PostGIS Documentation](https://postgis.net/documentation/)** - Spatial database
- **[Elasticsearch Guide](https://www.elastic.co/guide/)** - Search engine

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Open Pull Request

## 📋 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Team & Support

- **Project Lead**: Thato Chikane
- **Documentation**: Full API docs available in `/docs`
- **Issues**: Report bugs via GitHub Issues
- **Security**: Report security issues privately

## 🎉 Project Status

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: 2024

### Launch Checklist
- ✅ Core functionality implemented
- ✅ Database schema optimized
- ✅ Search functionality working
- ✅ Security hardened
- ✅ Docker containerization
- ✅ Health check endpoint
- ✅ Logging and monitoring
- ✅ Documentation complete

---

**Ready to deploy! Follow [DEPLOYMENT.md](./DEPLOYMENT.md) for production setup.**
