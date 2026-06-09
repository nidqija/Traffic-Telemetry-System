from .base_factory import AiAgent
import ollama
import sqlite3

class OllamaFactory(AiAgent):
    def __init__(self, model_name: str = "gemma3:1b"):
        self.model_name = model_name


    def ask_questions(self , question:str) -> tuple[list , list] | str:

        system_instructions = f"""
          
           You are an SQL expert and data analyst. You have access to a database with the following schema:
              {self.get_schema_context()}

            Given a user's natural language question, look at the schema and return ONLY the valid SQLite query. 
            Do not include any introductory text, markdown formatting, or backticks (e.g., do NOT wrap it in ```sql). 
            Just return the raw query string.
        """


        try :
            response = ollama.generate(self.model_name,
                                       system=system_instructions,
                                       prompt = question,
                                       options={"temperature": 0.2, "max_tokens": 200}
                                       )
            raw_sql = response.get("response" , "")
            generated_sql = self.clean_sql(raw_sql)

            # for debugging purposes , print the generated SQL query to command line
            print("Generated SQL Query:", generated_sql)


            conn = sqlite3.connect('traffic_data.db')
            cursor = conn.cursor()
            cursor.execute(generated_sql)
            results = cursor.fetchall()


            columns = [description[0] for description in cursor.description]
            conn.close()

            return results , columns

            
        
        except Exception as e:
            return f"Error generating SQL query: {e}"
        


    
        

    
                                       
    
    

