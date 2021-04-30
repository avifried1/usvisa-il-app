"""
Class to keep all css constants
Types of elements are ID, Xpath & CSS Selector
"""


class ElementPath(object):
    LOGIN_BUTTON_XPATH = '/html/body/div[6]/div[3]/div/button/span'
    USER_EMAIL_ID = 'user_email'
    USER_PASSWORD_ID = 'user_password'
    POLICY_AGREEMENT_CHECKBOX_XPATH = '/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[3]/label/div'
    SIGNIN_BUTTON_XPATH = '/html/body/div[5]/main/div[3]/div/div[1]/div/form/p[1]/input'
    DATE_PICKER_ID = 'appointments_consulate_appointment_date'
    ACTIVE_DAY_CELL_SELECTOR = '.undefined[data-handler="selectDay"]'
    NEXT_MONTH_XPATH = '//*[@id="ui-datepicker-div"]/div[2]/div/a/span'
    APPOINTMENT_TIMES_XPATH = '//*[@id="appointments_consulate_appointment_time"]'
    APPOINTMENT_SUBMIT_ID = 'appointments_submit'

    DAY_CELL_YEAR_ATTRIBUTE = 'data-year'
    DAY_CELL_MONTH_ATTRIBUTE = 'data-month'
