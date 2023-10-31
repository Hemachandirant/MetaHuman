import openai
import json
import streamlit as st
from speech_func import Speech
from function_call import Functions_call


# create an object for the function_call class

function_call = Functions_call()


class response_function:
    @staticmethod
    def generate_response(input_text, conversation_history):
        try:
            intial_prompt = """
                As your IT Expert, I'm dedicated to resolving your technical issues. Please describe your problem in detail. 
                If I'm unable to provide an immediate solution, I'll offer to create a ServiceNow ticket for you. 
                You can also inquire about the status of an existing ticket. How can I assist you today?

                
                Response Handling:

                User Describes an Issue:

                The IT Expert provides a solution or requests more information if needed.

                User Agrees to Create a ServiceNow Ticket:

                The IT Expert generates a ServiceNow ticket for the user's issue.
                The IT Expert provides the user with the ticket number and any additional information.

                User Declines to Create a ServiceNow Ticket:

                The IT Expert continues to assist with the issue based on available knowledge.

                User Inquires About an Existing Ticket.

                """
            messages = [
                {
                    "role": "system",
                    "content": intial_prompt,
                },
            ]

            # summary = response_function.summarize_history(conversation_history)
            messages.extend(conversation_history)
            messages.append({"role": "user", "content": input_text})
            functions = [
                {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
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
                    "name": "send_email",
                    "description": "Send mail to the given email and subject",
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
                    "description": "Get the status of an incident using the incident number the incident number should be starts with INC and length should be 10 if it exceeds say give the correct incident number as a response",
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
                    "description": "A comment is a free-text field that allows users to add additional information to a incident. For example, when creating or updating an incident, users can add comments to provide more details about the issue or update the status of the incident1. Comments can also be used to provide ongoing commentary on how a task is progressing",
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
            ]

            # response = openai.Completion.create(
            #     engine="text-davinci-002",
            #     messages=messages,
            # )

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
                functions=functions,
                function_call="auto",
            )
            print(response)
            response_message = response["choices"][0]["message"]

            if response_message.get("function_call"):
                # Step 3: call the function
                # Note: the JSON response may not always be valid; be sure to handle errors
                available_functions = {
                    "get_current_weather": function_call.get_current_weather,
                    "send_email": function_call.send_email,
                    "get_recent_incidents_status": function_call.get_recent_incidents_status,
                    "service_now_ticket_creation": function_call.service_now_ticket_creation,
                    "get_incident_status_by_number": function_call.get_incident_status_by_number,
                    "add_comment_to_incident": function_call.add_comment_to_incident,
                }  # only one function in this example, but you can have multiple
                function_name = response_message["function_call"]["name"]
                function_to_call = available_functions[function_name]
                function_args = json.loads(response_message["function_call"]["arguments"])

                if function_name == "get_current_weather":
                    location = function_args.get("location")
                    function_response = function_to_call(location=location)
                elif function_name == "send_email":
                    to_email = function_args.get("to_email")
                    subject = function_args.get("subject")
                    content = function_args.get("content")
                    function_response = function_to_call(
                        to_email=to_email, subject=subject, content=content
                    )
                elif function_name == "service_now_ticket_creation":
                    short_description = function_args.get("short_description")
                    description = function_args.get("description")

                    function_response = function_to_call(
                        short_description=short_description, description=description
                    )
                elif function_name == "get_incident_status_by_number":
                    incident_number = function_args.get("incident_number")
                    function_response = function_to_call(incident_number=incident_number)

                elif function_name == "get_recent_incidents_status":
                    number_of_incidents = function_args.get("number_of_incidents")
                    function_response = function_to_call(
                        number_of_incidents=number_of_incidents
                    )

                elif function_name == "add_comment_to_incident":
                    comment = function_args.get("comment")
                    incident_number = function_args.get("incident_number")
                    function_response = function_to_call(
                        incident_number=incident_number, comment=comment
                    )
                # Step 4: send the info on the function call and function response to GPT
                messages.append(
                    response_message
                )  # extend conversation with assistant's reply
                messages.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response

                print(messages)
                second_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0613", messages=messages, max_tokens=100
                )
                second_response_text = (
                    second_response.choices[0].message["content"].replace('"', "")
                )  # get a new response from GPT where it can see the function response
                return second_response_text

            else:
                response_text = response.choices[0].message["content"].replace('"', "")
                return response_text
        

        except openai.error.Timeout as e:
            # Handle timeout error, e.g. retry or log
            print(f"OpenAI API request timed out: {e}")
            pass
        except openai.error.APIError as e:
            # Handle API error, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            pass
        except openai.error.APIConnectionError as e:
            # Handle connection error, e.g. check network or log
            print(f"OpenAI API request failed to connect: {e}")
            pass
        except openai.error.InvalidRequestError as e:
            # Handle invalid request error, e.g. validate parameters or log
            print(f"OpenAI API request was invalid: {e}")
            pass
        except openai.error.AuthenticationError as e:
            # Handle authentication error, e.g. check credentials or log
            print(f"OpenAI API request was not authorized: {e}")
            pass
        except openai.error.PermissionError as e:
            # Handle permission error, e.g. check scope or log
            print(f"OpenAI API request was not permitted: {e}")
            pass
        except openai.error.RateLimitError as e:
            # Handle rate limit error, e.g. wait or log
            print(f"OpenAI API request exceeded rate limit: {e}")
            pass

    # @staticmethod
    # def summarize_history(conversation_history):
    #     # Concatenate the conversation history into a single string
    #     conversation_text = "\n".join(
    #         [message["content"] for message in conversation_history]
    #     )

    #     # Use OpenAI ChatCompletion to generate a summary
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": "Summarize the following conversation:"},
    #             {"role": "user", "content": conversation_text},
    #         ],
    #         max_tokens=50,  # Adjust the max tokens as needed for desired summary length
    #         temperature=0.7,  # Adjust the temperature for response randomness
    #     )

    #     summary = response["choices"][0]["message"]["content"]

    #     return summary