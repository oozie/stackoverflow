import boto.swf.layer2 as swf

DOMAIN = 'stackoverflow'
VERSION = '1.0'

swf.Domain(name=DOMAIN).register()
swf.ActivityType(domain=DOMAIN, name='SomeActivity', version=VERSION, task_list='default_tasks').register()
swf.WorkflowType(domain=DOMAIN, name='MyWorkflow', version=VERSION, task_list='default_tasks').register()
