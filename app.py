import streamlit as st
import pandas as pd
import plotly.express as px

from analyzer import (
    load_assessment,
    clean_assessment,
    analyze_class,
    create_misconception_summary,
    categorize_students
)

from intervention import get_intervention


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="EduLens",
    page_icon="🧠",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🧠 EduLens")

st.subheader(
    "AI Classroom Misconception Radar"
)

st.write(
    "See beyond marks. Discover what your classroom actually understands."
)

st.divider()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("EduLens")

st.sidebar.write(
    "Teacher Dashboard"
)

st.sidebar.info(
    "Upload student answers and let AI identify "
    "recurring learning misconceptions."
)


# --------------------------------------------------
# UPLOAD
# --------------------------------------------------

st.header("📂 Upload Assessment")

uploaded_file = st.file_uploader(
    "Upload a CSV file containing student answers",
    type=["csv"]
)


# --------------------------------------------------
# CSV FORMAT HELP
# --------------------------------------------------

with st.expander(
    "What should my CSV look like?"
):

    st.code(
        """student_id,question,answer
S01,"Explain the difference between flow control and congestion control in TCP.","Flow control protects the receiver."
S02,"Explain the difference between flow control and congestion control in TCP.","Flow control prevents congestion in the network."
""",
        language="csv"
    )


# --------------------------------------------------
# PROCESS UPLOAD
# --------------------------------------------------

if uploaded_file is not None:

    try:

        df = load_assessment(
            uploaded_file
        )

        df = clean_assessment(df)

        st.success(
            f"Loaded {len(df)} student responses."
        )

        with st.expander(
            "Preview assessment data"
        ):

            st.dataframe(
                df,
                use_container_width=True
            )

        st.divider()

        analyze_button = st.button(
            "🚀 Analyze Assessment",
            type="primary"
        )

        if analyze_button:

            progress_bar = st.progress(0)

            status_text = st.empty()

            def update_progress(value):

                progress_bar.progress(
                    value
                )

                status_text.write(
                    f"Analyzing... "
                    f"{int(value * 100)}%"
                )

            results = analyze_class(
                df,
                progress_callback=update_progress
            )

            progress_bar.progress(1.0)

            status_text.success(
                "Analysis complete! 🎉"
            )

            st.session_state[
                "results"
            ] = results

    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

