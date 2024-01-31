 fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=price_change_percentage_24h&per_page=100&page=1')
        .then(response => response.json())
        .then(data => {
          // Filter out coins with positive price change and sort data based on 24h price change in descending order
          const sortedData = data.filter(coin => coin.price_change_percentage_24h < 0).sort((a, b) => a.price_change_percentage_24h - b.price_change_percentage_24h);
          
          // Take top 10 coins
          const top10Coins = sortedData.slice(0, 10);
          
          // Display top 10 coins on HTML page
          const loserTable = document.getElementById('loser-table');
          top10Coins.forEach((coin, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
            <td class="coin-cell"><a href="/trade/${coin.id}"><img src="${coin.image}" alt="${coin.name}" style="height: 20px;"></a></td>
            <td class="coin-cell">${coin.symbol.toUpperCase()}</td>
            <td class="coin-cell">$${coin.current_price.toLocaleString()}</td>
            <td class="coin-cell" style="color: red;">${coin.price_change_percentage_24h.toFixed(2)}%</td>
            `;
            loserTable.appendChild(row);
          });
        })
        .catch(error => console.error(error));
