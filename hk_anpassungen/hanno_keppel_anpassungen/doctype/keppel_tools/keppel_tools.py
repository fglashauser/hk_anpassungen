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

@frappe.whitelist()
def update_lead_city(doc, method):
	"""
	Updates the City field of the lead to the City field of the address.
	"""
	addr = next(iter(frappe.get_all("Address", filters={"link_doctype": "Lead", "link_name": doc.name}, fields=["city"])), None)
	if addr:
		doc.city = addr.city

@frappe.whitelist()
def update_customer_city(doc, method):
	"""
	Updates the City field of the customer to the City field of the address.
	"""
	if doc.customer_primary_address:
		addr = frappe.get_doc("Address", doc.customer_primary_address)
		doc.city = addr.city

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

	def _update_hk_custom_fields_job(self):
		for lead in frappe.get_all("Lead"):
			lead = frappe.get_doc("Lead", lead.name)
			if lead.type == "Client":
				lead.update({"hk_type": "Client"})
			if lead.qualification_status == "Qualified" or lead.qualification_status == "Unqualified":
				lead.update({"hk_qualification": lead.qualification_status})
			lead.save()
		frappe.db.commit()
		print("+++++++ Updated HK Lead-Type and HK Qualification for all leads.")

	@frappe.whitelist()
	def update_hk_custom_fields(self):
		"""
		Updates HK Lead-Type and HK Qualification fields for all leads in the system.
		"""
		frappe.enqueue_doc(
			"Keppel-Tools",
			self.name,
			"_update_hk_custom_fields_job",
			queue="long",
			timeout=5000
		)

	def _update_crm_city_job(self):
		for lead in frappe.get_all("Lead"):
			lead = frappe.get_doc("Lead", lead.name)
			addr = next(iter(frappe.get_all("Address", filters={"link_doctype": "Lead", "link_name": lead.name}, fields=["city"])), None)
			if addr:
				lead.update({"city": addr.city})
				lead.save()
		print("+++++++ Updated City for all leads.")
		for cust in frappe.get_all("Customer"):
			cust = frappe.get_doc("Customer", cust.name)
			if cust.customer_primary_address:
				addr = frappe.get_doc("Address", cust.customer_primary_address)
				cust.update({"city": addr.city})
				cust.save()
		frappe.db.commit()
		print("+++++++ Updated City for all customers.")

	@frappe.whitelist()
	def update_crm_city(self):
		"""
		Updates the City field for all leads and customers in the system.
		"""
		frappe.enqueue_doc(
			"Keppel-Tools",
			self.name,
			"_update_crm_city_job",
			queue="long",
			timeout=5000
		)
		