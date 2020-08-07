class State:
    def __init__(self, user_id, state_text):
        self.user_id = user_id
        self.state_text = state_text


# STATES:
# awaiting_photo
# awaiting_name
# awaiting_company
# awaiting_lfwhat
# awaiting_skills
# awaiting_photo_full
# awaiting_name_full
# awaiting_company_full
# awaiting_lfwhat_full
# awaiting_skills_full
# awaiting_active
# error
# awaiting_active_bool
# idle