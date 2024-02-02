"""
WARNING:

Please make sure you install the bot with `pip install -e .` in order to get all the dependencies
on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the bot.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install --upgrade -r requirements.txt`
- Use the same interpreter as the one used to install the bot (`pip install --upgrade -r requirements.txt`)

Please refer to the documentation for more information at https://documentation.botcity.dev/
"""


# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Importando pandas
import pandas as pd

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    # Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()

    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to change the default Browser to Firefox
    bot.browser = Browser.CHROME

    # Uncomment to set the WebDriver path
    bot.driver_path = "C:\chromedriver-win64\chromedriver.exe"

    data = pd.read_excel(r"C:\Users\gustavo.ferreira\Downloads\EmployeesFeedback.xlsx")

    print(data)

    # Opens the BotCity website.
    bot.browse("https://forms.gle/m6fkxAnhkth3EbUB7")

    # Wait 2 seconds before closing
    bot.wait(2000)

    # Iterando pelos elementos do forms
    for index, row in data.iterrows():
        # utilizando a padrão de busca XPATH para localizar os elementos do formulário
        employee_name_field = bot.find_element("//div[contains(@data-params, 'Employee name')]//input[@type='text']", By.XPATH) 
        employee_name_field.send_keys(row['Employee Name'])

        bot.wait(500)

        years_of_service_field = bot.find_element("//div[contains(@data-params, 'Years of Service')]//input[@type='text']", By.XPATH) 
        years_of_service_field.send_keys(row['Years of Service'])

        bot.wait(500)

        department_field = bot.find_element("//div[contains(@data-params,  'Department')]//div[contains(@role, 'listbox')]", By.XPATH) 
        department_field.click()
        bot.wait(1000)
        # usando fstring para resultado da busca ser de acordo com a linha da coluna correspondente
        department_field_option = bot.find_element(f"//div[@role='option' and @data-value='{row['Department']}']", By.XPATH)
        department_field_option.click()
        bot.wait(500)

        satisfaction_rating_field = bot.find_element(f"//div[contains(@data-params, 'Employee satisfaction rating')]//span[text()='{row['Satisfaction Rating']}']", By.XPATH)
        satisfaction_rating_field.click()
        bot.wait(500)

        submit_btn = bot.find_element("//div[@role='button']//span[text()='Enviar']", By.XPATH)
        submit_btn.click()

        submit_another_response_btn = bot.find_element("//a[text()='Enviar outra resposta']", By.XPATH)
        submit_another_response_btn.click()
        bot.wait(3000)




    # Wait 3 seconds before closing
    bot.wait(3000)

    # Finish and clean up the Web Browser
    # You MUST invoke the stop_browser to avoid
    # leaving instances of the webdriver open
    bot.stop_browser()

    # Uncomment to mark this task as finished on BotMaestro
    maestro.finish_task(
        task_id=execution.task_id,
        status=AutomationTaskFinishStatus.SUCCESS,
        message="Task Finished OK."
    )


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
