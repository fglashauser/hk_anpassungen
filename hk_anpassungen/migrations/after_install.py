import frappe

@frappe.whitelist()
def execute():
    """
    Will be executed after installing the app.
    Changes values for the "type"-Field in Doctype "Lead".
    Changes values for the "qualification_status"-Field in Doctype "Lead".
    """
    lead_doctype = frappe.get_doc("DocType", "Lead")
    for field in lead_doctype.fields:
        if field.fieldname == "type":
            field.options = "\nClient\nLieferant\nModel"
        if field.fieldname == "qualification_status":
            field.options = "Unqualified\nVorqualifiziert\nQualified\nDisqualifiziert"
    lead_doctype.save()
    frappe.db.commit()