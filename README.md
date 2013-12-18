openerp-xmlrpc-caller
=====================

Simply call XML-RPC method on OpenERP instances

    $ ./oe-xmlrpc-caller.py test_db ir.module.module read "`./debug_rpc.py test_db ir.module.module search \"[('name','ilike','remote')]\"`" "['name','state']" 
    [{'id': 150, 'name': 'sync_remote_warehouse', 'state': 'installed'},
     {'id': 85, 'name': 'sync_remote_warehouse_server', 'state': 'uninstalled'}]
