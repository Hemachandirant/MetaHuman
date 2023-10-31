functions = [
                {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location ask for location if not mentioned",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA, Bangalore",
                            },
                            "unit": {"type": "string", "enum": ["celsius"]},
                        },
                        "required": ["location"],
                    },
                },
                {
                    "name": "time_delay",
                    "description": "Time delay is used to delay something. If user says give me sometime or give me second",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "time": {
                                "type": "string",
                                "description": "The seconds and minutes, e.g. give me a second eg: 10 , give me seconds eg: 20 ",
                            },
                        },
                        "required": ["time"],
                    },
                },
                {
                    "name": "send_email",
                    "description": "Send mail to the given email and subject. ask for email and subject if not mentioned",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "to_email": {
                                "type": "string",
                                "description": "The email or gmail,  e.g. balaji@gmail.com, abhijeet@wipro.com",
                            },
                            "subject": {
                                "type": "string",
                                "description": "Subject of the email or gmail, e.g. Can you fix meet today, What is the status of the task",
                            },
                            "content": {
                                "type": "string",
                                "description": "Content of the email or gmail, e.g. Dear Subscriber, We are excited to introduce our monthly newsletter, where you'll discover the latest updates, news, and exclusive offers from our company.",
                            },
                        },
                        "required": ["to_email", "subject", "content"],
                    },
                },
                {
                    "name": "service_now_ticket_creation",
                    "description": "Create a ServiceNow ticket with the given short description and description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "short_description": {
                                "type": "string",
                                "description": "A brief summary of the ticket",
                            },
                            "description": {
                                "type": "string",
                                "description": "Detailed information about the ticket",
                            },
                        },
                        "required": ["short_description", "description"],
                    },
                },
                {
                    "name": "get_incident_status_by_number",
                    "description": "Get the status of an incident using the incident number the incident number should be starts with INC and length should be 10 if it exceeds say give the correct incident number as a response.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "incident_number": {
                                "type": "string",
                                "description": "The unique identifier of the incident, e.g. INC0001234",
                            }
                        },
                        "required": ["incident_number"],
                    },
                },
                {
                    "name": "get_recent_incidents_status",
                    "description": "Get the recent incidents status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "number_of_incidents": {
                                "type": "string",
                                "description": "Number of incidents needs to showup. e.g. 2",
                            }
                        },
                        "required": ["number_of_incidents"],
                    },
                },
                {
                    "name": "add_comment_to_incident",
                    "description": "A comment is a free-text field that allows users to add additional information to a incident. For example, when creating or updating an incident, users can add comments to provide more details about the issue or update the status of the incident1. Always ask the user for comments",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "incident_number": {
                                "type": "string",
                                "description": "The unique identifier of the incident, e.g. INC0001234",
                            },
                            "comment": {
                                "type": "string",
                                "description": "Adding comments to the incident, e.g. i am unable to login",
                            },
                        },
                        "required": ["incident_number", "comments"],
                    },
                },
                {
                "name": "end_conversation",
                "description": "Ends the conversation once you get the feedback if user not mention ask user for feedback",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "feedback": {
                            "type": "string",
                            "description": "The user's feedback. eg. you done a good job and exit conversation"
                        }
                    },
                }
            }

            ]