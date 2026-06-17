import sqlite3
import os
from .base_factory import AiAgent
import requests
import dotenv

dotenv.load_dotenv()  # Load environment variables from .env filenv file


class CloudflareWorkerFactory(AiAgent):

    def __init__(self, model_name: str = "@cf/meta/llama-3.2-3b-instruct"):
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        self.model_name = model_name

        if not self.account_id or not self.api_token:
            raise ValueError("CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN must be set in environment variables.")

    def ask_questions(self, question: str) -> tuple[list, list] | str:
        system_instructions = f"""
            You are an SQL expert and data analyst. You have access to a database with the following schema:
               {self.get_schema_context()}

            Given a user's natural language question, look at the schema and return ONLY the valid SQLite query. 
            Do not include any introductory text, markdown formatting, or backticks (e.g., do NOT wrap it in ```sql). 
            Just return the raw query string.
        """
        
        # FIX: Cleaned up the URL string so it's a normal single API endpoint string
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model_name}"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "messages": [
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": question}
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()

            result_json = response.json()

            if not result_json or "result" not in result_json or "response" not in result_json["result"]:
                raise ValueError("Invalid response structural schema.")
            
            raw_sql = result_json.get("result", {}).get("response", "")

            print("Cloudflare connection test response:", result_json)  # Debugging
            print("Raw SQL from Cloudflare:", raw_sql)                  # Debugging

            generated_sql = self.clean_sql(raw_sql)
            print("Generated SQL Query:", generated_sql)                # Debugging

            conn = sqlite3.connect('traffic_data.db')
            cursor = conn.cursor()
            cursor.execute(generated_sql)
            results = cursor.fetchall()
            print("Query Results:", results)                            # Debugging

            columns = [description[0] for description in cursor.description]
            conn.close()

            return results, columns
        
        # FIX: Catch both network failures AND our structural JSON ValueError
        except (requests.exceptions.RequestException, ValueError) as e:
            return f"Error processing query: {e}"