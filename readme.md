# CLI Command Reference

A concise catalog of every Flask CLI command exposed by this app, grouped by area, with arguments, roles, and behavior.

---

## Roles & Authentication

- Some commands are role‑protected via `require_role("student")` or `require_role("staff")`.
- Run `flask user login` before any protected command.
- Roles:
  - **student**: can request hours and view accolades.
  - **staff**: can log hours directly, list requests, and approve/reject requests.

---

## App‑Level Commands

### `flask init`
- **Args:** none  
- **Role:** anyone  
- **Does:** Creates and initializes the database (runs `initialize()`).

### `flask leaderboard`
- **Args:** none  
- **Role:** anyone  
- **Does:** Prints a ranked list of students by total hours (descending; tie‑break by username).

---

## User Group Commands (`flask user …`)

### `flask user create <user_type> <username> <password>`
- **Role:** anyone  
- **Does:** Creates a user.  
- **Notes:** `user_type` must be `student` or `staff`.

### `flask user list [string|json]`
- **Role:** anyone  
- **Does:** Lists all users.  
- **Notes:** Output format defaults to `string`; `json` prints JSON.

### `flask user logs [string|json]`
- **Role:** anyone  
- **Does:** Lists all hour logs.  
- **Notes:** Output format defaults to `string`; `json` prints JSON.

### `flask user login <username> <password>`
- **Role:** anyone  
- **Does:** Logs in the user for role‑protected commands.

### `flask user logout`
- **Role:** anyone  
- **Does:** Logs out the current user.

### `flask user log <student_username> <hours> <activity_name>`
- **Role:** staff  
- **Does:** Adds a log entry for the student and increments the student’s total hours.  
- **Notes:** Fails if the activity name does not exist.

### `flask user request <hours> <activity_name>`
- **Role:** student  
- **Does:** Creates a request for staff approval to add hours for a specific activity.  
- **Notes:** Fails if the activity name does not exist.

### `flask user requests`
- **Role:** staff  
- **Does:** Shows all pending hour requests.  
- **Columns:** Request ID, Student Name, Activity, Requested Hours.

### `flask user confirm <approve|reject> <request_id>`
- **Role:** staff  
- **Does:** Approves or rejects a pending request.  
- **Approve:** Creates a log, adds hours to the student, removes the request.  
- **Reject:** Removes the request without adding hours.

### `flask user accolades`
- **Role:** student  
- **Does:** Displays per‑activity milestone status for the current user using `resolve_milestone` and `milestones_for`.  
- **Output:** One line per activity indicating current milestone and progress toward the next.

---
