import pandas as pd
from ai_engine import analyze_answer
from questions import QUESTIONS


# Columns required in the CSV
REQUIRED_COLUMNS = [
    "student_id",
    "question",
    "answer"
]


# --------------------------------------------------
# FIND QUESTION ID FROM QUESTION TEXT
# --------------------------------------------------

def find_question_id(question_text):

    question_text = str(question_text).strip()

    for question_id, data in QUESTIONS.items():

        if data["question"].strip() == question_text:
            return question_id

    return None


# --------------------------------------------------
# LOAD CSV
# --------------------------------------------------

def load_assessment(file):

    df = pd.read_csv(file)

    for column in REQUIRED_COLUMNS:

        if column not in df.columns:

            raise ValueError(
                f"CSV is missing required column: {column}"
            )

    return df


# --------------------------------------------------
# CLEAN DATA
# --------------------------------------------------

def clean_assessment(df):

    df = df.copy()

    df = df.dropna(
        subset=[
            "student_id",
            "question",
            "answer"
        ]
    )

    df["student_id"] = (
        df["student_id"]
        .astype(str)
        .str.strip()
    )

    df["question"] = (
        df["question"]
        .astype(str)
        .str.strip()
    )

    df["answer"] = (
        df["answer"]
        .astype(str)
        .str.strip()
    )

    df = df[
        df["answer"].str.len() > 0
    ]

    return df


# --------------------------------------------------
# ANALYZE CLASS
# --------------------------------------------------

def analyze_class(
    df,
    progress_callback=None
):

    results = []

    total = len(df)

    if total == 0:
        return results

    for index, row in df.iterrows():

        student_id = row["student_id"]

        question = row["question"]

        answer = row["answer"]

        # Find the matching internal question ID
        question_id = find_question_id(question)

        print(
            f"Analyzing {student_id}"
        )

        print(
            f"Question: {question}"
        )

        # If the question is not in our question bank
        if question_id is None:

            error_message = (
                "Question not found in questions.py. "
                "Make sure the question text in the CSV "
                "exactly matches the question in questions.py."
            )

            print(
                "AI ERROR:",
                error_message
            )

            results.append({

                "student_id": student_id,

                "question": question,

                "answer": answer,

                "diagnosis": {

                    "concepts_understood": [],

                    "concepts_partial": [],

                    "concepts_misunderstood": [],

                    "misconception": "QUESTION_NOT_FOUND",

                    "evidence": error_message,

                    "confidence": 0,

                    "explanation": error_message,

                    "recommended_action": (
                        "Check the question text."
                    )
                },

                "error": error_message

            })

        else:

            try:

                # Send answer to AI
                diagnosis = analyze_answer(
                    question_id=question_id,
                    student_answer=answer
                )

                print(
                    "AI RESULT:",
                    diagnosis
                )

                results.append({

                    "student_id": student_id,

                    "question": question,

                    "answer": answer,

                    "diagnosis": diagnosis,

                    "error": None

                })

            except Exception as e:

                print(
                    "AI ERROR:",
                    str(e)
                )

                results.append({

                    "student_id": student_id,

                    "question": question,

                    "answer": answer,

                    "diagnosis": {

                        "concepts_understood": [],

                        "concepts_partial": [],

                        "concepts_misunderstood": [],

                        "misconception": "AI_ERROR",

                        "evidence": str(e),

                        "confidence": 0,

                        "explanation": (
                            "AI analysis failed. "
                            "Check the terminal."
                        ),

                        "recommended_action": (
                            "Check the AI connection."
                        )

                    },

                    "error": str(e)

                })

        if progress_callback:

            progress_callback(
                (index + 1) / total
            )

    return results


# --------------------------------------------------
# MISCONCEPTION SUMMARY
# --------------------------------------------------

def create_misconception_summary(results):

    counts = {}

    for result in results:

        diagnosis = result["diagnosis"]

        misconception = diagnosis.get(
            "misconception",
            "NONE"
        )

        if misconception in [
            "NONE",
            "AI_ERROR",
            "QUESTION_NOT_FOUND"
        ]:
            continue

        if misconception not in counts:

            counts[misconception] = {
                "students": set()
            }

        counts[
            misconception
        ]["students"].add(
            result["student_id"]
        )

    total_students = len(
        set(
            result["student_id"]
            for result in results
        )
    )

    summary = []

    for misconception, data in counts.items():

        student_count = len(
            data["students"]
        )

        percentage = 0

        if total_students > 0:

            percentage = (
                student_count
                / total_students
            ) * 100

        summary.append({

            "misconception":
                misconception,

            "students":
                student_count,

            "percentage":
                round(
                    percentage,
                    1
                )

        })

    summary.sort(
        key=lambda x: x["students"],
        reverse=True
    )

    return summary


# --------------------------------------------------
# CATEGORIZE STUDENTS
# --------------------------------------------------

def categorize_students(results):

    student_status = {}

    for result in results:

        student_id = result[
            "student_id"
        ]

        diagnosis = result[
            "diagnosis"
        ]

        misconception = diagnosis.get(
            "misconception",
            "NONE"
        )

        confidence = diagnosis.get(
            "confidence",
            0
        )

        if student_id not in student_status:

            student_status[student_id] = {

                "intervention": False,

                "low_confidence": False

            }

        if (
            misconception != "NONE"
            and misconception != "AI_ERROR"
            and misconception != "QUESTION_NOT_FOUND"
        ):

            student_status[
                student_id
            ]["intervention"] = True

        if confidence < 0.75:

            student_status[
                student_id
            ]["low_confidence"] = True

    groups = {

        "needs_intervention": [],

        "needs_practice": [],

        "mastered": []

    }

    for student_id, status in student_status.items():

        if status["intervention"]:

            groups[
                "needs_intervention"
            ].append(student_id)

        elif status["low_confidence"]:

            groups[
                "needs_practice"
            ].append(student_id)

        else:

            groups[
                "mastered"
            ].append(student_id)

    return groups