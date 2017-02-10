import os.path

from saml2.entity_category.edugain import COC
from saml2 import BINDING_HTTP_REDIRECT
from saml2 import BINDING_HTTP_POST
from saml2.saml import NAME_FORMAT_URI, NAMEID_FORMAT_PERSISTENT

#BASE= 'https://catalog.data.gov/'
#BASE= 'https://saml-test.datagov.ckan.org/'
BASE = 'http://localhost/'
CONFIG_PATH = os.path.dirname(__file__)


try:
    from saml2.sigver import get_xmlsec_binary
except ImportError:
    get_xmlsec_binary = None


if get_xmlsec_binary:
    xmlsec_path = get_xmlsec_binary(["/opt/local/bin", "/usr/bin", "/bin"])
else:
    xmlsec_path = '/bin/xmlsec1'


CONFIG = {
    'entityid' : 'urn:mace:umu.se:saml:ckan:sp',
    'entity_category': [COC],
    'description': 'CKAN saml2 authorizor',
    'service': {
        'sp': {
            "authn_requests_signed": True,
            "logout_requests_signed": True,
            'name' : 'CKAN SP',
            #'name_id_format': NAMEID_FORMAT_PERSISTENT,
            'endpoints': {
                'assertion_consumer_service': [BASE],
                'single_logout_service' : [(BASE + 'slo',
                                            BINDING_HTTP_REDIRECT)],
                #"assertion_consumer_service": [
                #    ("%s/acs/post" % BASE, BINDING_HTTP_POST)
                #],
                #"single_logout_service": [
                #    ("%s/slo/redirect" % BASE, BINDING_HTTP_REDIRECT),
                #    ("%s/slo/post" % BASE, BINDING_HTTP_POST),
                #],
            },
            'required_attributes': [
                'displayName',
                'mail',
                'group',
                'groupType',
                'roleOccupant',
                'fullname',
                'sn',
                'givenname',
            ],
            'allow_unsolicited': True,
            'optional_attributes': [],
            'idp': ['urn:mace:umu.se:saml:ckan:idp'],
        }
    },
    'allow_unknown_attributes': True,
    'debug': 0,
    'key_file': CONFIG_PATH + '/pki/mykey.pem',
    'cert_file': CONFIG_PATH + '/pki/mycert.pem',
    'attribute_map_dir': CONFIG_PATH + '/../attributemaps',
    "xmlsec_binary": xmlsec_path,
    'metadata': {
       'local': [CONFIG_PATH + '/dir_idp'],
    },
    # -- below used by make_metadata --
    'organization': {
        'name': 'Exempel AB',
        'display_name': [('Exempel AB','se'),('Example Co.','en')],
        'url':'http://www.example.com/ckan',
    },
    'contact_person': [{
        'given_name':'John',
        'sur_name': 'Smith',
        'email_address': ['john.smith@example.com'],
        'contact_type': 'technical',
        },
    ],
    'name_form': NAME_FORMAT_URI,
    'logger': {
        'rotating': {
            'filename': '/tmp/sp.log',
            'maxBytes': 100000,
            'backupCount': 5,
            },
        'loglevel': 'error',
    }
}
