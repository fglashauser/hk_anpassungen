function is_male(salutation) {
    return ["Herr", "Hr", "Hr.", "Mr", "Mr."].includes(salutation);
}

function get_salutation(frm, callback) {     
    if (frm.doc.contact_person != undefined) {
        frappe.db.get_doc('Contact', frm.doc.contact_person)
            .then(contact => {
                salutation = "Sehr geehrte";
                is_male(contact.salutation) ? salutation += "r Herr " : salutation += " Frau ";
                salutation += contact.last_name + ",<br>";
                callback(salutation);
            });
    }
    else {
        callback("Sehr geehrte Damen und Herren,<br>");
    }
}

/* 
 * ANGEBOT
 */
frappe.ui.form.on('Quotation', {
    onload(frm) {
        if (frm.doc.final_note == undefined) {
            frm.set_value('final_note',
                "Wir danken Ihnen herzlich für Ihre Anfrage und freuen uns auf die weitere Zusammenarbeit.<br><br>" +
                "Mit besten Grüßen<br>" +
                "Hanno Keppel & Team");
        }
    },
    contact_person(frm) {
        if (frm.doc.introduction == undefined) {
            get_salutation(frm, function(salutation) {
                frm.set_value('introduction', salutation +
                    "gerne unterbreiten wir Ihnen folgendes Angebot:");
            });
        }
    }
});

/* 
 * AUFTRAG
 */
frappe.ui.form.on('Sales Order', {
    onload(frm) {
        if (frm.doc.final_note == undefined) {
            frm.set_value('final_note',
                "Vielen Dank für Ihren Auftrag! Für Anmerkungen oder Fragen stehen wir gerne zur Verfügung.<br><br>" +
                "Mit besten Grüßen<br>" +
                "Hanno Keppel & Team");
        
        }
    },
    contact_person(frm) {
        if (frm.doc.introduction == undefined) {
            get_salutation(frm, function(salutation) {
                frm.set_value('introduction', salutation +
                    "hiermit bestätigen wir Ihren Auftrag über die folgenden Positionen:");
            });
        }
    }
});

/* 
 * RECHNUNG
 */
frappe.ui.form.on('Sales Invoice', {
    onload(frm) {
        if (frm.doc.final_note == undefined) {
            frm.set_value('final_note',
                "Vielen Dank für Ihren Auftrag! Für Anmerkungen oder Fragen stehen wir gerne zur Verfügung.<br><br>" +
                "Mit besten Grüßen<br>" +
                "Hanno Keppel & Team");
        
        }
    },
    contact_person(frm) {
        if (frm.doc.introduction == undefined) {
            get_salutation(frm, function(salutation) {
                frm.set_value('introduction', salutation +
                    "vielen Dank für Ihren Auftrag! Wir erlauben uns, unsere Leistungen wie folgt in Rechnung zu stellen:");
            });
        }
    }
});