import openai
import json
import os
import streamlit as st
from speech_func import Speech
from function_definition import functions
from function_call import Functions_call



# create an object for the function_call class

function_call = Functions_call()


# openai.api_key = "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"

class response_function_azure:
    @staticmethod
    def generate_response_azure(input_text, conversation_history):
        try:
            intial_prompt = f"""
                    You are the IT Expert, dedicated to resolving technical issues.You will get description of problem user
                    and will provide step-by-step solution, providing first step in begining and once you user confirms he/she have completed that provide the next step. 
                    If I can't solve it immediately, I'll offer to create a ServiceNow ticket. 
                    You can also inquire about an existing ticket.
                    And Don't use the sentence "as an AI Language Model" in reponse.
                    Ensure that the response you provide is not more than 40 words and response which you are given should be in {st.session_state.language_name} Language"
                    Response Handling:
                    - User Describes an Issue: I'll provide a step-by-step solution and wait for you to complete each step, starting with the first.
                    - User Agrees to Create a Ticket: I'll generate a ServiceNow ticket with a number and details.
                    - User Declines Ticket: I'll continue to assist with available knowledge.

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

            # response = openai.Completion.create(
            #     engine="text-davinci-002",
            #     messages=messages,
            # )

            #Note: The openai-python library support for Azure OpenAI is in preview.
            openai.api_type = "azure"
            openai.api_base = "https://dwspoc.openai.azure.com/"
            openai.api_version = "2023-07-01-preview"
            openai.api_key = "bd38ee31e244408cacab3e1dd4c32221"

            response = openai.ChatCompletion.create(
                    engine="GPT4",
                    messages = messages,
                    functions = functions,
                    function_call="auto", 
                    temperature=0.7,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None
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
                    "time_delay": function_call.time_delay,
                    "get_incident_status_by_number": function_call.get_incident_status_by_number,
                    "add_comment_to_incident": function_call.add_comment_to_incident,
                    "end_conversation": function_call.end_conversation,
                }  # only one function in this example, but you can have multiple
                function_name = response_message["function_call"]["name"]

                if function_name in available_functions:
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(
                        response_message["function_call"]["arguments"]
                    )
                    function_response = function_to_call(**function_args)

                    # Step 4: send the info on the function call and function response to GPT
                    messages.append(
                        {
                            "role": response_message["role"],
                            "function_call": {
                                "name": response_message["function_call"]["name"],
                                "arguments": response_message["function_call"]["arguments"],
                            },
                            "content": None
                        }
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
                            engine="GPT4",
                            messages = messages,
                            temperature=0.7,
                            top_p=0.95,
                            frequency_penalty=0,
                            presence_penalty=0,
                            stop=None
                    )

                    second_response_text = (
                        second_response.choices[0].message["content"].replace('"', "")
                    )
                    # get a new response from GPT where it can see the function response
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

    #     second_response = response.choices[0].message["content"]
                    #     response_message += response_text[-1]  # Append the last character

                    # # Update the user interface with the new response letter by letter
                    #     st.text(response_message + "▌")

                    # message_placeholder = st.empty()
                    # second_response_message = ""
                    # for response in openai.ChatCompletion.create(
                    #     model="gpt-3.5-turbo-0613",
                    #     messages=messages,
                    #     max_tokens=100,
                    #     stream=True,
                    # ):
                    #     if 'choices' in response and len(response.choices) > 0 and 'message' in response.choices[0]:
                    #         response_text = response.choices[0].message["content"]
                    #         second_response_message += response_text[-1]

                    #         # Update the user interface with the new response letter by letter
                    #         message_placeholder.text(second_response_message + "▌")