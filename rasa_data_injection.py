import pandas as pd
import os

def data_injection(product_directory):
    try:
        current_directory = os.getcwd()
        data_directory = "data"
        product_directory = product_directory
        source_file = "data.xlsx"
        rasa_directory_name = "rasa"
        rasa_directory = os.path.join(current_directory, rasa_directory_name)
        data_file = os.path.join(current_directory, data_directory, product_directory, source_file)
        nlu_df = pd.read_excel(data_file, sheet_name=0)
        domain_df = pd.read_excel(data_file, sheet_name=1)
        columns_mapping = None
        nlu_columns = [column.replace(" ", "").strip().lower() for column in nlu_df.columns]
        domain_columns = [column.replace(" ", "").strip().lower() for column in domain_df.columns]

        if all(x in nlu_columns for x in domain_columns) and all(x in domain_columns for x in nlu_columns):
            columns_mapping = True
        else:
            columns_mapping = False

    except Exception as e:
        return False

    if columns_mapping == True:
        try:
            nlu_df.columns = nlu_columns
            domain_df.columns=domain_columns
            nlu_df = nlu_df.dropna(how='all')
            domain_df = domain_df.dropna(how='all')

            ##########  nlu.py #################
            nlu_yml = os.path.join(rasa_directory, 'data','nlu.yml')
            nlu = open(nlu_yml, "w", encoding="utf-8")
            nlu.write('''version: "3.1"\n\n''')
            nlu.write('''nlu:\n''')
            for column in nlu_df.columns:
                intent = f'- intent: {column}\n'
                nlu.write(intent)
                nlu.write("  examples: |\n")
                examples = [x.replace("\n", " ").strip() for x in nlu_df[column].to_list() if isinstance(x, str) and any(c.isalpha() for c in x)]
                for example in examples:
                    example = example.replace("\n", " ")
                    nlu.write(f"    - {example}\n")
                nlu.write("\n")
            nlu.close()

            ##########  domain.py #################
            domain_yml = os.path.join(rasa_directory, 'domain.yml')
            domain = open(domain_yml, "w", encoding="utf-8")
            domain.write('''version: "3.1"\n\n''')
            domain.write('''intents:\n''')
            for column in nlu_df.columns:
                domain.write(f'  - {column}\n')
            domain.write("\n")
            domain.write('''responses:''')
            domain.write("\n")
            for column in nlu_df.columns:
                responses = [x.strip() for x in domain_df[column].tolist() if isinstance(x, str) and any(c.isalpha() for c in x)]
                domain.write(f'''  utter_{column}:\n''')
                for response in responses:
                    response = response.replace("\n", " ")
                    response = response.replace(":", "..")
                    response = response.replace('"', "'")
                    domain.write(f'''  - text: "{response}"\n''')
                    domain.write("\n")
            domain.close()

            ##########  rules.py ################# 
            rules_yml = nlu_yml = os.path.join(rasa_directory, 'data','rules.yml')
            rules = open(rules_yml, "w", encoding="utf-8")
            rules.write('''version: "3.1"\n\n''')
            rules.write('''rules:\n''')
            rules.write("\n")
            for column in nlu_df.columns:
                rules.write(f'''- rule: {column.replace("_", " ")}\n''')
                rules.write('''  steps:\n''')
                rules.write(f'''  - intent: {column}\n''')
                rules.write(f'''  - action: utter_{column}\n''')
                rules.write("\n")
            rules.close()

            ##########  stories.py ################# 
            stories_yml = os.path.join(rasa_directory, 'data','stories.yml')
            stories = open(stories_yml, "w", encoding="utf-8")
            stories.write('''version: "3.1"\n\n''')
            stories.write('''stories:\n''')
            stories.write("\n")
            stories.close()
            return True
        
        except Exception as e:
            return False
    else:
        print("columns are different")
        return False
    

#data_injection(product_directory = "omail")