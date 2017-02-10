from pylons import config

def get_idps():
    idps = config.get('saml2.login_form_sso_text', '')
    if idps:
        idps_list = idps.split()
        dict_idps = {}
        for i in idps_list:
            list = i.split(",")
            dict_idps[list[0]] = list[1]
        return dict_idps
    return {}


