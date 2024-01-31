const API_URL = 'https://api.coingecko.com/api/v3/coins/markets';

fetch(API_URL)
  .then(response => response.json())
  .then(data => {
    // Calculate the percentage change in price for each cryptocurrency
    const gainers = data.map(crypto => {
      const priceChangePercent = crypto.price_change_percentage_24h;
      return { name: crypto.name, priceChangePercent };
    });

    // Sort the list of cryptocurrencies based on their percentage change in price
    gainers.sort((a, b) => b.priceChangePercent - a.priceChangePercent);

    // Select the top three gainers
    const topGainers = gainers.slice(0, 3);

    // Create HTML elements to display the top three gainers
    const gainersDiv = document.querySelector('#gainers');
    topGainers.forEach((gainer, index) => {
      const gainerElement = document.createElement('div');
      gainerElement.innerText = `${index + 1}. ${gainer.name}: ${gainer.priceChangePercent}%`;
      gainersDiv.appendChild(gainerElement);
    });
  })
  .catch(error => console.error(error));
