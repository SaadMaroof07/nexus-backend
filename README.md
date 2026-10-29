Nexus – Investor & Entrepreneur Collaboration Platform

A full-stack platform connecting Entrepreneurs and Investors, featuring authentication,
profile management, meeting scheduling, video calling, and document handling with
e-signatures.


Tech Stack

LayerTechnologyFrontendReact + TypeScript + Vite + Tailwind CSS Backend Django + Django REST FrameworkReal-time / Video SignalingDjango Channels (WebSockets) + Daphne (ASGI) Database PostgreSQL AuthenticationJWT (djangorestframework-simplejwt)Video CallingWebRTC (peer-to-peer)


Features Implemented

 Authentication & Profiles 


Custom User model with role-based accounts (Entrepreneur / Investor)
JWT-based registration and login
Role-based dashboards
Full profile management (bio, startup info, investment history/preferences)
"Find Investors" — browse all registered investors with search & filters,
connected to live backend data


 Meeting Scheduling 


Schedule, accept, and reject meetings between users
Conflict detection — prevents double-booking overlapping time slots for
either participant
Meeting status tracking (pending / accepted / rejected / cancelled)
Full frontend calendar/list view connected to backend APIs


 Video Calling 


WebSocket signaling server built with Django Channels
Room-based call pages (join via room ID/link)
Camera & microphone access, audio/video toggle, end call
Full peer-to-peer WebRTC handshake (offer/answer/ICE exchange over
WebSocket), verified working in both directions between two browsers
Debugged and fixed a React StrictMode double-mount issue that was
creating duplicate peer connections in development mode


 Document Processing Chamber 


Document upload with metadata (uploader, version, status: draft/final/signed)
File storage and in-browser preview/download
E-signature — attach a signature image to a document, which updates its
status to "signed" and records who signed it
Delete functionality (owner-restricted)


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

