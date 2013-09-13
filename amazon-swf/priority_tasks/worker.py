import boto.swf.layer2 as swf

DOMAIN = 'stackoverflow'
VERSION = '1.0'

class PrioritizingWorker(swf.ActivityWorker):

    domain = DOMAIN
    version = VERSION

    def run(self):

        urgent_task_count = swf.Domain(name=DOMAIN).count_pending_activity_tasks('urgent_tasks').get('count', 0)
        if urgent_task_count > 0:
            self.task_list = 'urgent_tasks'
        else:
            self.task_list = 'default_tasks'
        activity_task = self.poll()

        if 'activityId' in activity_task:
            print urgent_task_count, 'urgent tasks in the queue. Executing ' + activity_task.get('activityId')
            self.complete()
            return True
