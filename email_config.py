#Email template to send when the login is unsuccessful to the mail address of the user
#
email_body = """Hello,
    We are sorry to inform you that the login to {website} was unsuccessful.
    Please check your credentials and try again.
    If the problem persists, please contact us.
    Best regards,
    The Test team"""
email_subject = "Login unsuccessful for {website}"


gmail_sender_account = "test@gmail.com"
gmail_sender_password = ''

email_body_no_job = """Hello,
    We are sorry to inform you that there are no jobs available for {website}.
    Please check back later.
    
    Best regards,
    The Test team"""

email_subject_no_job = "No jobs available for {website}"
