document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("pokemon-form");
    const resultDiv = document.getElementById("result");
    
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const name = document.getElementById("pokemon-name").value;
        const number = document.getElementById("pokemon-number").value;
        const set = document.getElementById("pokemon-set").value;

        // Validate input here (e.g., non-empty, valid format)
        if (!name || !number || !set) {
            resultDiv.innerHTML = `<p class="error">Please fill in all fields.</p>`;
            return; // Prevent further execution
        }

        // Show loading indicator while fetching data
        resultDiv.innerHTML = `<p class="loading">Fetching data...</p>`;

        // If valid, send AJAX request to the back-end
        try {
            const response = await fetch(`/get_pokemon_price?name=${name}&number=${number}&set=${set}`);
            const data = await response.json();
            displayResult(data);
        } catch (error) {
            console.error("Error:", error);
            resultDiv.innerHTML = `<p class="error">An error occurred. Please try again later.</p>`;
        }
    });

    function displayResult(data) {
        if (data.error) {
            resultDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        } else {
            resultDiv.innerHTML = `
                <h3 class="result-heading">All Prices in $USD for ${data.productName}</h3>
                <p>Price from Price Charting: ${data.priceChartingPrice}</p>
                <p>Price from PokeData: ${data.pokeDataPrice}</p>
                <p>Average Price: ${data.averagePrice}</p>
            `;
        }
    }
});
