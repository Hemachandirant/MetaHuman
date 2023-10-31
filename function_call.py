import requests
import json
import time
import streamlit as st
from requests.auth import HTTPBasicAuth




class Functions_call:
    @staticmethod
    def send_email(to_email, subject, content):
            # API URL
            url = "https://gray-repulsive-duck.cyclic.app/sendEmail"

            # Headers
            headers = {
                "Content-Type": "application/json",
            }

            # the request body with the provided values
            payload = {
                "to": to_email,
                "subject": subject,
                "content": content,
            }

            # Convert the payload to JSON
            json_payload = json.dumps(payload)

            # Send the POST request
            response = requests.post(url, headers=headers, data=json_payload)

            # Check the response status code
            if response.status_code == 200:
                return "Email sent successfully!"
            else:
                # return f"Failed to send email. Status code: {response.status_code}"
                return f"Failed to send email. Status code: please provide the write details"


    @staticmethod
    def get_current_weather(location):
        """Get the current weather in a given location"""

        url = f"https://open-weather13.p.rapidapi.com/city/{location}"

        headers = {
            "X-RapidAPI-Key": "27678da727mshb69f3fc5c4e5cf0p175e22jsnb10038e8caa6",
            "X-RapidAPI-Host": "open-weather13.p.rapidapi.com",
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Connection Error:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something went wrong:", err)

        weather_info = response.json()

        return json.dumps(weather_info)


    # # ServiceNow Ticket Creation
    # @staticmethod
    # def service_now_ticket_creation(short_description, description):
    #     """Create a new servicenow ticket"""

    #     auth = HTTPBasicAuth("adarsh.talinki@wipro.com", "Demo@1234")

    #     uri = "https://wiprodemo4.service-now.com/api/now/table/incident?sysparm_display_value=true"

    #     headers = {
    #         "Accept": "application/json;charset=utf-8",
    #         "Content-Type": "application/json",
    #     }

    #     # define payload for request, note we are passing the sysparm_action variable in the body of the request

    #     payload = {"short_description": short_description, "description": description}

    #     r = requests.post(
    #         url=uri, data=json.dumps(payload), auth=auth, verify=False, headers=headers
    #     )

    #     content = r.json()

    #     return json.dumps(content)

    @staticmethod
    def service_now_ticket_creation(short_description, description):
        """Create a new ServiceNow ticket"""

        auth = HTTPBasicAuth("adarsh.talinki@wipro.com", "Demo@1234")

        uri = "https://wiprodemo4.service-now.com/api/now/table/incident?sysparm_display_value=true"

        headers = {
            "Accept": "application/json;charset=utf-8",
            "Content-Type": "application/json",
        }

        # define payload for request, note we are passing the sysparm_action variable in the body of the request

        payload = {"short_description": short_description, "description": description}

        try:
            r = requests.post(
                url=uri, data=json.dumps(payload), auth=auth, verify=False, headers=headers
            )
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            return json.dumps({"error": {"message": str(errh)}})
        except requests.exceptions.ConnectionError as errc:
            return json.dumps({"error": {"message": str(errc)}})
        except requests.exceptions.Timeout as errt:
            return json.dumps({"error": {"message": str(errt)}})
        except requests.exceptions.RequestException as err:
            return json.dumps({"error": {"message": str(err)}})

        content = r.json()

        return json.dumps(content)


        # ServiceNow Ticket Creation
    @staticmethod
    def get_incident_status_by_number(incident_number):
        try:
            # Check if the incident_number meets the validation criteria
            if incident_number.startswith("INC") and len(incident_number) == 10:
                auth = HTTPBasicAuth("adarsh.talinki@wipro.com", "Demo@1234")

                uri = f"https://wiprodemo4.service-now.com/api/now/table/incident?sysparm_query=numberLIKE{incident_number}^ORDERBYDESCsys_created_on&sysparm_display_value=true"

                headers = {
                    "Accept": "application/json;charset=utf-8",
                    "Content-Type": "application/json",
                }

                r = requests.get(url=uri, auth=auth, verify=False, headers=headers)

                # Check if the response status code indicates success (201 or 2xx)
                if r.status_code == 201 or (r.status_code >= 200 and r.status_code < 300):
                    content = r.json()
                    return json.dumps(content)
                else:
                    return f"Failed to retrieve incident status. Status code: {r.status_code}"
            else:
                return "Please enter a valid incident number starting with 'INC' and having exactly 10 characters."
        except Exception as e:
            return f"An error occurred: {str(e)}"



    @staticmethod
    def get_recent_incidents_status(number_of_incidents):
        auth = HTTPBasicAuth("adarsh.talinki@wipro.com", "Demo@1234")

        uri = f"https://wiprodemo4.service-now.com/api/now/table/incident?sysparm_query=sys_created_bySTARTSWITHadarsh^ORDERBYDESCsys_updated_on^active=true&sysparm_limit={number_of_incidents}"
        headers = {
            "Accept": "application/json;charset=utf-8",
            "Content-Type": "application/json",
        }

        # # define payload for request, note we are passing the sysparm_action variable in the body of the request

        # payload = {

        #     "short_description": "Monitor issue55",

        #     "description": "Display blackout55"

        # }

        r = requests.get(url=uri, auth=auth, verify=False, headers=headers)

        content = r.json()

        incidents = []
        for incident in content["result"]:
            status = incident["state"]
            incident_number = incident["number"]
            short_description = incident["short_description"]
            comments = incident["comments"]
            description = incident["description"]
            sys_id = incident["sys_id"]

            # Storing the extracted fields in a dictionary
            incident_dict = {
                "status": status,
                "incident_number": incident_number,
                "short_description": short_description,
                "comments": comments,
                "description": description,
                "sys_id": sys_id,
            }

            # Adding the dictionary to a list of incidents
            incidents.append(incident_dict)

        #   "sys_updated_on": "2021-01-21 07:53:57",
        #   "number": "INC0063510",
        #   "state": "1",
        #   "sys_created_by": "adarshs@wiprolabs.com",
        #   "knowledge": "false",
        #   "impact": "3",
        #   "active": "true",
        #   "priority": "5",
        #   "sys_domain_path": "/",
        #   "short_description": "Testing",
        #   "made_sla": "true",
        #   "task_effective_number": "INC0063510",
        #   "sys_updated_by": "adarshs@wiprolabs.com",
        #   "sys_created_on": "2021-01-21 07:53:57",
        #   "sys_domain": {
        #     "link": "https://wiprodemo4.service-now.com/api/now/table/sys_user_group/global",
        #     "value": "global"
        #   },
        #   "opened_at": "2021-01-21 07:53:33",
        #   "incident_state": "1",
        #   "urgency": "3",
        #   "severity": "3",
        #   "category": "inquiry"

        print("Response Status Code: " + str(content))

        return json.dumps(incidents)

    @staticmethod
    def add_comment_to_incident(incident_number, comment):
        content1 = Functions_call.get_incident_status_by_number(incident_number)
        
        content=json.loads(content1)

        status = content["result"][0]["state"]
        incident_number = content["result"][0]["number"]
        short_description = content["result"][0]["short_description"]
        comments = content["result"][0]["comments"]
        description = content["result"][0]["description"]
        sys_id = content["result"][0]["sys_id"]

        auth = HTTPBasicAuth("adarsh.talinki@wipro.com", "Demo@1234")
        uri = f"https://wiprodemo4.service-now.com/api/now/table/incident/{sys_id}?sysparm_display_value=true"
        headers = {
            "Accept": "application/json;charset=utf-8",
            "Content-Type": "application/json",
        }
        payload = {
            # "comments_and_work_notes": comment,
            "comments": comment
        }
        r = requests.patch(
            url=uri, auth=auth, verify=False, headers=headers, json=payload
        )
        content = r.json()
        print("Response Status Code: " + str(content))
        return json.dumps(content)
    
    @staticmethod
    def end_conversation(feedback):
        st.session_state.should_exit = False
        # st.session_state.
        return "Thank you for your feedback." + feedback

    @staticmethod
    def time_delay(time):
        time.sleep(5)
        return "Ok have you completed now"


