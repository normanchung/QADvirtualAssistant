# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import datetime

from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

from .params import *

class ActionBuildURL(Action):

    def name(self) -> Text:
        return "action_build_url"
    
    def split_intent(self, intent):
        words = intent.split('_')
        return '_'.join(words[:1]), '_'.join(words[1:])

    def get_url_template(self, operation, object):
        params = action_map[operation]
        browseType, viewAction, viewMode = params["browseType"], params["viewAction"], params["viewMode"]
        meta_uri = meta_uri_map[object]
        return base_url + browseType + base_uri + meta_uri + viewAction + viewMode
    
    def get_from_to_times(self, time):
        """
        Returns start time & end time from the time entity extracted by duckling
        """
        info = time["additional_info"]["values"][0]
        if "from" in info:
            from_time = info["from"]["value"][:10]
            grain = info["from"]["grain"]
        else:
            from_time = info["value"][:10]
            grain = info["grain"]
        start_date = datetime.datetime.strptime(from_time, "%Y-%m-%d")
        end_date = start_date
        if "to" in info:
            to_time = info["to"]["value"][:10]
        else:
            if grain == "week":
                time_delta = datetime.timedelta(weeks=1)
                end_date = start_date + time_delta
            elif grain == "month":
                # https://stackoverflow.com/questions/42950/how-to-get-the-last-day-of-the-month
                # get close to the end of the month for any day, and add 4 days 'over'
                end_date = start_date.replace(day=28) + datetime.timedelta(days=4)
                # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
                end_date = end_date - datetime.timedelta(days=end_date.day)
            elif grain == "quarter":
                time_delta = datetime.timedelta(weeks=12)
                end_date = start_date + time_delta
            elif grain == "year":
                end_date = start_date.replace(day=31).replace(month=12)
            else:
                pass
            to_time = str(end_date)[:10]
        return from_time, to_time

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.tracker = tracker
        self.dispatcher = dispatcher
        self.response = ""

        intent = self.tracker.latest_message["intent"].get("name")
        if intent == "nlu_fallback":
            dispatcher.utter_message("Not sure what you meant there.")
            return
        operation, object = self.split_intent(intent)
        self.URL = self.get_url_template(operation, object)
        try:
            method = getattr(self, intent)
            method()
        except AttributeError as e:
            dispatcher.utter_message("Unrecognized intent: " + e)
            return []
        except KeyError as e:
            dispatcher.utter_message("Key Error: " + str(e))
            return []
        response = {
            "URL": self.URL
        }
        dispatcher.utter_message(text = "%s [URL](%s)" % (self.response, self.URL), json_message = response)
        return [AllSlotsReset()]
    
    def create_action_request(self):
        self.response = "Creating an action request: "
        # check if action has extra parameters
        if self.tracker.get_slot("contact_type"):
            contact_type_num = contact_num_map[self.tracker.get_slot("contact_type")]
            auto_fill = "&autoFill=contactType%%3d%s" % (contact_type_num)
            self.URL += auto_fill
        if self.tracker.get_slot("customer_id"):
            customer_id = self.tracker.get_slot("customer_id")[0]
            auto_fill = "&autoFill=contactCode%%3d%s" % (customer_id)
            self.URL += auto_fill

    def read_action_request(self):
        self.response = "Opening an action request: "
        # check if action has extra parameters
        time = next((e for e in self.tracker.latest_message["entities"] if e["entity"] == "time"), None)
        if time:
            from_time, to_time = self.get_from_to_times(time)
            auto_fill = "&filter=acr_mstr.acr_req_datetime,rg,%s,literal,%s,literal" % (from_time, to_time)
            self.URL += auto_fill
        if self.tracker.get_slot("action_request_id"):
            action_request_id = self.tracker.get_slot("action_request_id")
            self.URL += '&filter=acr_mstr.acr_nbr,eq,%s,literal' % (action_request_id)
        if self.tracker.get_slot("contact_type"):
            contact_type = self.tracker.get_slot("contact_type")
            auto_fill = '&filter=local_variables.local-var02,eq,%s,literal' % (contact_type)
            self.URL += auto_fill
        if self.tracker.get_slot("customer_id"):
            customer_id = self.tracker.get_slot("customer_id")[0]
            auto_fill = '&filter=acr_mstr.acr_con_code,eq,%s,literal' % (customer_id)
            self.URL += auto_fill
        
    def update_action_request(self):
        self.response = "Editing an action request: "
        # If action request ID is not specified, open action requests
        if self.tracker.get_slot("action_request_id"):
            action_request_id = self.tracker.get_slot("action_request_id")
            self.URL += '&filter=acr_mstr.acr_nbr,eq,%s,literal' % (action_request_id)
        else:
            self.read_action_request()
            return
        
        if self.tracker.get_slot("contact_type"):
            contact_type_num = contact_num_map[self.tracker.get_slot("contact_type")]
            auto_fill = "&autoFill=contactType%%3d%s" % (contact_type_num)
            self.URL += auto_fill
        if self.tracker.get_slot("customer_id"):
            customer_id = self.tracker.get_slot("customer_id")[0]
            auto_fill = "&autoFill=contactCode%%3d%s" % (customer_id)
            self.URL += auto_fill

    def delete_action_request(self):
        self.response = "Deleting an action request: "
        self.read_action_request()

    def create_sale_order(self):
        self.response = "Creating a sales order: "
        if self.tracker.get_slot("customer_id"):
            customer_ids = self.tracker.get_slot("customer_id")
            fields = self.tracker.get_slot("field")
            for i in range(len(customer_ids)):
                try:
                    auto_fill = "&autoFill=%sCustomerCode%%3d%s" % (fields[i], customer_ids[i])
                except (IndexError, TypeError):
                    auto_fill = "&autoFill=soldToCustomerCode%%3d%s" % (customer_ids[i])
                self.URL += auto_fill

    def read_sale_order(self):
        self.response = "Opening a sales order: "
        time = next((e for e in self.tracker.latest_message["entities"] if e["entity"] == "time"), None)
        if time:
            from_time, to_time = self.get_from_to_times(time)
            auto_fill = "&filter=so_mstr.so_ord_date,rg,%s,literal,%s,literal" % (from_time, to_time)
            self.URL += auto_fill
        
        if self.tracker.get_slot("field") and self.tracker.get_slot("customer_id"):
            customer_ids = self.tracker.get_slot("customer_id")
            fields = self.tracker.get_slot("field")
            for i in range(len(customer_ids)):
                try:
                    field = sale_order_filters[fields[i]]
                    auto_fill = "&filter=so_mstr.%s,eq,%s,literal" % (field, customer_ids[i])
                except (IndexError, TypeError):
                    auto_fill = "&filter=so_mstr.so_cust,eq,%s,literal" % (customer_ids[i])
                self.URL += auto_fill
        elif self.tracker.get_slot("sale_order_id"):
            sale_order_id = self.tracker.get_slot("sale_order_id")
            auto_fill = "&filter=so_mstr.so_nbr,eq,%s,literal" % (sale_order_id)
            self.URL += auto_fill

    def update_sale_order(self):
        self.response = "Editing a sales order: "
        # If sale order ID is not specified, open sale orders
        if self.tracker.get_slot("sale_order_id"):
            sale_order_id = self.tracker.get_slot("sale_order_id")
            self.URL += '&filter=so_mstr.so_nbr,eq,%s,literal' % (sale_order_id)
        else:
            self.read_sale_order()
            return
        if self.tracker.get_slot("field"):
            fields = self.tracker.get_slot("field")
            customer_ids = self.tracker.get_slot("customer_id")
            if len(fields) != len(customer_ids):
                self.dispatcher.utter_message("Invalid format for 'update_sale_order'")
                return
            for i in range(len(fields)):
                auto_fill = "&autoFill=%sCustomerCode%%3d%s" % (fields[i], customer_ids[i])
                self.URL += auto_fill
    
    def delete_sale_order(self):
        self.response = "Deleting a sales order: "
        self.read_sale_order()

    def read_inventory_detail(self):
        self.response = "Opening inventory detail: "
        if self.tracker.get_slot("number"):
            fields = self.tracker.get_slot("field")
            number = self.tracker.get_slot("number")
            try:
                field = inventory_detail_filters[fields[0]]
                auto_fill = "&filter=in_mstr.%s,eq,%s,literal" % (field, number)
            except (IndexError, TypeError):
                auto_fill = "&filter=in_mstr.in_part,eq,%s,literal" % (number)
            self.URL += auto_fill
            
    
    def update_inventory_detail(self):
        self.read_inventory_detail()