if "results" in st.session_state:

    results = st.session_state[
        "results"
    ]


    # --------------------------------------------------
    # SHOW ERRORS
    # --------------------------------------------------

    errors = [
        result
        for result in results
        if result.get("error")
    ]

    if errors:

        st.error(
            "⚠️ Some responses could not be analyzed."
        )

        for result in errors:

            st.write(
                f"**{result['student_id']}**"
            )

            st.write(
                result["error"]
            )


    # --------------------------------------------------
    # CLASSROOM OVERVIEW
    # --------------------------------------------------

    st.divider()

    st.header(
        "📊 Classroom Overview"
    )

    total_students = len(
        set(
            result["student_id"]
            for result in results
        )
    )

    total_answers = len(
        results
    )

    misconception_summary = (
        create_misconception_summary(
            results
        )
    )

    groups = categorize_students(
        results
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Students Analysed",
            total_students
        )


    with col2:

        st.metric(
            "Answers Analysed",
            total_answers
        )


    with col3:

        st.metric(
            "Misconceptions Found",
            len(
                misconception_summary
            )
        )


    with col4:

        st.metric(
            "Students Needing Support",
            len(
                groups[
                    "needs_intervention"
                ]
            )
        )


    # --------------------------------------------------
    # LEARNING GROUPS
    # --------------------------------------------------

    st.divider()

    st.header(
        "👥 Learning Groups"
    )

    col1, col2, col3 = st.columns(3)


    with col1:

        st.error(
            f"🔴 Intervention\n\n"
            f"{len(groups['needs_intervention'])} students"
        )


    with col2:

        st.warning(
            f"🟡 Practice\n\n"
            f"{len(groups['needs_practice'])} students"
        )


    with col3:

        st.success(
            f"🟢 Mastered\n\n"
            f"{len(groups['mastered'])} students"
        )


    # --------------------------------------------------
    # MISCONCEPTION RADAR
    # --------------------------------------------------

    st.divider()

    st.header(
        "🚨 Misconception Radar"
    )


    if len(
        misconception_summary
    ) == 0:

        st.success(
            "No significant misconceptions detected."
        )

    else:

        misconception_df = pd.DataFrame(
            misconception_summary
        )

        misconception_df = (
            misconception_df.rename(
                columns={
                    "misconception":
                        "Misconception",

                    "students":
                        "Students",

                    "percentage":
                        "Percentage"
                }
            )
        )

        st.dataframe(
            misconception_df,
            use_container_width=True,
            hide_index=True
        )


        fig = px.bar(
            misconception_df,
            x="Misconception",
            y="Students",
            title="Most Common Misconceptions"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------
    # TEACHER INTERVENTION
    # --------------------------------------------------

    st.divider()

    st.header(
        "🎯 Teacher Intervention"
    )


    if misconception_summary:

        selected = st.selectbox(

            "Select a misconception",

            [
                item["misconception"]
                for item
                in misconception_summary
            ]

        )

        intervention = get_intervention(
            selected
        )


        st.subheader(
            intervention["title"]
        )

        st.write(
            intervention["description"]
        )

        st.info(
            f"Recommended Activity:\n\n"
            f"{intervention['activity']}"
        )

        st.write(
            f"⏱️ Duration: "
            f"{intervention['duration']}"
        )


        st.subheader(
            "Suggested Questions"
        )

        for question in intervention[
            "questions"
        ]:

            st.write(
                f"• {question}"
            )


    else:

        st.success(
            "No intervention required."
        )


    # --------------------------------------------------
    # STUDENT INSIGHTS
    # --------------------------------------------------

    st.divider()

    st.header(
        "👨‍🎓 Student-Level Insights"
    )


    student_list = sorted(
        set(
            result["student_id"]
            for result in results
        )
    )


    selected_student = st.selectbox(
        "Select a student",
        student_list
    )


    student_results = [

        result

        for result in results

        if result["student_id"]
        == selected_student

    ]


    for result in student_results:

        diagnosis = result[
            "diagnosis"
        ]


        # SHOW ACTUAL QUESTION
        st.subheader(
            "Question"
        )

        st.write(
            result["question"]
        )


        # STUDENT ANSWER
        st.write(
            "**Student Answer:**"
        )

        st.write(
            result["answer"]
        )


        # MISCONCEPTION
        misconception = diagnosis.get(
            "misconception",
            "NONE"
        )


        if misconception == "AI_ERROR":

            st.error(
                "AI analysis failed."
            )

        elif misconception == "QUESTION_NOT_FOUND":

            st.error(
                "Question not found in the question bank."
            )

        elif misconception != "NONE":

            st.error(
                f"Misconception: "
                f"{misconception}"
            )

        else:

            st.success(
                "No major misconception detected."
            )


        # CONFIDENCE
        confidence = diagnosis.get(
            "confidence",
            0
        )

        st.write(
            f"AI Confidence: "
            f"{confidence * 100:.0f}%"
        )


        # EXPLANATION
        st.write(
            "**AI Explanation:**"
        )

        st.write(
            diagnosis.get(
                "explanation",
                ""
            )
        )


        # EVIDENCE
        st.write(
            "**Evidence from Student Answer:**"
        )

        st.write(
            diagnosis.get(
                "evidence",
                ""
            )
        )


        # CONCEPTS
        st.write(
            "**Concepts Understood:**"
        )

        st.write(
            diagnosis.get(
                "concepts_understood",
                []
            )
        )


        st.write(
            "**Concepts Misunderstood:**"
        )

        st.write(
            diagnosis.get(
                "concepts_misunderstood",
                []
            )
        )


        st.divider()