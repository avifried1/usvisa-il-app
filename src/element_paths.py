"""
Class to keep all css constants
Types of elements are ID, Xpath & CSS Selector
"""


class ElementPath(object):
    LOGIN_BUTTON_XPATH = '/html/body/div[6]/div[3]/div/button'
    USER_EMAIL_ID = 'user_email'
    USER_PASSWORD_ID = 'user_password'
    POLICY_AGREEMENT_CHECKBOX_XPATH = '/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[3]/label/div'
    SIGNIN_BUTTON_XPATH = '/html/body/div[5]/main/div[3]/div/div[1]/div/form/p[1]/input'
    DATE_PICKER_ID = 'appointments_consulate_appointment_date'
    ACTIVE_GROUP_CARD_CLASS = '.application.attend_appointment.card.success'
    CONTINUE_BUTTON_CLASS = '.button.primary.small'
    ACCORDION_BUTTONS_CLASS = 'accordion-item'
    ACTION_BUTTONS_CLASS = '.button.small.primary.small-only-expanded'
    ACTIVE_DAY_CELL_SELECTOR = '.undefined[data-handler="selectDay"]'
    NEXT_MONTH_XPATH = '//*[@id="ui-datepicker-div"]/div[2]/div/a'
    APPOINTMENT_TIMES_ID = 'appointments_consulate_appointment_time'
    APPOINTMENT_SUBMIT_ID = 'appointments_submit'
    APPOINTMENT_CONFIRMATION_CLASS = '.button.alert'
    APPOINTMENT_SUCCESS_CLASS = '.ui-button.ui-corner-all.ui-widget'

    DAY_CELL_YEAR_ATTRIBUTE = 'data-year'
    DAY_CELL_MONTH_ATTRIBUTE = 'data-month'
