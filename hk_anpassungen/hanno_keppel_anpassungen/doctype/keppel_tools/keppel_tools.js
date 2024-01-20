// Copyright (c) 2024, PC-Giga and contributors
// For license information, please see license.txt

frappe.ui.form.on("Keppel-Tools", {
	refresh(frm) {
        frm.add_custom_button(__("Update all Lead Owners"), function() {
            frm.call('update_lead_owners');
        });
        frm.add_custom_button(__("Update migrated Lead date"), function() {
            frm.call('update_lead_dates');
        });
        frm.add_custom_button(__("Feld-Migrationen (Install)"), function() {
            frappe.call("hk_anpassungen.migrations.after_install.execute");
        });
        frm.add_custom_button(__("Update Qualification Status"), function() {
            frm.call('update_lr_qualification_status');
        });
	}
});
