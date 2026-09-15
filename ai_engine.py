# ============================================================
# EduLens - Local AI Diagnostic Engine
# Works WITHOUT an OpenAI API key
# ============================================================

from questions import get_question


# ------------------------------------------------------------
# MAIN ANALYSIS FUNCTION
# ------------------------------------------------------------

def analyze_answer(question_id, student_answer):

    # Get question information
    question_data = get_question(question_id)

    question = question_data["question"]

    answer = student_answer.lower().strip()


    # ========================================================
    # Q1 - FLOW CONTROL vs CONGESTION CONTROL
    # ========================================================

    if question_id == "Q1":

        # Words related to flow control
        flow_words = [
            "receiver",
            "receiver buffer",
            "buffer",
            "slow receiver",
            "receive",
            "accept"
        ]

        # Words related to congestion control
        congestion_words = [
            "network",
            "congestion",
            "traffic",
            "too many packets",
            "network traffic"
        ]


        has_flow = any(
            word in answer
            for word in flow_words
        )

        has_congestion = any(
            word in answer
            for word in congestion_words
        )


        # ----------------------------------------------------
        # CORRECT ANSWER
        # ----------------------------------------------------

        if has_flow and has_congestion:

            return {

                "concepts_understood": [
                    "flow control",
                    "congestion control",
                    "receiver protection",
                    "network congestion"
                ],

                "concepts_partial": [],

                "concepts_misunderstood": [],

                "misconception": "NONE",

                "evidence": (
                    "The student correctly connects "
                    "flow control with the receiver "
                    "and congestion control with the network."
                ),

                "confidence": 0.95,

                "explanation": (
                    "The student correctly distinguishes "
                    "flow control from congestion control. "
                    "Flow control protects the receiver, "
                    "while congestion control deals with "
                    "network congestion."
                ),

                "recommended_action": (
                    "No major intervention required. "
                    "Continue with normal practice."
                )
            }


        # ----------------------------------------------------
        # FLOW CONTROL / CONGESTION CONFUSION
        # ----------------------------------------------------

        if (
            "flow control" in answer
            and (
                "network congestion" in answer
                or "network" in answer
                or "traffic" in answer
            )
        ):

            return {

                "concepts_understood": [],

                "concepts_partial": [
                    "flow control"
                ],

                "concepts_misunderstood": [
                    "congestion control",
                    "receiver protection"
                ],

                "misconception":
                    "FLOW_CONGESTION_CONFUSION",

                "evidence": (
                    "The student associates flow control "
                    "with congestion or network traffic "
                    "instead of receiver protection."
                ),

                "confidence": 0.92,

                "explanation": (
                    "The student is confusing flow control "
                    "with congestion control. Flow control "
                    "controls how much data a receiver can "
                    "handle, while congestion control deals "
                    "with congestion in the network."
                ),

                "recommended_action": (
                    "Use a sender → receiver diagram and "
                    "ask the student to identify what flow "
                    "control protects and what congestion "
                    "control manages."
                )
            }


        # ----------------------------------------------------
        # RECEIVER / NETWORK CONFUSION
        # ----------------------------------------------------

        if (
            "congestion control" in answer
            and (
                "receiver" in answer
                or "buffer" in answer
            )
        ):

            return {

                "concepts_understood": [],

                "concepts_partial": [
                    "congestion control"
                ],

                "concepts_misunderstood": [
                    "receiver protection",
                    "network congestion"
                ],

                "misconception":
                    "RECEIVER_NETWORK_CONFUSION",

                "evidence": (
                    "The student describes congestion "
                    "control as protecting the receiver."
                ),

                "confidence": 0.93,

                "explanation": (
                    "The student has confused the purpose "
                    "of congestion control with flow control. "
                    "Flow control protects the receiver from "
                    "being overwhelmed, while congestion "
                    "control manages traffic in the network."
                ),

                "recommended_action": (
                    "Draw a sender → network → receiver "
                    "diagram and label which mechanism "
                    "protects the receiver and which manages "
                    "network congestion."
                )
            }


        # ----------------------------------------------------
        # BOTH ARE THE SAME
        # ----------------------------------------------------

        if (
            "same" in answer
            or "same thing" in answer
            or (
                "both" in answer
                and "receiver" in answer
            )
        ):

            return {

                "concepts_understood": [],

                "concepts_partial": [],

                "concepts_misunderstood": [
                    "flow control",
                    "congestion control"
                ],

                "misconception":
                    "FLOW_CONGESTION_CONFUSION",

                "evidence": (
                    "The student treats flow control "
                    "and congestion control as the "
                    "same mechanism."
                ),

                "confidence": 0.98,

                "explanation": (
                    "Flow control and congestion control "
                    "are different mechanisms. Flow control "
                    "protects the receiver, while congestion "
                    "control responds to congestion in the "
                    "network."
                ),

                "recommended_action": (
                    "Teach the two mechanisms side-by-side "
                    "using a simple sender → network → "
                    "receiver diagram."
                )
            }


        # ----------------------------------------------------
        # PARTIAL UNDERSTANDING
        # ----------------------------------------------------

        if has_flow:

            return {

                "concepts_understood": [
                    "flow control"
                ],

                "concepts_partial": [
                    "congestion control"
                ],

                "concepts_misunderstood": [],

                "misconception":
                    "FLOW_CONGESTION_CONFUSION",

                "evidence": (
                    "The student mentions flow control "
                    "but does not clearly distinguish "
                    "it from congestion control."
                ),

                "confidence": 0.78,

                "explanation": (
                    "The student shows some understanding "
                    "of flow control but has not clearly "
                    "explained the difference between "
                    "flow control and congestion control."
                ),

                "recommended_action": (
                    "Give the student a short comparison "
                    "exercise between receiver protection "
                    "and network congestion."
                )
            }


        # ----------------------------------------------------
        # DEFAULT Q1 CASE
        # ----------------------------------------------------

        return {

            "concepts_understood": [],

            "concepts_partial": [
                "flow control",
                "congestion control"
            ],

            "concepts_misunderstood": [],

            "misconception":
                "FLOW_CONGESTION_CONFUSION",

            "evidence": (
                "The answer does not clearly demonstrate "
                "the distinction between flow control "
                "and congestion control."
            ),

            "confidence": 0.70,

            "explanation": (
                "The answer needs more explanation of "
                "the difference between flow control and "
                "congestion control."
            ),

            "recommended_action": (
                "Review the difference using a simple "
                "sender, network, and receiver diagram."
            )
        }


    # ========================================================
    # Q2 - TCP RELIABILITY
    # ========================================================

    if question_id == "Q2":

        reliability_words = [
            "acknowledgement",
            "acknowledgment",
            "ack",
            "sequence number",
            "sequence numbers",
            "retransmission",
            "retransmit"
        ]

        found = [
            word
            for word in reliability_words
            if word in answer
        ]


        if len(found) >= 2:

            return {

                "concepts_understood": [
                    "acknowledgement",
                    "sequence numbers",
                    "retransmission"
                ],

                "concepts_partial": [],

                "concepts_misunderstood": [],

                "misconception": "NONE",

                "evidence": (
                    "The student mentions multiple "
                    "mechanisms used by TCP to provide "
                    "reliable transmission."
                ),

                "confidence": 0.94,

                "explanation": (
                    "The student understands that TCP "
                    "uses acknowledgements, sequence "
                    "numbers and retransmission to provide "
                    "reliable data transmission."
                ),

                "recommended_action": (
                    "Continue with normal practice."
                )
            }


        if (
            "packet" in answer
            and "loss" in answer
        ):

            return {

                "concepts_understood": [
                    "packet loss"
                ],

                "concepts_partial": [
                    "retransmission"
                ],

                "concepts_misunderstood": [
                    "TCP reliability"
                ],

                "misconception":
                    "PACKET_LOSS_MISUNDERSTANDING",

                "evidence": (
                    "The student mentions packet loss "
                    "but does not explain how TCP detects "
                    "and recovers from it."
                ),

                "confidence": 0.85,

                "explanation": (
                    "The student recognizes packet loss "
                    "but needs to understand how TCP uses "
                    "acknowledgements and retransmission "
                    "to recover from lost data."
                ),

                "recommended_action": (
                    "Demonstrate three packets being sent, "
                    "remove one packet, and show how TCP "
                    "retransmits the missing packet."
                )
            }


        return {

            "concepts_understood": [],

            "concepts_partial": [
                "TCP reliability"
            ],

            "concepts_misunderstood": [
                "acknowledgement",
                "sequence numbers",
                "retransmission"
            ],

            "misconception":
                "TCP_RELIABILITY_MISUNDERSTANDING",

            "evidence": (
                "The answer does not clearly explain "
                "the mechanisms TCP uses for reliability."
            ),

            "confidence": 0.80,

            "explanation": (
                "The student needs more practice with "
                "acknowledgements, sequence numbers and "
                "retransmission."
            ),

            "recommended_action": (
                "Draw a simple packet-flow diagram showing "
                "sequence numbers, acknowledgements and "
                "retransmission."
            )
        }


    # ========================================================
    # Q3 - THREE WAY HANDSHAKE
    # ========================================================

    if question_id == "Q3":

        has_syn = "syn" in answer

        has_syn_ack = (
            "syn-ack" in answer
            or "syn ack" in answer
            or "synack" in answer
        )

        has_ack = (
            "ack" in answer
            or "acknowledgement" in answer
        )


        # ----------------------------------------------------
        # CORRECT HANDSHAKE
        # ----------------------------------------------------

        if (
            has_syn
            and has_syn_ack
            and has_ack
        ):

            return {

                "concepts_understood": [
                    "SYN",
                    "SYN-ACK",
                    "ACK",
                    "connection establishment"
                ],

                "concepts_partial": [],

                "concepts_misunderstood": [],

                "misconception": "NONE",

                "evidence": (
                    "The student identifies the three "
                    "messages used during TCP connection "
                    "establishment."
                ),

                "confidence": 0.96,

                "explanation": (
                    "The student understands the TCP "
                    "three-way handshake: SYN, SYN-ACK "
                    "and ACK."
                ),

                "recommended_action": (
                    "Continue with normal practice."
                )
            }


        # ----------------------------------------------------
        # SYN / SYN-ACK CONFUSION
        # ----------------------------------------------------

        if (
            has_syn
            and not has_syn_ack
        ):

            return {

                "concepts_understood": [
                    "SYN"
                ],

                "concepts_partial": [
                    "connection establishment"
                ],

                "concepts_misunderstood": [
                    "SYN-ACK",
                    "ACK"
                ],

                "misconception":
                    "SYN_ACK_CONFUSION",

                "evidence": (
                    "The student mentions SYN but does "
                    "not correctly describe the SYN-ACK "
                    "and final ACK steps."
                ),

                "confidence": 0.82,

                "explanation": (
                    "The student has partial understanding "
                    "of the handshake but needs to learn "
                    "the sequence SYN → SYN-ACK → ACK."
                ),

                "recommended_action": (
                    "Draw the three messages separately "
                    "and label who sends each message."
                )
            }


        # ----------------------------------------------------
        # DEFAULT HANDSHAKE CASE
        # ----------------------------------------------------

        return {

            "concepts_understood": [],

            "concepts_partial": [
                "connection establishment"
            ],

            "concepts_misunderstood": [
                "SYN",
                "SYN-ACK",
                "ACK"
            ],

            "misconception":
                "HANDSHAKE_MISUNDERSTANDING",

            "evidence": (
                "The answer does not clearly explain "
                "the TCP three-way handshake."
            ),

            "confidence": 0.88,

            "explanation": (
                "The student needs to review the three "
                "steps used by TCP to establish a connection."
            ),

            "recommended_action": (
                "Draw and explain SYN → SYN-ACK → ACK."
            )
        }


    # ========================================================
    # UNKNOWN QUESTION
    # ========================================================

    return {

        "concepts_understood": [],

        "concepts_partial": [],

        "concepts_misunderstood": [],

        "misconception": "NONE",

        "evidence": "Question is not supported yet.",

        "confidence": 0.50,

        "explanation": (
            "This question has not yet been added "
            "to the EduLens diagnostic engine."
        ),

        "recommended_action": (
            "Add diagnostic rules for this question."
        )
    }