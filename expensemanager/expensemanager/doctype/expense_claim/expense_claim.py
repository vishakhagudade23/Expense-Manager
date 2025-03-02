# Copyright (c) 2024, Vishakha Gudade and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ExpenseClaim(Document):
	def validate(self):
		total = 0
		for expense in self.types:
			total += expense.amount 
		
		self.total_amount = total 


