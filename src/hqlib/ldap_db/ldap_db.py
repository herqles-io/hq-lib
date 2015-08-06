import ldap


class LDAP(object):

    def __init__(self, host, domain, base_dn):
        self.host = host
        self.domain = domain
        self.base_dn = base_dn

    def connection_as(self, username, password):
        conn = ldap.initialize("ldap://"+self.host)
        conn.set_option(ldap.OPT_REFERRALS, 0)
        conn.simple_bind_s(username+"@"+self.domain, password)
        return conn