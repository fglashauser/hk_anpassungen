# Copyright (c) 2024, PC-Giga and contributors
# For license information, please see license.txt
#
# This files handles custom logic for ToDo doctype.

import frappe

def delete_done_todos():
    """
    Deletes all tasks that are marked as 'Closed' or 'Cancelled'.
    """
    tasks = frappe.get_all("ToDo", filters={"status": ["in", ["Closed", "Cancelled"]]})
    for task in tasks:
        frappe.delete_doc("ToDo", task.name)
    frappe.db.commit()