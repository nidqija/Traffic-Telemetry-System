import sqlite3
import os
from .base_factory import AiAgent





class CloudflareWorkerFactory(AiAgent):

    def init(self):
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        





    

    


    

        
