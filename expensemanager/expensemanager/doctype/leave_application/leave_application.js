// Copyright (c) 2024, Vishakha Gudade and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Leave Application", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Leave Application', {
    start_date: function(frm) {
        frm.trigger('calculate_total_days');
    },
    end_date: function(frm) {
        frm.trigger('calculate_total_days');
    },
    calculate_total_days: function(frm) {
        if (frm.doc.start_date && frm.doc.end_date) {
            // Calculate the difference between start_date and end_date
            var start = new Date(frm.doc.start_date);
            var end = new Date(frm.doc.end_date);
            var diff = (end - start) / (1000 * 60 * 60 * 24) + 1;  // Include both start and end

            // Set the total_days field
            frm.set_value('total_days', diff);
        }
    }
});
