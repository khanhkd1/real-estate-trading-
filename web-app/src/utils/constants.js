export const VALIDATE_EMAIL_REGEX = /^[a-zA-Z][a-zA-Z0-9_.-]{1,}@[a-z0-9]{1,}(\.[a-z0-9]{1,}){1,2}$/
export const VALIDATE_PHONE_REGEX_RULE = /((^0|^84|^\+84|^\(\+84\))+([0-9]{2}))+([0-9]{7}|[0-9]{1}\.[0-9]{3}\.[0-9]{3}|[0-9]{1}-[0-9]{3}-[0-9]{3}|[0-9]{1}\s[0-9]{3}\s[0-9]{3}$)/
export const VALIDATE_PASSWORD_REGEX_RULE = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$/
export const STATUS = {
    'PENDING': 1,
    'APPROVED': 2,
    'SHIPPED': 3,
    'RETURNED': 4,
    'CANCELED': 5,
};
export const ACTIVE_MENU = [
    'Home',
    'Recharges'
];
export const UPLOAD_EXCEL_STATUS = {
    'PENDING': 1,
    'PROCESSING': 2,
    'PROCESSED': 3,
    'FAILED': 4,
};
export const ACTION_UPLOAD_EXCEL = {
    'ADD': 1,
    'UPDATE_QUANTITY': 2,
    'OVERWRITE': 3,
    'OVERWRITE_QUANTITY': 4,
};
export const COMPLAINT_STATUS = {
    'PENDING': 1,
    'PROCESSING': 2,
    'DONE': 3,
};
export const TYPE = new Array()
TYPE['SHOPS'] = 1
TYPE['SELLERS'] = 2
