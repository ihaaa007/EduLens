INTERVENTIONS = {

    "FLOW_CONGESTION_CONFUSION": {
        "title": "Flow Control vs Congestion Control",

        "description": (
            "The student is confusing receiver-side "
            "flow control with network congestion control."
        ),

        "activity": (
            "Draw a simple diagram showing a sender, "
            "receiver, and network. Explain how flow "
            "control protects the receiver while "
            "congestion control manages network traffic."
        ),

        "duration": "5 minutes",

        "questions": [
            "Which mechanism prevents a fast sender from overwhelming a slow receiver?",
            "Which mechanism reacts to congestion inside the network?",
            "Explain flow control in one sentence."
        ]
    },


    "RECEIVER_NETWORK_CONFUSION": {
        "title": "Receiver vs Network Protection",

        "description": (
            "The student is confusing protection of "
            "the receiver with protection of the network."
        ),

        "activity": (
            "Use a sender → network → receiver diagram "
            "and identify which part is protected by "
            "flow control and which part is affected "
            "by congestion control."
        ),

        "duration": "5 minutes",

        "questions": [
            "What does flow control protect?",
            "What does congestion control respond to?",
            "Where does network congestion occur?"
        ]
    },


    "TCP_RELIABILITY_MISUNDERSTANDING": {
        "title": "Understanding TCP Reliability",

        "description": (
            "The student has difficulty understanding "
            "how TCP provides reliable data transmission."
        ),

        "activity": (
            "Draw a simple packet-flow diagram showing "
            "sequence numbers, acknowledgements, and "
            "retransmission."
        ),

        "duration": "7 minutes",

        "questions": [
            "Why does TCP use acknowledgements?",
            "What happens when a TCP segment is lost?",
            "What is the purpose of sequence numbers?"
        ]
    },


    "PACKET_LOSS_MISUNDERSTANDING": {
        "title": "Understanding TCP Packet Loss",

        "description": (
            "The student misunderstands what happens "
            "when a TCP packet is lost."
        ),

        "activity": (
            "Demonstrate packet loss using three packets. "
            "Remove one packet and show how TCP detects "
            "the problem and retransmits it."
        ),

        "duration": "5 minutes",

        "questions": [
            "What happens when TCP detects a missing segment?",
            "Why is retransmission necessary?"
        ]
    },


    "HANDSHAKE_MISUNDERSTANDING": {
        "title": "TCP Three-Way Handshake",

        "description": (
            "The student has difficulty understanding "
            "the sequence used to establish a TCP connection."
        ),

        "activity": (
            "Draw the sequence SYN → SYN-ACK → ACK "
            "and explain what each message means."
        ),

        "duration": "5 minutes",

        "questions": [
            "What is the first message sent by the client?",
            "What does SYN-ACK represent?",
            "Why is the final ACK required?"
        ]
    },


    "SYN_ACK_CONFUSION": {
        "title": "Understanding SYN and SYN-ACK",

        "description": (
            "The student is confusing the SYN and "
            "SYN-ACK messages in the TCP handshake."
        ),

        "activity": (
            "Draw the three messages separately and "
            "label who sends each message."
        ),

        "duration": "5 minutes",

        "questions": [
            "Who sends SYN?",
            "Who sends SYN-ACK?",
            "Who sends the final ACK?"
        ]
    }
}


def get_intervention(misconception):

    return INTERVENTIONS.get(
        misconception,
        {
            "title": "General Concept Review",

            "description": (
                "The student needs additional review "
                "of the relevant concept."
            ),

            "activity": (
                "Review the relevant concept using "
                "a simple example or diagram."
            ),

            "duration": "5 minutes",

            "questions": []
        }
    )