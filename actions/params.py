# base url + browse type + base uri + meta uri + view action + view mode + extras (i.e. filters, view modes)
base_url = "https://qvarfrdlwb01.qad.com/clouderp/#/"
base_uri = "?viewMetaUri=urn:view:meta:com.qad.erp."

action_map = {
    "create": {
        "browseType": "view/qraview/hybridbrowse",
        "viewAction": "&viewAction=CREATE",
        "viewMode": "&hybridMode=maint",
    },
    "read": {
        "browseType": "view/qracore/browses/list",
        "viewAction": "",
        "viewMode": "&hybridMode=browse",
    },
    "update": {
        "browseType": "view/qraview/hybridbrowse",
        "viewAction": "&viewAction=UPDATE",
        "viewMode": "&hybridMode=hybrid",
    },
    "delete": {
        "browseType": "view/qraview/hybridbrowse",
        "viewAction": "&viewAction=DELETE",
        "viewMode": "&hybridMode=hybrid",
    }
}

contact_num_map = {
    "customer": '1',
    "end user": '2',
    "supplier": '3',
    "employee": '4',
    "salesper": '5',
    "engineer": '6',
    "other"   : '7',
    "crm acco": '8'
}

sale_order_filters = {
    "soldTo": "so_cust",
    "shipTo": "so_ship",
    "billTo": "so_bill"
}

inventory_detail_filters = {
    "item": "in_part"
}

meta_uri_map = {
    "sale_order": "sales.salesOrders",
    "inventory_detail": "inventory.inventoryDetails",
    "action_request": "service.actionRequests",
    "customer": "base.customers"
}
