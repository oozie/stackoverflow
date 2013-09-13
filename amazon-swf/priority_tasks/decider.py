import boto.swf.layer2 as swf

DOMAIN = 'stackoverflow'
ACTIVITY = 'SomeActivity'
VERSION = '1.0'

class MyWorkflowDecider(swf.Decider):

    domain = DOMAIN
    task_list = 'default_tasks'
    version = VERSION

    def run(self):
        history = self.poll()
        print history
        if 'events' in history:
            # Get a list of non-decision events to see what event came in last.
            workflow_events = [e for e in history['events']
                               if not e['eventType'].startswith('Decision')]

            decisions = swf.Layer1Decisions()

            last_event = workflow_events[-1]
            last_event_type = last_event['eventType']

            if last_event_type == 'WorkflowExecutionStarted':
                # At the start, get the worker to fetch the first assignment.
                decisions.schedule_activity_task(ACTIVITY+'1', ACTIVITY, VERSION, task_list='default_tasks')
                decisions.schedule_activity_task(ACTIVITY+'2', ACTIVITY, VERSION, task_list='urgent_tasks')
                decisions.schedule_activity_task(ACTIVITY+'3', ACTIVITY, VERSION, task_list='default_tasks')
                decisions.schedule_activity_task(ACTIVITY+'4', ACTIVITY, VERSION, task_list='urgent_tasks')
                decisions.schedule_activity_task(ACTIVITY+'5', ACTIVITY, VERSION, task_list='default_tasks')
            elif last_event_type == 'ActivityTaskCompleted':
                # Complete workflow execution after 5 completed activities.
                closed_activity_count = sum(1 for wf_event in workflow_events if wf_event.get('eventType') == 'ActivityTaskCompleted')
                if closed_activity_count == 5:
                    decisions.complete_workflow_execution()

            self.complete(decisions=decisions)
            return True
