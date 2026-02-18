# 🧠 DocuMind AI Agent Design

## 🎯 Goal
Turn unstructured brain dumps (text/voice) into structured, professional JSON data ready for PDF generation.

## 🤖 Prompt Strategy

We will use a **System Prompt** that enforces a strict JSON output format and acts as a generic "Senior Technical Writer".

### The Prompt Template

```text
SYSTEM:
You are DocuMind, an expert technical writer and document structurer.
Your goal is to analyze the user's raw input and transform it into a structured JSON object.

RULES:
1. Identify the input type: "meeting_notes", "prd" (Product Requirements), or "code_docs".
2. Extract relevant sections based on the type.
3. Clean up the language to be professional and concise.
4. Output ONLY valid JSON. No markdown fencing, no commentary.

JSON SCHEMA STRUCTURE:
{
  "doc_type": "meeting_notes" | "prd" | "code_docs",
  "title": "Inferred Title",
  "content": {
     // Fields specific to the doc_type
  }
}

SPECIFIC FIELDS BY TYPE:
- Meeting Notes: summary, attendees (list), action_items (list of {owner, task, due_date}), key_decisions.
- PRD: overview, problem_statement, goals, user_stories (list), functional_requirements, non_functional_requirements.
- Code Docs: module_name, description, classes (list), functions (list with params/returns), usage_example.
```

---

## 🧪 Examples

### 1. Meeting Notes

**Input:**
> "Had a sync with the design team about the new dashboard. Sarah said the dark mode colors are too low contrast. Mike agreed to update the palette by Wednesday. We decided to delay the beta launch by 2 days to fix this. Also, john needs to review text copy."

**Output JSON:**
```json
{
  "doc_type": "meeting_notes",
  "title": "Design Team Sync - Dashboard",
  "content": {
    "summary": "Sync focused on dashboard visual issues, specifically dark mode contrast.",
    "attendees": ["Sarah", "Mike", "John", "Unknown Speaker"],
    "key_decisions": [
      "Delay beta launch by 2 days to fix contrast issues."
    ],
    "action_items": [
      {
        "owner": "Mike",
        "task": "Update dark mode color palette",
        "due_date": "Wednesday"
      },
      {
        "owner": "John",
        "task": "Review text copy",
        "due_date": null
      }
    ]
  }
}
```

### 2. Product Requirements Document (PRD)

**Input:**
> "We need a new feature for the app called 'Smart Search'. Users complain they can't find old docs. It should let them search by keyword and date. Needs to respond in under 200ms. We want to track search queries for analytics."

**Output JSON:**
```json
{
  "doc_type": "prd",
  "title": "PRD: Smart Search Feature",
  "content": {
    "overview": "Implementation of a robust search functionality to improve document retrieval.",
    "problem_statement": "Users currently struggle to locate historical documents, leading to frustration.",
    "goals": [
      "Enable keyword and date-based search.",
      "Track search analytics to understand user behavior."
    ],
    "functional_requirements": [
      "Search input field supporting text keywords.",
      "Date range filter.",
      "Results displayed in list view."
    ],
    "non_functional_requirements": [
      "Search latency must be under 200ms."
    ]
  }
}
```

### 3. Code Documentation

**Input:**
> "I wrote a python function called calculate_risk. It takes a user_profile dict and a credit_score int. Returns a float risk_factor. If credit score is under 500 it raises a ValueError."

**Output JSON:**
```json
{
  "doc_type": "code_docs",
  "title": "Function: calculate_risk",
  "content": {
    "module_name": "Risk Analysis",
    "description": "Calculates the risk factor for a given user based on their profile and credit score.",
    "functions": [
      {
        "name": "calculate_risk",
        "params": [
          {"name": "user_profile", "type": "dict", "desc": "User demographic data"},
          {"name": "credit_score", "type": "int", "desc": "Client's credit score"}
        ],
        "returns": {"type": "float", "desc": "Calculated risk factor"},
        "raises": ["ValueError if credit_score < 500"]
      }
    ],
    "usage_example": "risk = calculate_risk(user, 720)"
  }
}
```

## ⚖️ Note for Judges
This structure allows the frontend to be "dumb" - it just renders whatever the AI returns, making the system highly flexible. We can add new doc types just by updating the system prompt!
