openerp-xmlrpc-caller
=====================

Simply call XML-RPC method on OpenERP instances

Synopsis
--------

```bash
# Simple call
$ ./oe-xmlrpc-caller.py test_db ir.module.module search "[('name','=ilike','event%')]"
[158, 150, 85]

# Nested calls using back-ticks
$ ./oe-xmlrpc-caller.py test_db ir.module.module read \
    "`./oe-xmlrpc-caller.py test_db ir.module.module search \"[('name','=ilike','event%')]\"`" \
    "['name','state']" 
[{'id': 158, 'name': 'event_moodle', 'state': 'uninstalled'},
 {'id': 150, 'name': 'event_sale', 'state': 'uninstalled'},
 {'id': 85, 'name': 'event', 'state': 'installed'}]
```
