# Microservices Architecture Analysis for Applify

Based on the API specifications in `apis_doc.md`, the backend should be structured into several distinct microservices, each handling a specific domain of the application. Here is the recommended microservice breakdown:

## 1. Authentication Service (Auth Service)
**Domain:** Identity, Session Management, and Security.
**Responsibilities:**
- User registration and login.
- Password hashing and verification.
- Generating and validating JWT tokens (or other session mechanisms).
- Securing the initial entry points to the application.
**Relevant Endpoints:**
- `POST /api/auth/register`
- `POST /api/auth/login`

## 2. User Profile Service (User Service)
**Domain:** User Data, Professional Background, and Preferences.
**Responsibilities:**
- Managing the complex `UserSchema`, including personal details, job preferences, and professional background.
- Handling the onboarding process data mutations.
- Serving user profile data to the frontend.
**Relevant Endpoints:**
- `GET /api/users/me`
- `PUT /api/users/me`

## 3. Job Catalog Service (Job Service)
**Domain:** Job Postings, Search, and Filtering.
**Responsibilities:**
- Storing and retrieving job metadata (`JobSchema`).
- Handling complex search queries, filtering (remote/hybrid, full-time/contract), and text searches.
- Calculating the `compatibilityScore` (potentially requiring asynchronous communication with the User Service to fetch the user's profile for comparison).
**Relevant Endpoints:**
- `GET /api/jobs`
- `GET /api/jobs/{jobId}`

## 4. Application Tracker Service (Tracker Service)
**Domain:** Job Applications, Kanban Board State, and Interview Tracking.
**Responsibilities:**
- Managing the junction between Users and Jobs (`ApplicationSchema`).
- Tracking the status of applications (Saved, Applied, Interviews, Accepted, Rejected).
- Managing interview dates and status transitions for the Kanban board.
**Relevant Endpoints:**
- `GET /api/applications`
- `POST /api/applications`
- `PATCH /api/applications/{applicationId}`

## 5. AI Integration Service (AI Service)
**Domain:** LLM Communication, Document Parsing, and Intelligent Suggestions.
**Responsibilities:**
- Wrapper for external AI providers (e.g., OpenAI, Gemini).
- Parsing resumes (PDF/Word) into structured JSON.
- Handling conversational workflows (Council Chat).
- Generating tailored CVs and suggesting target roles based on unstructured text.
**Relevant Endpoints:**
- `POST /api/ai/parse-cv`
- `POST /api/ai/council-chat`
- `POST /api/ai/suggest-roles`
- `POST /api/ai/generate-custom-cv`

## 6. API Gateway (Infrastructure Component)
While not a domain service itself, a microservices architecture will require an API Gateway to expose these disparate services under a single, cohesive `/api/` prefix to the frontend.
**Responsibilities:**
- Routing frontend requests to the appropriate internal microservice.
- Centralized authentication/authorization checks.
- Rate limiting and cross-origin resource sharing (CORS) handling.

> [!TIP]
> The **Job Service** calculating the `compatibilityScore` dynamically will require fetching the user's profile. You might need to implement inter-service communication (e.g., gRPC, REST, or an event bus) between the Job Service and the User Service to accomplish this efficiently.
