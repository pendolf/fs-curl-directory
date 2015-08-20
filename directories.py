#!/usr/bin/env python
# -*- coding: utf-8 -*-

print "Content-Type: text/xml"
print

from lxml.builder import E
from lxml import etree
import hashlib
import cgi
import pyodbc


connection = pyodbc.connect('DRIVER={MySQL};DSN=sipdb')
cursor = connection.cursor()


def create_base_directory_xml_doc():
    doc = (
        E.document(
            E.section(name="directory"),
            type="freeswitch/xml"
        )
    )
    return doc


def not_found():
    doc = (
        E.document(
            E.section(name="result"),
            type="freeswitch/xml"
        )
    )
    result = E.result(status="not found")
    section = doc.find("section")
    section.append(result)
    return doc


def hash_password(domain, username, password):
    hash = hashlib.md5()
    hash.update(username + ":" + domain + ":" + password)
    password_hash = hash.hexdigest()
    password_param = "a1-hash"
    return password_param, password_hash


def add_directory_domain_user(doc, domain, username, password, user_context, callgroup):
    section = doc.find("section")
    dom = (
        E.domain(E.params(E.param(
            name="dial-string",
            value='{^^:sip_invite_domain=${dialed_domain}:presence_id=${dialed_user}@${dialed_domain}}${sofia_contact(*/${dialed_user}@${dialed_domain})}')),
            E.groups(), name=domain))
    section.append(dom)

    grp = E.group(E.users(), name=domain)
    groups = dom.find("groups")
    groups.append(grp)

    usr = E.user(
        E.params(
            E.param(name="password", value=password),
            E.param(name="vm-password", value=password),
            E.param(name="register", value="false"),
            E.param(name="register-transport", value="ws"),
            # E.param(name="session-timeout", value="true"),
            # E.param(name="minimum-session-expires", value="120"),
            E.param(name="rtp-timer-name", value="soft"),
            E.param(name="apply-inbound-acl", value="goip"),
        ),
        E.variables(
            E.variable(name="toll_allow", value="domestic,international,local"),
            E.variable(name="user_context", value=user_context),
            E.variable(name="accountcode", value=username),
            E.variable(name="effective_caller_id_name", value=username),
            E.variable(name="effective_caller_id_number", value=username),
            E.variable(name="outbound_caller_id_name", value="$${outbound_caller_name}"),
            E.variable(name="outbound_caller_id_number", value="$${outbound_caller_id}"),
            E.variable(name="callgroup", value=callgroup),
            E.variable(name="rtp_secure_media", value="true"),
            E.variable(name="max_calls", value="1"),
        ),
        id=username
    )
    users = grp.find("users")
    users.append(usr)


def select_by_username(username):
    row = cursor.execute("select * from fs_users WHERE accountcode=?", username).fetchone()
    return row

form = cgi.FieldStorage()
domain = form.getvalue('domain', None)
username = form.getvalue('user', None)

if domain and username:
    user = select_by_username(username)
    if user:
        document = create_base_directory_xml_doc()
        add_directory_domain_user(document, domain, username, user.password, user.user_context, user.callgroup)
    else:
        document = not_found()
else:
    document = not_found()

print(etree.tostring(document, encoding='UTF-8', standalone=False, pretty_print=True))
