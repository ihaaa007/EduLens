# 🧠 EduLens

### AI-Powered Classroom Misconception Radar

EduLens is an AI-powered educational analytics tool that helps teachers understand **what students actually understand**, rather than relying only on marks.

Instead of simply identifying whether an answer is correct or wrong, EduLens analyzes student responses to detect **learning misconceptions**, groups students based on their learning needs, and recommends targeted interventions.

---

## 🎯 Problem

Traditional assessment systems mainly focus on marks and scores.

A student may get an answer wrong, but a teacher still has to figure out:

- What concept did the student misunderstand?
- Is the same misconception affecting multiple students?
- Which students need intervention?
- What should the teacher teach again?

EduLens aims to answer these questions automatically.

---

## 💡 Solution

EduLens analyzes student answers and provides:

- 🔍 Misconception detection
- 🧠 Concept-level understanding
- 👥 Student learning groups
- 📊 Classroom misconception analytics
- 🎯 Personalized teacher interventions
- 📚 Recommended activities and questions

---

## 🚀 Features

### 📂 Assessment Upload
Teachers can upload student responses using a CSV file.

### 🧠 Misconception Detection
EduLens identifies common conceptual misunderstandings instead of only checking right/wrong answers.

### 📊 Classroom Misconception Radar
Teachers can see which misconceptions are most common across the classroom.

### 👥 Learning Groups
Students are categorized into:

- 🔴 Needs Intervention
- 🟡 Needs Practice
- 🟢 Mastered

### 🎯 Teacher Intervention
The system recommends activities and questions to address specific misconceptions.

### 👨‍🎓 Student-Level Insights
Teachers can inspect individual student answers, detected misconceptions, confidence, and explanations.

---

## 🏗️ Architecture

```text
Student Answers (CSV)
        ↓
   Data Cleaning
        ↓
   Diagnostic Engine
        ↓
Misconception Detection
        ↓
Classroom Analysis
        ↓
Teacher Dashboard
        ↓
Recommended Intervention
