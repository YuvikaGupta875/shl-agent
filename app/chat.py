from app.retrieval import search_catalog, find_by_name

OFFTOPIC = [
    "weather",
    "ipl",
    "cricket",
    "football",
    "movie",
    "salary",
    "politics",
    "president",
    "prime minister"
]

LEGAL = [
    "legal",
    "law",
    "hipaa",
    "compliance",
    "required by law"
]


def process_chat(messages):

    # -------- Conversation --------
    user_messages = [
        m.content
        for m in messages
        if m.role == "user"
    ]

    conversation = " ".join(user_messages)

    text = conversation.lower()

    last_message = user_messages[-1].lower()

    # -------- Legal refusal --------
    if any(word in last_message for word in LEGAL):

        return {
            "reply": (
                "I can help recommend SHL assessments, but I can't provide legal "
                "or regulatory advice. Please consult your legal or compliance team."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # -------- Off topic --------
    if any(word in last_message for word in OFFTOPIC):

        return {
            "reply": "I can only help with SHL assessments and assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -------- Compare --------
    if "compare" in last_message or "difference" in last_message:

        opq = find_by_name("OPQ")
        gsa = find_by_name("Global Skills Assessment")

        if opq and gsa:

            return {

                "reply": (
                    f"{opq[0]['name']} is a personality assessment, while "
                    f"{gsa[0]['name']} focuses on workplace skills and competencies."
                ),

                "recommendations": [
                    opq[0],
                    gsa[0]
                ],

                "end_of_conversation": False

            }

        results = search_catalog(text)

        if len(results) >= 2:

            return {

                "reply": (
                    f"{results[0]['name']} differs from "
                    f"{results[1]['name']} based on their assessment purpose."
                ),

                "recommendations": results[:2],

                "end_of_conversation": False

            }

        return {

            "reply": "Please mention the two SHL assessments you would like me to compare.",

            "recommendations": [],

            "end_of_conversation": False

        }

    # -------- Clarification --------
    vague_queries = [

        "assessment",

        "need assessment",

        "test",

        "hire",

        "hiring"

    ]

    if text in vague_queries or len(last_message.split()) < 4:

        return {

            "reply": (
                "Could you tell me the job role, required skills, seniority, "
                "or paste the job description?"
            ),

            "recommendations": [],

            "end_of_conversation": False

        }

    # -------- Refinement --------
    if any(word in last_message for word in [

        "add",

        "remove",

        "drop",

        "include"

    ]):

        recommendations = search_catalog(text)

        return {

            "reply": "Updated the recommendations based on your latest requirements.",

            "recommendations": recommendations,

            "end_of_conversation": False

        }

    # -------- Recommendation --------
    recommendations = search_catalog(text)

    if not recommendations:

        return {

            "reply": (
                "I couldn't confidently recommend SHL assessments based on the "
                "information provided. Please provide more details."
            ),

            "recommendations": [],

            "end_of_conversation": False

        }

    reply = (
        f"I found {len(recommendations)} SHL assessments matching your "
        "requirements based on the skills, experience, and context provided."
    )

    confirm_words = [

        "perfect",

        "confirmed",

        "looks good",

        "that's good",

        "locking it in",

        "final",

        "done",

        "thanks"

    ]

    done = any(word in last_message for word in confirm_words)

    return {

        "reply": reply,

        "recommendations": recommendations,

        "end_of_conversation": done

    }