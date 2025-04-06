class TaskRoutingAgent:
    def __init__(self):
        """Initializes the TaskRoutingAgent."""
       
        self.routing_table = {
            "Technical": "Tech Team",
            "Billing": "Finance Team",
            "General": "Support Team"
        }

    def route_task(self, task_description, category):
        """Routes a task to the appropriate team."""
        team = self.routing_table.get(category, "Support Team")  # Default
        return f"Task '{task_description}' routed to {team}"

    def track_task(self, task_id):
        """Tracks the status of a task (placeholder)."""
      
        return f"Task {task_id}: Status - Pending"

    def escalate_task(self, task_id, reason):
        """Escalates a task (placeholder)."""
        
        return f"Task {task_id} escalated. Reason: {reason}"