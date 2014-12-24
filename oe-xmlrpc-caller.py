#!/usr/bin/env python2

import sys
import os
import re
from pprint import pprint, pformat
import argparse
import xmlrpclib

re_autoeval = re.compile(r"^(-?\d+|None|True|False|\[.*\]"
                         r"|\{.*\}|\".*\"|'.*')$")

def warn(*messages):
    sys.stderr.write(" ".join(map(unicode, messages))+"\n")

def die(*messages):
    warn(*messages)
    sys.exit(1)

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--help', action='store_true')
parser.add_argument('--url',
    help="Specify the base xmlrpc url to connect")
parser.add_argument('--uid',
    help="Specify the user id instead of a login "
        "and skip the login procedure")
parser.add_argument('--login', '--username', '-U', default='admin')
parser.add_argument('--password', '-W', type=str, default=None)
parser.add_argument('--host', '-h', default='localhost')
parser.add_argument('--port', '-p', type=int)
parser.add_argument('--protocol', default='http',
    help="Can be http or https, but use xmlrpc only")
parser.add_argument('--debug', action='store_true')
parser.add_argument('--pipe', action='store_true',
    help="Print the result directly")
parser.add_argument('--pretty', action='store_true',
    help="Pretty print the result")
parser.add_argument('--serial', action='store_true',
    help="If the result is a list, print every element in a new line "
        "(useful with search() to iterate on it)")
parser.add_argument('--wrap', '-w',
                    help="Wrap the results in a function f(x)")
parser.add_argument('db', metavar='database', nargs='?')
parser.add_argument('model', nargs='?')
parser.add_argument('method', nargs='?')
parser.add_argument('args', nargs='*',
    help="Beware that the following arguments will be Pyton evaluated: "
        +re_autoeval.pattern)
opt = parser.parse_args()

if opt.help or not opt.db:
    parser.print_help()
    sys.exit(0)

def debug(*messages):
    if opt.debug:
        warn("debug:", *messages)

def require(args):
    for arg in (args.split()
              if isinstance(args, basestring)
              else args):
        if getattr(opt, arg) is None:
            die("missing argument:", arg)

wrap_code = compile(opt.wrap or 'x', 'wrapper.py', mode='eval')

if not opt.port:
    if opt.protocol == 'http':
        opt.port = 8069
    elif opt.protocol == 'https':
        opt.port = 8071
    else:
        die("can not determine port for protocol:", opt.protocol)
    debug("port determinated is:", opt.port)

if not opt.url:
    require("protocol host port")
    opt.url = "%s://%s:%s/xmlrpc" % (opt.protocol, opt.host, opt.port)
    debug("url determinated is:", opt.url)

if not opt.password:
    opt.password = opt.login

if opt.uid:
    opt.uid = int(opt.uid)
else:
    require("url login password")
    opt.uid = xmlrpclib.ServerProxy(opt.url + '/common')\
        .login(opt.db, opt.login, opt.password)
    if not opt.uid:
        die("login failed:", "%s@%s" % (opt.login, opt.db),
            "(password: %s)" % opt.password)
    elif not opt.model:
        print "login success:", "%s@%s" % (opt.login, opt.db), \
            "(password: %s, uid=%s)" % (opt.password, opt.uid)
        sys.exit(0)
    debug("login uid is:", opt.uid)

require("url db uid password model method")

opt.args = [
    (eval(arg) if re_autoeval.match(arg) else arg)
    for arg in opt.args ]

debug("call", opt.method, "on model", opt.model)
debug("arguments are:", pformat(opt.args))

try:
    result = xmlrpclib.ServerProxy(opt.url + '/object')\
        .execute(opt.db, opt.uid, opt.password,
                 opt.model, opt.method, *opt.args)
except xmlrpclib.Fault, fault:
    die("XML RPC Fault Code: %s\nXML RPC Fault String: %s"
        % (fault.faultCode, fault.faultString))
except TypeError:
    die("cannot marshal one of the arguments:\n"+
        "\n".join(map(unicode, opt.args)))

if opt.serial and hasattr(result, '__iter__'):
    debug("serial print")
    for value in result:
        if not opt.wrap:
            print value
        else:
            print eval(wrap_code, {}, {'x': value})
elif (os.isatty(sys.stdout.fileno()) or opt.pretty) \
     and not opt.pipe and not opt.serial:
    debug("pretty print")
    if not opt.wrap:
        pprint(result)
    else:
        pprint(eval(wrap_code, {}, {'x': result}))
else:
    debug("pipable print")
    if not opt.wrap:
        print result
    else:
        print eval(wrap_code, {}, {'x': result})
