from django.core.management.base import BaseCommand
import asyncio
from testapp.tests import main

class Command(BaseCommand):
    help="run the playwright test and save the test data in the database"
    
    def handle(self,*args,**options):
    
      # results1=asyncio.run(step1())
      # self.stdout.write(f"successfully tested  Step 1 and stored in database!")
      # results2=asyncio.run(step2())
      # self.stdout.write(f"successfully tested  Step 2 and stored in database!")

      # results3=asyncio.run(step3())
      # self.stdout.write(f"successfully tested  Step 3 and stored in database!")

      results4=asyncio.run(main())
      
      # results5=asyncio.run(step5())
      # self.stdout.write(f"successfully tested  Step5 and stored in database!")
      # save_test_data(Test01Model,results1)
      

  