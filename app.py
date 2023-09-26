from flask import Flask, request, jsonify
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/get_pokemon_price")


def get_pokemon_price():

    # Retrieve user input from the query parameters
    inputPokemonName = request.args.get("name")
    pokemonNumber = request.args.get("number")
    inputPokemonSet = request.args.get("set")

    CO = webdriver.ChromeOptions()
    CO.add_experimental_option('useAutomationExtension', False)
    CO.add_argument('--ignore-certificate-errors')
    CO.add_argument('--start-maximized')
    CO.add_argument('--headless')
    # Initialize the WebDriver with options and the specified executable path
    wd = webdriver.Chrome(options=CO)
    # Perform scraping and price calculation logic here
    while True:
        if len(inputPokemonName) > 1:
            rawPokemonName = inputPokemonName.split()
            pokemonNamePC = "-".join(rawPokemonName)
            pokemonNamePD = "+".join(word.capitalize() for word in rawPokemonName)
            break
        elif len(inputPokemonName) == 1:
            pokemonNamePC = inputPokemonName
            pokemonNamePD = inputPokemonName
            break
        else:
            print("Invalid input, please try again.")

    while True:
        if len(inputPokemonSet) > 1:
            rawPokemonSet = inputPokemonSet.split()
            pokemonSetPC = "-".join(rawPokemonSet)
            pokemonSetPD = "+".join(word.capitalize() for word in rawPokemonSet)
            break
        elif len(inputPokemonSet) == 1:
            pokemonSetPC = inputPokemonSet
            pokemonSetPD = inputPokemonSet
            break
        else:
            print("Invalid input, please try again.")



    source1 = "https://www.pricecharting.com/game/pokemon-"+pokemonSetPC+"/"+pokemonNamePC+"-"+pokemonNumber
    source2 = "https://www.pokedata.io/set/"+pokemonSetPD+"?f="+pokemonNamePD+"+"+pokemonNumber


    # Initialize the WebDriver with options and the specified executable path
    # Initialize price_charting_price and poke_data_price variables

    
    with webdriver.Chrome(options=CO) as wd:

        try:
            print("Connecting to Price Charting")
            wd.get(source1)
            time.sleep(1) 
            try:
                raw_price = ""
                pc_price = wd.find_element(By.ID, "used_price")
                pr_name = wd.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/h1")
                product = pr_name.text
                r_priceVar = pc_price.text
                r_priceVar = r_priceVar.strip()  # Strip whitespace from both ends of the string
                r_price = r_priceVar.split()[0]  # Split the string by space and take the first part
                print(r_priceVar)
                print(r_price)
                print(" ---> Successfully retrieved the price from Price Charting\n")
                time.sleep(0.5) 
            except NoSuchElementException:
                print("Element not found on the page. Check if pokemon name, number, and set name are valid.")

            print("Connecting to PokeData")
            wd.get(source2)
            time.sleep(1)  
            try:
                time.sleep(2) 
                raw_price = ""
                pd_price = wd.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[3]/div[2]/div/div/div[2]/a/div[3]/span")
                raw_price = pd_price.text

                print(" ---> Successfully retrieved the price from PokeData\n")
            except NoSuchElementException:
                print("Element not found on the page. Check if pokemon name, number, and set name are valid.")


            # Assign values to price_charting_price and poke_data_price
            product_name = product
            price_charting_price = r_price
            poke_data_price = raw_price

            # Calculate average price
            r_priceNum = float(r_price.replace("$", ""))
            raw_priceNum = float(raw_price.replace("$", ""))
            average_price = (raw_priceNum + r_priceNum) / 2

            # Create a JSON response
            response_data = {
                "productName": product_name,
                "priceChartingPrice": price_charting_price,
                "pokeDataPrice": poke_data_price,
                "averagePrice": average_price,
            }
            print(" ---> Successfully created json response\n")
            return jsonify(response_data)

        except NoSuchElementException as e:
            error_message = f"Element not found: {str(e)}"
            return jsonify({"error": error_message})
        finally:
            wd.quit()
if __name__ == "__main__":
    app.run(debug=True)
