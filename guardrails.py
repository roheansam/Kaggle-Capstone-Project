def validate_project_idea(user_input: str):
    """
    Basic safety and quality checks for the project idea.
    """

    if not user_input or len(user_input.strip()) < 5:
        return False, "Please enter a clearer project idea."

    risky_keywords = [
        "hack",
        "steal password",
        "malware",
        "phishing",
        "illegal",
        "weapon",
        "fake certificate"
    ]

    lowered_input = user_input.lower()

    for keyword in risky_keywords:
        if keyword in lowered_input:
            return False, "This project idea may be unsafe or unethical. Please choose a safe and useful project topic."

    return True, "Valid idea."