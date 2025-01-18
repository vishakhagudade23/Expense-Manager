# Copyright (c) 2024, Vishakha Gudade and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document

class LeaveApplication(Document):
    def total_days_calculate(self):
        if self.start_date and self.end_date:
            
            start_date = datetime.strptime(str(self.start_date), '%Y-%m-%d')
            end_date = datetime.strptime(str(self.end_date), '%Y-%m-%d')
            
            total_days = (end_date - start_date).days + 1  
            self.total_days = total_days
        else:
            self.total_days = 0


    def validate(self):
        if self.workflow_state == "Pending":
            self.status = "Pending"
        elif self.workflow_state == "Approved":
            self.status = "Approved"
        elif self.workflow_state == "Rejected":
            self.status = "Rejected"


        self.total_days_calculate()
        
        # Fetch Leave Quota for this employee and leave type
        leave_quota = frappe.get_doc("Leave Quota", {
            "employee": self.employee,
            "leave_type": self.leave_type
        })
        if leave_quota.leave_balance < self.total_days:
            frappe.throw(f"Not enough leave balance for {self.leave_type}. You have {leave_quota.leave_balance} days left.")


    
    def on_change(self):
        if self.status == "Approved":
            frappe.msgprint("Leave Application is Approved")
            leave_quota = frappe.get_doc("Leave Quota", {
                "employee": self.employee,
                "leave_type": self.leave_type
            })

            if leave_quota:
                leave_quota.leave_taken += self.total_days
                leave_quota.leave_balance = leave_quota.maximum_allowed - leave_quota.leave_taken
                leave_quota.save()

