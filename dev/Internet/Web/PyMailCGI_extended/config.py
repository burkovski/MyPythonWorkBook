class DBResponse(dict):
    path = "database/database.sqlite3"
    users_table = "users"
    empty_field = "NULL"


class DBUsersFields(dict):
    username = "user_name"
    password = "user_passwd"
    session = "user_session"


class FormFields(dict):
    handler_script = "formaction"
    username = "username"
    verify_mode = "verify_mode"
    vm_sign_in = "sign_in"
    vm_sign_up = "sign_up"
    password = "password"
    repeat_password = "rep_password"
    user_id = "u_id"
    session_id = "s_id"
    submit_button_caption = "caption"


class OptionsKeys(FormFields):
    prompt = "prompt"
    kind = "kind"
    extra_fields = "extras"
