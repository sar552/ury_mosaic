import json

import frappe
from ury.ury_pos.api import getBranch


# Function to set order status in a KOT document
@frappe.whitelist()
def serve_kot(name, time):
    frappe.db.set_value("URY KOT", name, "start_time_serv", time)
    frappe.db.set_value("URY KOT", name, "order_status", "Served")


# Function to mark it as verified by a user in cancel type KOT
@frappe.whitelist()
def confirm_cancel_kot(name, user):
    frappe.db.set_value("URY KOT", name, "verified", 1)
    frappe.db.set_value("URY KOT", name, "verified_by", user)


# Function to reject/decline a new order
@frappe.whitelist()
def reject_kot(name, user):
    try:
        # Get KOT document
        kot_doc = frappe.get_doc("URY KOT", name)
        
        # Update KOT status first
        kot_doc.order_status = "Rejected"
        kot_doc.verified = 1
        kot_doc.verified_by = user
        kot_doc.save(ignore_permissions=True)
        frappe.db.commit()
        
        # Cancel the associated POS Invoice if exists
        if kot_doc.invoice:
            try:
                # POS Invoice, not Sales Invoice
                invoice_doc = frappe.get_doc("POS Invoice", kot_doc.invoice)
                
                # Check if invoice is submitted
                if invoice_doc.docstatus == 1:
                    # Set flags to bypass certain validations if needed
                    invoice_doc.flags.ignore_permissions = True
                    
                    # Cancel the POS invoice
                    invoice_doc.cancel()
                    frappe.db.commit()
                    
                    frappe.logger().info(f"POS Invoice {kot_doc.invoice} cancelled for rejected KOT {name}")
                elif invoice_doc.docstatus == 0:
                    # If draft, just delete it
                    frappe.delete_doc("POS Invoice", kot_doc.invoice, ignore_permissions=True)
                    frappe.db.commit()
                    frappe.logger().info(f"Draft POS Invoice {kot_doc.invoice} deleted for rejected KOT {name}")
                    
            except Exception as e:
                error_msg = f"Error processing POS Invoice {kot_doc.invoice} for KOT {name}: {str(e)}"
                frappe.log_error(error_msg, "KOT Rejection - POS Invoice Error")
                # Continue even if invoice cancellation fails
                pass
        
        return {
            "status": "success", 
            "message": f"Order {name} rejected successfully",
            "invoice_cancelled": bool(kot_doc.invoice)
        }
    except Exception as e:
        error_msg = f"Error rejecting KOT {name}: {str(e)}"
        frappe.log_error(error_msg, "KOT Rejection Error")
        return {
            "status": "error",
            "message": error_msg
        }


@frappe.whitelist()
def kot_list():
    today = frappe.utils.now()
    branch = getBranch()
    kot_alert_time = frappe.db.get_value(
        "POS Profile", {"branch": branch}, "custom_kot_warning_time"
    )
    three_hours_ago = frappe.utils.add_to_date(today, hours=-3)
    audio_alert = frappe.db.get_value(
        "POS Profile", {"branch": branch}, "custom_kot_alert"
    )
    kotList = frappe.get_list(
        "URY KOT",
        fields=["name"],
        filters={
            "order_status": "Ready For Prepare",
            "branch": branch,
            "type": [
                "in",
                [
                    "New Order",
                    "Order Modified",
                    "Duplicate",
                    "Cancelled",
                    "Partially cancelled",
                ],
            ],
            "docstatus": 1,
            "verified": 0,
            "creation": (">=", three_hours_ago),
        },
        order_by="creation desc",
    )
    KOT = []
    for kot in kotList:
        kotdoc = frappe.get_doc("URY KOT", kot.name)
        kotjson = json.loads(frappe.as_json(kotdoc))
        KOT.append(kotjson)
    return {
        "KOT": KOT,
        "Branch": branch,
        "kot_alert_time": kot_alert_time,
        "audio_alert": audio_alert
    }

