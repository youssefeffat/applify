# Applify Frontend-to-Backend API Analysis

Based on a deep dive into the current Vue 3 frontend state (`useAppStore.js`, routing logic, and simulated AI functionality), here is the comprehensive analysis of all REST API endpoints and data schemas required to connect the frontend to a real backend.

---

## 1. Authentication & Identity

The application requires a robust authentication system (e.g., JWT) to manage user sessions, specifically separating the Login and "Create Account" flows.

### Endpoints
- **`POST /api/auth/register`**
  - **Payload**: `{ email, password }`
  - **Response**: `{ token, user }`
- **`POST /api/auth/login`**
  - **Payload**: `{ email, password }`
  - **Response**: `{ token, user }`
- **`GET /api/users/me`**
  - **Headers**: `Authorization: Bearer <token>`
  - **Response**: The full `UserSchema`

---

## 2. User Profile & Onboarding

The `OnboardingView` and `ProfileView` both mutate the user's professional profile. The backend must support updating a complex, nested user schema.

### Endpoints
- **`PUT /api/users/me`**
  - **Description**: Updates the user's profile data. Called when completing Onboarding or saving the Profile Dashboard.
  - **Payload**: Partial `UserSchema` updates.

### `UserSchema`
```json
{
  "id": "uuid",
  "email": "string",
  "firstName": "string",
  "lastName": "string",
  "currentTitle": "string",
  "github": "string",
  "location": "string",
  
  // Job Preferences
  "targetRoles": ["string"],
  "employmentTypes": ["string"], // e.g., ["Full-Time", "Remote"]
  "experienceLevels": ["string"], // e.g., ["Entry", "Mid"]
  "targetYearsExperience": "string", // e.g., "3-5"
  
  // Professional Background (Long text fields)
  "education": "string",
  "experience": "string",
  "skills": "string",
  "softSkills": "string",
  "certificates": "string",
  "languages": "string",
  "longResume": "string"
}
```

---

## 3. Job Exploration

The `JobExplorerView` relies on fetching, filtering, and scoring jobs. The backend must handle text searching and metadata filtering.

### Endpoints
- **`GET /api/jobs`**
  - **Query Params**: `?search={query}&mode={remote|hybrid|on-site}&contract={full-time|contract}`
  - **Response**: Array of `JobSchema`. Note: The API should dynamically calculate the `compatibilityScore` based on the requested user's profile.
- **`GET /api/jobs/{jobId}`**
  - **Response**: Detailed `JobSchema`

### `JobSchema`
```json
{
  "id": "uuid",
  "title": "string",
  "company": "string",
  "location": "string",
  "type": "string", // remote, on-site, hybrid
  "contractType": "string", // full-time, part-time, contract
  "tags": ["string"],
  "description": "string",
  "compatibilityScore": "integer" // 0-100, calculated server-side
}
```

---

## 4. Application Tracker (Kanban)

The `ApplicationTrackerView` and `DashboardView` rely on a junction table representing the relationship between a User and a Job.

### Endpoints
- **`GET /api/applications`**
  - **Response**: Array of `ApplicationSchema`
- **`POST /api/applications`**
  - **Description**: Triggered when clicking "Save Job" or "Apply" directly.
  - **Payload**: `{ jobId: "uuid", status: "Saved" | "Applied" }`
- **`PATCH /api/applications/{applicationId}`**
  - **Description**: Triggered when dragging/moving cards in the Kanban board or setting an interview date.
  - **Payload**: `{ status: "Interviews", interviewDate: "2026-10-12T14:00:00Z" }`

### `ApplicationSchema`
```json
{
  "id": "uuid",
  "userId": "uuid",
  "jobId": "uuid",
  "jobDetails": { /* subset of JobSchema for quick rendering */ },
  "status": "string", // Enum: Saved, Applied, Interviews, Accepted, Rejected
  "interviewDate": "datetime | null",
  "dateAdded": "datetime",
  "lastUpdated": "datetime"
}
```

---

## 5. AI Service Integrations

Currently, the frontend simulates several complex AI workflows using `setTimeout`. To make these real, the backend must expose wrapper APIs that communicate with an LLM (like GPT-4 or Gemini) and specialized parsers.

### Endpoints
- **`POST /api/ai/parse-cv`**
  - **Description**: Accepts a PDF/Word document upload and returns extracted text mapped to the `UserSchema`.
  - **Payload**: `multipart/form-data` (file)
  - **Response**: `{ education, experience, skills, softSkills, certificates, languages }`

- **`POST /api/ai/council-chat`**
  - **Description**: Conversational endpoint for the profound questions on Step 2.
  - **Payload**: `{ currentField: "challenge", userMessage: "I migrated a legacy app..." }`
  - **Response**: `{ nextQuestion: "...", extractedData: { skills: "..." } }`

- **`POST /api/ai/suggest-roles`**
  - **Description**: Analyzes the user's free-text input on Step 3 and suggests roles.
  - **Payload**: `{ description: "I love designing UIs and managing teams" }`
  - **Response**: `{ suggestedRoles: ["UX Designer", "Product Manager"] }`

- **`POST /api/ai/generate-custom-cv`**
  - **Description**: Generates a tailored CV for a specific job application.
  - **Payload**: `{ jobId: "uuid" }`
  - **Response**: `{ cvContent: "string (markdown or pdf link)" }`
