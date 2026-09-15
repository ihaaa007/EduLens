QUESTIONS = {
    "Q1": {
        "topic": "Computer Networks",
        "subtopic": "TCP",
        "question": "Explain the difference between flow control and congestion control in TCP.",
        "concepts": [
            "flow control",
            "congestion control",
            "receiver protection",
            "network congestion"
        ],
        "misconception_labels": [
            "FLOW_CONGESTION_CONFUSION",
            "RECEIVER_NETWORK_CONFUSION",
            "NONE"
        ]
    },

    "Q2": {
        "topic": "Computer Networks",
        "subtopic": "TCP Reliability",
        "question": "How does TCP provide reliable data transmission?",
        "concepts": [
            "acknowledgement",
            "sequence numbers",
            "retransmission",
            "packet loss"
        ],
        "misconception_labels": [
            "TCP_RELIABILITY_MISUNDERSTANDING",
            "PACKET_LOSS_MISUNDERSTANDING",
            "NONE"
        ]
    },

    "Q3": {
        "topic": "Computer Networks",
        "subtopic": "TCP Connection",
        "question": "Explain the TCP three-way handshake.",
        "concepts": [
            "SYN",
            "SYN-ACK",
            "ACK",
            "connection establishment"
        ],
        "misconception_labels": [
            "HANDSHAKE_MISUNDERSTANDING",
            "SYN_ACK_CONFUSION",
            "NONE"
        ]
    }
}


def get_question(question_id):
    if question_id not in QUESTIONS:
        raise ValueError(
            f"Question ID '{question_id}' does not exist."
        )

    return QUESTIONS[question_id]