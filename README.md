odoo-send
=========

Simply call XML-RPC method on Odoo instances

Synopsis
--------

```bash
# Simple call
$ ./odoo-send.py test_db ir.module.module search "[('name','=ilike','event%')]"
[158, 150, 85]

# Nested calls using back-ticks
$ ./odoo-send.py test_db ir.module.module read \
    "`./odoo-send.py test_db ir.module.module search \"[('name','=ilike','event%')]\"`" \
    "['name','state']"
[{'id': 158, 'name': 'event_moodle', 'state': 'uninstalled'},
 {'id': 150, 'name': 'event_sale', 'state': 'uninstalled'},
 {'id': 85, 'name': 'event', 'state': 'installed'}]
```
