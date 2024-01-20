# Copyright (c) 2024, PC-Giga and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

@frappe.whitelist()
def set_custom_created_at(doc, method):
	"""
	Sets the custom_created_at field to the current datetime.
	"""
	from frappe.utils import now
	doc.custom_created_at = now()

class KeppelTools(Document):

	def get_config(self):
		"""
		Returns the Keppel-Tools configuration document.
		"""
		return frappe.get_single("Keppel-Tools")
	
	def get_lr_config(self):
		return frappe.get_single("LeadRebel Settings")

	def _update_lead_owners_job(self):
		for lead in frappe.get_all("Lead"):
			lead = frappe.get_doc("Lead", lead.name)
			lead.update({"lead_owner": self.get_config().lead_owner}).save()
		frappe.db.commit()

	@frappe.whitelist()
	def update_lead_owners(self):
		"""
		Updates the lead owners of all leads in the system.
		Uses the User set in the Keppel-Tools document.
		"""
		frappe.enqueue_doc(
			"Keppel-Tools",
			self.name,
			"_update_lead_owners_job",
			queue="long",
			timeout=5000
		)

	def _update_lead_dates_job(self):
		# WeClapp
		from weclapp_migration.weclapp.api import Api as WcApi
		from weclapp_migration.tools.data import get_datetime_from_weclapp_ts
		with WcApi() as api:
			for wc_lead in api.get_cache_objects("lead"):
				en_lead = next(iter(frappe.get_all("Lead", filters={"wc_id": wc_lead["id"]}, fields=["name"])), None)
				if en_lead:
					en_lead = frappe.get_doc("Lead", en_lead.name)
					en_lead.update({"custom_created_at": get_datetime_from_weclapp_ts(wc_lead["createdDate"])}).save()
		# LeadRebel
		for en_lead in frappe.get_all("Lead", filters={"source": self.get_lr_config().lead_source}, fields=["name"]):
			en_lead = frappe.get_doc("Lead", en_lead.name)
			en_lead.update({"custom_created_at": en_lead.creation}).save()
		frappe.db.commit()

	@frappe.whitelist()
	def update_lead_dates(self):
		"""
		Updates all migrated lead dates from WeClapp to custom field.
		Also updates LeadRebel imported leads.
		"""
		frappe.enqueue_doc(
			"Keppel-Tools",
			self.name,
			"_update_lead_dates_job",
			queue="long",
			timeout=5000
		)

	def _update_lr_qualification_status_job(self):
		config = frappe.get_single("LeadRebel Settings")
		for lead in frappe.get_all("Lead", filters={"source": config.lead_source}):
			lead = frappe.get_doc("Lead", lead.name)
			if lead.qualification_status != "Qualified":
				lead.update({"qualification_status": config.qualification_status}).save()
		frappe.db.commit()

	@frappe.whitelist()
	def update_lr_qualification_status(self):
		"""
		Updates the qualification status of all leads from LeadRebel in the system to configured status in LeadRebel Settings.
		"""
		frappe.enqueue_doc(
			"Keppel-Tools",
			self.name,
			"_update_lr_qualification_status_job",
			queue="long",
			timeout=5000
		)