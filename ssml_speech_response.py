import os
import azure.cognitiveservices.speech as speechsdk

def convert_ssml_to_speech(ssml_text):
    subscription_key = "71b49f1e9a8f444e80a1a74d9b87b79c"
    region = "eastus"

    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

    speech_config.speech_synthesis_language = "en-NZ"
    speech_config.speech_synthesis_voice_name = "en-NZ-MollyNeural"
    
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = synthesizer.speak_ssml(ssml_text)

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # audio_data = result.audio_data
        # with open("output.wav", "wb") as audio_file:
        #     audio_file.write(audio_data)
        print("SSML converted to speech and saved as output.wav")
    else:
        print("Speech synthesis failed: {}".format(result.reason))

# Example SSML text
ssml_text = """
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
    <voice name='en-NZ-MollyNeural'><prosody rate="slow">I'm really sorry to hear that you're feeling unhappy about the functions not working properly.</prosody><break time="300ms"/><prosody volume="loud" rate="fast">Your feedback is important to us.</prosody>
    <break time="500ms"/><emphasis level="strong">We understand your frustration, and we are working hard to fix the issues.</emphasis><break time="500ms"/><prosody rate="slow">Please bear with us as we strive to resolve this situation as quickly as possible.</prosody></voice>
</speak>
"""

convert_ssml_to_speech(ssml_text)
