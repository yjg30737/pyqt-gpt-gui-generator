import os, sys

from openai import OpenAI

import importlib

def load_and_instantiate_class(module_name, class_name=None):
    # Load module dynamically
    if module_name in sys.modules:
        del sys.modules[module_name]
    module = importlib.import_module(module_name)

    # Find first class in the module if there is no explicit class name given
    if class_name is None:
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type):  # Is obj class
                class_name = name
                break

    # Instantiate
    if class_name is not None:
        return getattr(module, class_name)()
    else:
        raise ValueError("There is not a single class in module.")


PROMPT = '''
Context (C): You're an expert in PyQt5 GUI development tasked with generating source code for various GUI applications.

Objective (O): Your task is to provide the complete Python source code for a PyQt5 GUI application specified by the user. The code should be ready to run, assuming PyQt5 is already installed.

Style (S): The style of the response should be direct and to the point, focusing solely on the Python code necessary to implement the described GUI functionality.

Tone (T): The tone should be neutral, as the response will be purely code.

Audience (A): The intended audience is developers or programmers with some familiarity with Python and PyQt5, looking to quickly integrate or study the provided code.

Response Format (R): The format of the response must be a block of Python source code without any additional text before or after it. You MUST NOT include package installation commands or environmental setup instructions.

Generate the Python source code for a PyQt5 GUI application according to the specifications provided. The code should assume PyQt5 is installed and be ready to run as is. Include all necessary imports, class definitions, and event handling required to fulfill the application's intended functionality. You will be penalized for including any explanatory text outside the code or installation instructions.

specifications: {}
'''

class GPTJsonWrapper:
    def __init__(self, api_key=None):
        super().__init__()
        # Initialize OpenAI client
        if api_key:
            self.__client = OpenAI(api_key=api_key)
        self.__prompt = ''

    def set_api(self, api_key):
        self.__api_key = api_key
        self.__client = OpenAI(api_key=api_key)

    def get_data(self, query):
        module_name = 'result'
        filename = f'{module_name}.py'
        if os.path.exists(filename):
            os.remove(filename)

        prompt = PROMPT.format(query)
        data = self.get_response(query=prompt)

        data = '\n'.join(data.split('\n')[1:-1])
        with open(filename, 'w') as f:
            f.write(data)
        return module_name

    def get_response(
        self,
        model="gpt-4-0125-preview",
        n=1,
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format="text",
        objective: dict = {},
        query: str = '',
        stream=False,
    ):
        if response_format == 'text':
            pass
        else:
            query = objective["query"] + " " + str(objective["json_format"])
        try:
            openai_arg = {
                "model": model,
                "messages": [],
                "n": n,
                "temperature": temperature,
                "top_p": top_p,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
                "stream": stream,
                "response_format": {"type": response_format},
            }

            openai_arg["messages"].append({"role": "user", "content": query})

            response = self.__client.chat.completions.create(**openai_arg)
            response_content = response.choices[0].message.content

            return response_content
        except Exception as e:
            print(e)

# for test
# wrapper = GPTJsonWrapper(api_key='')
# prompt = PROMPT.format('QWidget which can show the three button named from "Alexander1" to "Alexander3" vertically. Background photo is a.png.')
# for i in range(3):
#     data = wrapper.get_response(query=prompt)
#     data = '\n'.join(data.split('\n')[1:-1])
#     with open(f'a{i}.py', 'w') as f:
#         f.write(data)
