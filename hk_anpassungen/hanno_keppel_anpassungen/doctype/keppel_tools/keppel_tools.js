// Copyright (c) 2024, PC-Giga and contributors
// For license information, please see license.txt

frappe.ui.form.on("Keppel-Tools", {
	refresh(frm) {
        frm.page.add_menu_item(__("Update all Lead Owners"), function() {
            frm.call('update_lead_owners');
        });
        frm.page.add_menu_item(__("Update migrated Lead date"), function() {
            frm.call('update_lead_dates');
        });
        frm.page.add_menu_item(__("Feld-Migrationen (Install)"), function() {
            frappe.call("hk_anpassungen.migrations.after_install.execute");
        });
        frm.page.add_menu_item(__("Update Qualification Status"), function() {
            frm.call('update_lr_qualification_status');
        });
        frm.page.add_menu_item(__("Update HK Custom fields"), function() {
            frm.call('update_hk_custom_fields');
        });
        frm.page.add_menu_item(__("Update Lead/Customer City"), function() {
            frm.call('update_crm_city');
        });
        frm.page.add_menu_item(__("Update LeadRebel Source"), function() {
            frm.call('update_lr_source');
        });
        frm.page.add_menu_item(__("Update Sales Invoice Lead Source"), function() {
            frm.call('update_invoice_source');
        });
        frm.page.add_menu_item(__("Delete done ToDo's"), function() {
            frm.call('delete_done_todos');
        });
	}
});
