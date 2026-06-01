# Goal-Tracking System — AI Prompt

Use the prompt below (copy everything inside the code block) to instruct an AI assistant to build a complete goal-tracking system on top of the existing Flask + SQLAlchemy + PostgreSQL stack found in this repository.

---

```
You are a senior full-stack engineer. I need you to extend my existing Flask + SQLAlchemy + PostgreSQL application with a complete goal-tracking system. The system must support five goal levels that cascade from top to bottom:

  Yearly → Quarterly → Monthly → Weekly → Daily

I already have a `daily_goals` table. Replace or extend it so that all five levels are consistent and properly related.

─────────────────────────────────────────
1. DATABASE MODELS  (backend/models.py)
─────────────────────────────────────────
Create one SQLAlchemy model per goal level. Every model must have:

  • id            – Integer primary key (auto-increment)
  • title         – String(255), not nullable
  • description   – Text, nullable
  • status        – String(20), default "not_started"
                    allowed values: "not_started", "in_progress", "completed", "abandoned"
  • progress      – Integer (0–100), default 0
  • created_at    – DateTime, default UTC now
  • updated_at    – DateTime, auto-updated on every save

Additional per-level fields:

  YearlyGoal
    • year         – Integer, not nullable (e.g. 2025)

  QuarterlyGoal
    • year         – Integer, not nullable
    • quarter      – Integer, not nullable (1–4)
    • yearly_goal_id – ForeignKey("yearly_goals.id"), nullable
                       (back-ref: yearly_goal.quarterly_goals)

  MonthlyGoal
    • year         – Integer, not nullable
    • month        – Integer, not nullable (1–12)
    • quarterly_goal_id – ForeignKey("quarterly_goals.id"), nullable
                          (back-ref: quarterly_goal.monthly_goals)

  WeeklyGoal
    • year         – Integer, not nullable
    • week_number  – Integer, not nullable (1–53, ISO week)
    • monthly_goal_id – ForeignKey("monthly_goals.id"), nullable
                        (back-ref: monthly_goal.weekly_goals)

  DailyGoal
    • date         – Date, not nullable (e.g. 2025-06-01)
    • weekly_goal_id – ForeignKey("weekly_goals.id"), nullable
                       (back-ref: weekly_goal.daily_goals)

Each model must implement:
  • insert()  – add to session and commit
  • update()  – commit current session
  • delete()  – remove from session and commit
  • format()  – return a plain dict of all columns (dates/datetimes as ISO strings)

─────────────────────────────────────────
2. API ENDPOINTS  (backend/flaskr/__init__.py)
─────────────────────────────────────────
Register a Blueprint named "goals" with the url_prefix "/goals".
Implement full CRUD for every level. Use the pattern /<level>s/ for
the collection and /<level>s/<int:id> for individual resources.

Levels and their URL segments:
  yearly      →  /goals/yearly
  quarterly   →  /goals/quarterly
  monthly     →  /goals/monthly
  weekly      →  /goals/weekly
  daily       →  /goals/daily

Required endpoints for EACH level:

  GET    /<level>s/
    • Optional query params: status, year (plus quarter/month/week_number/date
      where applicable) for filtering.
    • Returns { "success": true, "goals": [...], "total": <int> }

  GET    /<level>s/<int:id>
    • Returns { "success": true, "goal": {...} }
    • 404 if not found.

  POST   /<level>s/
    • Accepts JSON body matching the model fields.
    • Validates required fields; returns 400 on missing data.
    • Returns { "success": true, "created": <id>, "goal": {...} }

  PATCH  /<level>s/<int:id>
    • Accepts partial JSON body; only updates provided fields.
    • Returns { "success": true, "goal": {...} }

  DELETE /<level>s/<int:id>
    • Returns { "success": true, "deleted": <id> }

Additional aggregation endpoints:

  GET  /goals/yearly/<int:id>/tree
    • Returns the full nested tree for one yearly goal:
      yearly goal → quarterly goals → monthly goals → weekly goals → daily goals.
    • Shape: { "success": true, "goal": { ...yearly fields,
        "quarterly_goals": [ { ...quarterly fields,
          "monthly_goals": [ { ...monthly fields,
            "weekly_goals": [ { ...weekly fields,
              "daily_goals": [ {...} ] } ] } ] } ] } }

  GET  /goals/summary?year=<int>
    • Returns counts and average progress per level for the given year.
    • Shape: { "success": true, "year": <int>, "summary": {
        "yearly":    { "total": <int>, "avg_progress": <float> },
        "quarterly": { ... },
        "monthly":   { ... },
        "weekly":    { ... },
        "daily":     { ... } } }

─────────────────────────────────────────
3. ERROR HANDLING
─────────────────────────────────────────
Reuse the existing error-handler pattern already in the app:
  400  – bad request (missing required fields)
  404  – resource not found
  422  – unprocessable entity (DB errors)

─────────────────────────────────────────
4. TESTS  (backend/test_goals.py)
─────────────────────────────────────────
Write a unittest.TestCase class GoalTrackingTestCase using the same
setUp / tearDown pattern as test_flaskr.py (in-memory SQLite or a
dedicated test DB). Cover at minimum:

  • Create a goal at each level (success and missing-field failure).
  • Retrieve a list with filtering.
  • Retrieve a single goal (success and 404).
  • Update a goal's status and progress.
  • Delete a goal.
  • Retrieve the nested tree for a yearly goal.
  • Retrieve the year summary.

─────────────────────────────────────────
5. CONSTRAINTS & STYLE
─────────────────────────────────────────
• Follow the conventions already used in models.py and flaskr/__init__.py
  (SQLAlchemy declarative models, jsonify responses, abort() for errors).
• Do NOT modify existing Question or Category models or their endpoints.
• All new code must be importable without runtime errors when
  `flask run` is executed from the backend/ directory.
• Use Flask-SQLAlchemy relationships with lazy="dynamic" where the
  child collection could be large (weekly → daily).
• Validate that foreign-key parents exist before inserting a child.
• Keep the code clean: no commented-out blocks, no print debugging.

─────────────────────────────────────────
6. DELIVERABLES
─────────────────────────────────────────
Provide:
  1. Updated backend/models.py with all five new models appended.
  2. A new file backend/flaskr/goals.py containing the Blueprint and
     all route handlers.
  3. A one-line change in backend/flaskr/__init__.py to register the
     Blueprint: `from flaskr.goals import goals_bp; app.register_blueprint(goals_bp)`
  4. A new file backend/test_goals.py with the full test suite.
  5. A SQL migration snippet (plain ALTER TABLE / CREATE TABLE statements)
     that can be run against an existing PostgreSQL database to add the
     new tables without dropping the existing ones.
```
