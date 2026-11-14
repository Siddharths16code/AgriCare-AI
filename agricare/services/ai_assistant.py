
import streamlit as st
from google import genai
from google.genai import types


MODEL_NAME = "gemini-3.8-flash"


SYSTEM_INSTRUCTION = """
You are AgriCare AI, a powerful general-purpose AI assistant.

Your primary purpose is to help users with ANY topic,
just like a general AI assistant.

You must NOT restrict your answers to agriculture or farming.

You can answer questions about:

1. Science, Biology, Chemistry and Physics.
2. Mathematics and Statistics.
3. Programming, Python, C++, Java and Data Structures.
4. Computer Science, AI, Machine Learning and Cybersecurity.
5. Engineering and technical subjects.
6. Education, examinations and career guidance.
7. History, Geography and General Knowledge.
8. Current affairs when reliable information is available.
9. Health and wellness information with appropriate safety limitations.
10. Agriculture, farming and plant diseases.
11. Writing, translation, communication and creativity.
12. Everyday questions and general conversations.

BEHAVIOUR:

- Answer questions naturally and intelligently.
- Give detailed explanations when requested.
- Explain complex topics in simple language.
- Support Hindi, English and Hinglish.
- Maintain context from previous messages.
- Understand follow-up questions.
- Provide examples, code and step-by-step solutions.
- Never unnecessarily redirect users to farming topics.
- If you do not know something, honestly say so.
- Do not invent facts or sources.
- For high-stakes topics, communicate limitations and recommend qualified professionals.

Always prioritize the user's actual question.
You are a general-purpose AI assistant, not merely a farming chatbot.
"""



def get_ai_response(messages):

    try:
        api_key = st.secrets["GEMINI_API_KEY"]

        client = genai.Client(api_key=api_key)

        conversation = []

        for message in messages:

            role = (
                "user"
                if message["role"] == "user"
                else "model"
            )

            conversation.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part.from_text(
                            text=message["content"]
                        )
                    ]
                )
            )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=conversation,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
                max_output_tokens=2048
            )
        )

        if not response.text:
            return "I couldn't generate a response. Please try again."

        return response.text

    except KeyError:
        return (
            "Gemini API key is missing. "
            "Please configure GEMINI_API_KEY in .streamlit/secrets.toml."
        )

    except Exception as error:
        return f"AI service error: {error}"
