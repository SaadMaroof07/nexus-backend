Nexus – Investor & Entrepreneur Collaboration Platform

Intern: Saad Maroof
Internship: DevelopersHub Corporation – Full Stack Development
Submission Date: 14 July 2026

A full-stack platform connecting Entrepreneurs and Investors, featuring authentication,
profile management, meeting scheduling, video calling, and document handling with
e-signatures.


Tech Stack

LayerTechnologyFrontendReact + TypeScript + Vite + Tailwind CSS Backend Django + Django REST FrameworkReal-time / Video SignalingDjango Channels (WebSockets) + Daphne (ASGI) Database PostgreSQL AuthenticationJWT (djangorestframework-simplejwt)Video CallingWebRTC (peer-to-peer)


Features Implemented

Week 1 – Authentication & Profiles ✅


Custom User model with role-based accounts (Entrepreneur / Investor)
JWT-based registration and login
Role-based dashboards
Full profile management (bio, startup info, investment history/preferences)
"Find Investors" — browse all registered investors with search & filters,
connected to live backend data


Week 2 – Meeting Scheduling ✅


Schedule, accept, and reject meetings between users
Conflict detection — prevents double-booking overlapping time slots for
either participant
Meeting status tracking (pending / accepted / rejected / cancelled)
Full frontend calendar/list view connected to backend APIs


Week 2 – Video Calling ✅


WebSocket signaling server built with Django Channels
Room-based call pages (join via room ID/link)
Camera & microphone access, audio/video toggle, end call
Full peer-to-peer WebRTC handshake (offer/answer/ICE exchange over
WebSocket), verified working in both directions between two browsers
Debugged and fixed a React StrictMode double-mount issue that was
creating duplicate peer connections in development mode


Week 2 – Document Processing Chamber ✅


Document upload with metadata (uploader, version, status: draft/final/signed)
File storage and in-browser preview/download
E-signature — attach a signature image to a document, which updates its
status to "signed" and records who signed it
Delete functionality (owner-restricted)


Week 3 – Payment & Advanced Security ❌ Not Implemented

Per internship coordinator's updated timeline (deadline moved from 21 July to
14 July, with Week 3 marked optional), this module was deprioritized in favor
of fully completing and polishing Weeks 1–2.

Security fundamentals from Week 1–2 are still in place:


Passwords hashed via Django's built-in hasher (never stored in plain text)
JWT access/refresh token authentication
Object-level permissions (e.g., only a document's owner can delete it, only
a meeting's invited participant can accept/reject it)
CORS restricted to the frontend origin



Project Structure

Nexus Platform/
├── backend/
│   ├── nexus_backend/      # Django project settings, URLs, ASGI config
│   ├── users/              # Custom User model, auth, profile APIs
│   ├── meetings/           # Meeting scheduling APIs
│   ├── documents/          # Document upload & e-signature APIs
│   ├── calls/              # WebSocket signaling for video calls
│   └── manage.py
└── Nexus/                  # React frontend (forked base repo)
    └── src/
        ├── pages/           # Auth, dashboard, investors, meetings, documents, call
        ├── context/         # AuthContext (JWT session state)
        ├── services/        # API client (axios) + backend-to-frontend data mapping
        └── components/      # Shared UI components


Setup Instructions

Backend

bashcd backend
python -m venv venv
venv\Scripts\activate            # Windows
pip install -r requirements.txt  # or install packages listed below manually

# Configure .env with your PostgreSQL credentials:
# DB_NAME=nexus_db
# DB_USER=postgres
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432

python manage.py migrate
python manage.py createsuperuser
daphne -p 8000 nexus_backend.asgi:application

Key packages: django, djangorestframework, djangorestframework-simplejwt,
django-cors-headers, psycopg2-binary, python-decouple, Pillow,
channels, daphne

Frontend

bashcd Nexus
npm install
npm run dev

App runs at http://localhost:5173, backend API at http://127.0.0.1:8000/api/.


Endpoints
 

/api/users/register/POSTCreate a new account
/api/token/POSTLogin (returns JWT access/refresh tokens)
/api/users/me/GET/PATCHView or update own profile
/api/users/GETBrowse all users
/api/meetings/GET/POSTList or schedule meetings
/api/meetings/{id}/accept/PATCHAccept a meeting
/api/meetings/{id}/reject/PATCHReject a meeting
/api/documents/GET/POSTList or upload documents
/api/documents/{id}/sign/PATCHAttach e-signature to a document
ws://.../ws/call/{room_id}/WebSocketVideo call signaling

