# function to validate
def validate_login(usr_name_inp=None, usr_psswd_inp=None, usr_psswd_chk=None, registrationFlag=False):
    '''
    validate login or registration credentials
    :param usr_name_inp:  - user name
    :param usr_psswd_inp: - user password
    :param usr_psswd_chk: - user password (redundant input) used for registration purposes
    :param registrationFlag: - set to True if registration, otherwise False
    ;
    :return:
        usr_name - user name
        usr_psswd - user password
        message - error message
    '''
    # initialize output parameters
    usr_name = None
    usr_psswd = None
    message = None
    chkPsswd = True
    try:
        if usr_name_inp and len(usr_name_inp) >= 2 and usr_name_inp[0].isalnum():
            if usr_psswd_inp and len(usr_psswd_inp) >= 2 and usr_psswd_inp[0].isalnum():
                if (registrationFlag and usr_psswd_inp == usr_psswd_chk) or not registrationFlag:
                    usr_name = usr_name_inp
                    usr_psswd = usr_psswd_inp
                else:
                    message = "Password inputs do not match.  \n" + \
                              "Password input fields require identical strings in both fields"
            else:
                chkPsswd = False
                message = "Invalid password.\n Password needs to be at least two characters long and start" + \
                          " with the alphanumeric value"
        else:
            if chkPsswd:
                message = " Invalid username.\n Username needs to be at least two characters long and " + \
                          "start with the alphanumeric value"
            else:
                message = " Invalid username and password.\n These fields needs to be at least two characters long" + \
                          "and start with the alphanumeric value"
    except ValueError:
        message = " Invalid credentials.\n Username/Password need to be at least two characters long and" + \
                  "start with the alphanumeric value"
    return usr_name, usr_psswd, message

if __name__ == "__main__":
    name, psswd, msg = validate_login(usr_name_inp="df", usr_psswd_inp="sa", usr_psswd_chk="sdfa",
                                      registrationFlag=False)
    print(f"user name= {name} \n password= {psswd} \n message= {msg}")