//BTC PRICE

fetch("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
  .then(response => response.json())
  .then(data => {
    const btcPrice = parseFloat(data.price);
    const btcPriceSpan = document.getElementById("btc-price");
    btcPriceSpan.textContent = `$${btcPrice.toFixed(2)}`;
  })
  .catch(error => {
    console.error("Failed to fetch BTC price:", error);
  });

//BTC PRICE CHANGE


fetch("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT")
  .then(response => response.json())
  .then(data => {

    const btcPriceChange = parseFloat(data.priceChangePercent);

    const btcPriceChangeSpan = document.getElementById("btc-growth-rate");
    btcPriceChangeSpan.textContent = `${btcPriceChange.toFixed(2)}%`;
  })
  .catch(error => {
    console.error("Failed to fetch BTC price change:", error);
  });

//ETH PRICE
  

  fetch("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
    .then(response => response.json())
    .then(data => {
     
      const ethPrice = parseFloat(data.price);
  

      const ethPriceSpan = document.getElementById("eth-price");
      ethPriceSpan.textContent = `$${ethPrice.toFixed(2)}`;
    })
    .catch(error => {
      console.error("Failed to fetch ETH price:", error);
    });
//ETH GROWTH RATE

fetch("https://api.binance.com/api/v3/ticker/24hr?symbol=ETHUSDT")
  .then(response => response.json())
  .then(data => {
    const ethPriceChange = parseFloat(data.priceChangePercent);

    const ethPriceChangeSpan = document.getElementById("eth-growth-rate");
    ethPriceChangeSpan.textContent = `${ethPriceChange.toFixed(2)}%`;
  })
  .catch(error => {
    console.error("Failed to fetch ETH price change:", error);
  });
//LTC PRICE
fetch("https://api.binance.com/api/v3/ticker/price?symbol=LTCUSDT")
  .then(response => response.json())
  .then(data => {
    const ltcPrice = parseFloat(data.price);
    const ltcPriceSpan = document.getElementById("ltc-price");
    ltcPriceSpan.textContent = `$${ltcPrice.toFixed(2)}`;
  })
  .catch(error => {
    console.error("Failed to fetch LTC price:", error);
  });
//LTC PRICE CHANGE



// Fetch the 24-hour ticker statistics for the LTC/USDT trading pair from the Binance API
fetch("https://api.binance.com/api/v3/ticker/24hr?symbol=LTCUSDT")
  .then(response => response.json())
  .then(data => {
    const ltcPriceChange = parseFloat(data.priceChangePercent);
    const ltcPriceChangeSpan = document.getElementById("ltc-growth-rate");
    ltcPriceChangeSpan.textContent = `${ltcPriceChange.toFixed(2)}%`;
  })
  .catch(error => {
    console.error("Failed to fetch LTC price change:", error);
  });

  //Function for Button to hold value of usdt amount
  function displayValueBuy() {
    var input = document.getElementById("usdt-amount").value;
    var button = document.getElementById("display-button");
    button.innerHTML = "Purchase $" + input;
  }


  function showDiv1() {
    document.getElementById("div1").style.display = "block";
    document.getElementById("div2").style.display = "none";
  }
  
  function showDiv2() {
    document.getElementById("div1").style.display = "none";
    document.getElementById("div2").style.display = "block";
  }
  
  window.onload = function() {
    document.getElementById("div1").style.display = "block";
  }



  function copyAddress() {
    const address = document.querySelector("#crypto-address-bar span").textContent;
    navigator.clipboard.writeText(address).then(() => {
      alert("Address copied to clipboard!");
    });
  }
  function updateAddress(crypto) {
    fetch('/', {
      method: 'POST',
      body: new URLSearchParams({crypto: crypto})
    }).then(response => response.text())
      .then(address => {
        document.getElementById('address').innerText = `Your ${crypto} address: ${address}`
      })
  }  
 
  fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=price_change_percentage_24h&per_page=100&page=1')
  .then(response => response.json())
  .then(data => {
    // Sort data based on 24h price change
    const sortedData = data.sort((a, b) => b.price_change_percentage_24h - a.price_change_percentage_24h);
    
    // Take top 10 coins
    const top10Coins = sortedData.slice(0, 10);
    
    // Display top 10 coins on HTML page
    const coinsTable = document.getElementById('coins-table');
    top10Coins.forEach((coin, index) => {
      const row = document.createElement('tr');
      row.classList.add('coin-row');
      const logoLink = document.createElement('a');
      logoLink.href = `https://www.coingecko.com/en/trade/${coin.id}`;
      logoLink.target = '_blank';
      const logoImg = document.createElement('img');
      logoImg.src = coin.image;
      logoImg.alt = coin.name;
      logoImg.style.height = '20px';
      logoLink.appendChild(logoImg);
      const symbolCell = document.createElement('td');
      symbolCell.classList.add('coin-cell');
      const symbolLink = document.createElement('a');
      symbolLink.href = `https://www.coingecko.com/en/trade/${coin.id}`;
      symbolLink.target = '_blank';
      symbolLink.appendChild(document.createTextNode(coin.symbol.toUpperCase()));
      symbolCell.appendChild(symbolLink);
      const priceCell = document.createElement('td');
      priceCell.classList.add('coin-cell');
      priceCell.appendChild(document.createTextNode(`$${coin.current_price.toFixed(2)}`));
      const changeCell = document.createElement('td');
      changeCell.classList.add('coin-cell');
      changeCell.classList.add('growth-cell');
      changeCell.appendChild(document.createTextNode(`${coin.price_change_percentage_24h.toFixed(2)}%`));
      row.appendChild(document.createElement('td').appendChild(logoLink));
      row.appendChild(symbolCell);
      row.appendChild(priceCell);
      row.appendChild(changeCell);
      coinsTable.appendChild(row);
    });
  })
  .catch(error => console.error(error));

  //Top 10 Losers
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


// Top 10 by vol
fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1')
  .then(response => response.json())
  .then(data => {
    // Display top 10 coins on HTML page
    const top10Coins = data;
    const top10Table = document.getElementById('top-10-table');
    top10Coins.forEach((coin, index) => {
      const row = document.createElement('tr');
      row.innerHTML = `
      <td class="coin-cell"><img src="${coin.image}" alt="${coin.name}" style="height: 20px;"></td>
      <td class="coin-cell">${coin.symbol.toUpperCase()}</td>
      <td class="coin-cell" style="color: ${coin.price_change_percentage_24h < 0 ? 'red' : 'green'};">${coin.price_change_percentage_24h.toFixed(2)}%</td>
      `;
      top10Table.appendChild(row);
    });
  })
  .catch(error => console.error(error));


  //Greed and Fear Index
  fetch('https://api.alternative.me/fng/')
  .then(response => response.json())
  .then(data => {
    // Extract latest value from data
    const value = data.data[0].value;

    // Set fear and greed index value and label
    document.getElementById('fear-greed-value').textContent = value;
    document.getElementById('fear-greed-label').textContent = getFearGreedLabel(value);

    // Set fear and greed index background color
    const container = document.getElementById('fear-greed-container');
    container.classList.add(getFearGreedBackground(value));
  })
  .catch(error => console.error(error));

// Function to get fear and greed index label based on value
function getFearGreedLabel(value) {
  if (value <= 20) {
    return 'Extreme Fear';
  } else if (value <= 40) {
    return 'Fear';
  } else if (value <= 60) {
    return 'Neutral';
  } else if (value <= 80) {
    return 'Greed';
  } else {
    return 'Extreme Greed';
  }
}

// Function to get fear and greed index background class based on value
function getFearGreedBackground(value) {
  if (value <= 20) {
    return 'extreme-fear';
  } else if (value <= 40) {
    return 'fear';
  } else if (value <= 60) {
    return 'neutral';
  } else if (value <= 80) {
    return 'greed';
  } else {
    return 'extreme-greed';
  }
}


// Function to fetch order book data from Binance API
async function getOrderBook(symbol) {
  try {
    const response = await fetch(`https://api.binance.com/api/v3/trades?symbol=${symbol}`);
    const data = await response.json();
    const orders = data;

    // Clear previous order book data
    document.getElementById('buyOrders').innerHTML = '';
    document.getElementById('sellOrders').innerHTML = '';

    // Group orders by price
    const groupedOrders = {};
    orders.forEach(order => {
      const price = parseFloat(order.price).toFixed(2);
      if (!groupedOrders[price]) {
        groupedOrders[price] = {
          buyQuantity: 0,
          buyTotal: 0,
          sellQuantity: 0,
          sellTotal: 0,
        };
      }

      if (order.isBuyerMaker) {
        groupedOrders[price].sellQuantity += parseFloat(order.qty);
        groupedOrders[price].sellTotal += parseFloat(order.qty) * parseFloat(order.price);
      } else {
        groupedOrders[price].buyQuantity += parseFloat(order.qty);
        groupedOrders[price].buyTotal += parseFloat(order.qty) * parseFloat(order.price);
      }
    });

    // Display buy orders
    Object.entries(groupedOrders).forEach(([price, order]) => {
      if (order.buyQuantity > 0) {
        const orderRow = document.createElement('div');
        orderRow.classList.add('order-row', 'buy-order');

        const orderInfo = document.createElement('p');
        orderInfo.classList.add('order-info');
        orderInfo.style.color = '#01c38d'; // Set text color for buy orders
        orderInfo.innerText = `${price} ${order.buyQuantity.toFixed(4)} ${order.buyTotal.toFixed(2)}`;
        orderRow.appendChild(orderInfo);

        document.getElementById('buyOrders').appendChild(orderRow);
      }
    });

    // Display sell orders
    Object.entries(groupedOrders).forEach(([price, order]) => {
      if (order.sellQuantity > 0) {
        const orderRow = document.createElement('div');
        orderRow.classList.add('order-row', 'sell-order');

        const orderInfo = document.createElement('p');
        orderInfo.classList.add('order-info');
        orderInfo.style.color = 'red'; // Set text color for sell orders
        orderInfo.innerText = `${price} ${order.sellQuantity.toFixed(4)} ${order.sellTotal.toFixed(2)}`;
        orderRow.appendChild(orderInfo);

        document.getElementById('sellOrders').appendChild(orderRow);
      }
    });

  } catch (error) {
    console.log('Error:', error);
  }
}

// Fetch order book initially
const pair = window.location.pathname.split('/').pop();
if (pair) {
  const symbol = pair.toUpperCase();
  getOrderBook(symbol);
} else {
  getOrderBook('BTCUSDT'); // Default to BTCUSDT if pair is not provided in the URL
}

// Refresh order book every 5 seconds (5000 milliseconds)
setInterval(() => {
  if (pair) {
    const symbol = pair.toUpperCase();
    getOrderBook(symbol);
  } else {
    getOrderBook('BTCUSDT'); // Default to BTCUSDT if pair is not provided in the URL
  }
}, 1000);



function addParameter() {
  var currentUrl = window.location.href; // Get the current URL
  var parameter = "newParam=example"; // Parameter to add

  // Check if the URL already has query parameters
  if (currentUrl.indexOf('?') !== -1) {
      // URL already has parameters
      window.location.href = currentUrl + '&' + parameter;
  } else {
      // URL does not have parameters
      window.location.href = currentUrl + '?' + parameter;
  }
}
// Inflow chart code
let inflowChart;

// Fetch the pair value from the URL slug
const urlParams = new URLSearchParams(window.location.search);
const pair2 = urlParams.get('pair2');
const symbol = pair2 || 'BTCUSDT'; // Default pair if no pair value is provided
const apiUrl = `https://api.binance.com/api/v3/depth?symbol=${symbol}`;

function updateChart() {
  fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      // Extracting relevant data
      const bids = data.bids;
      const asks = data.asks;

      // Preparing cumulative sum arrays
      const cumulativeBids = bids.reduce((acc, order) => {
        const [price, quantity] = order;
        const prevSum = acc.length > 0 ? acc[acc.length - 1] : 0;
        acc.push(prevSum + parseFloat(quantity));
        return acc;
      }, []);
      const cumulativeAsks = asks.reduce((acc, order) => {
        const [price, quantity] = order;
        const prevSum = acc.length > 0 ? acc[acc.length - 1] : 0;
        acc.push(prevSum + parseFloat(quantity));
        return acc;
      }, []);

      // Reversing the asks arrays for proper visualization
      cumulativeAsks.reverse();

      // Destroy the old chart before creating the new one
      if (inflowChart) {
        inflowChart.destroy();
      }

      // Create the inflow chart
      const inflowChartCtx = document.getElementById('inflowChart').getContext('2d');
      inflowChart = new Chart(inflowChartCtx, {
        type: 'line',
        data: {
          labels: [...bids.map(order => order[0]), ...asks.map(order => order[0])],
          datasets: [
            {
              data: [...cumulativeBids, ...cumulativeBids.slice(-1)],
              borderColor: 'green',
              backgroundColor: 'rgba(0, 128, 0, 0.1)',
              fill: 'origin',
              pointRadius: 0
            },
            {
              data: [...cumulativeAsks, ...cumulativeAsks.slice(-1)],
              borderColor: 'red',
              backgroundColor: 'rgba(255, 0, 0, 0.1)',
              fill: 'origin',
              pointRadius: 0
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          title: {
            display: true,
            text: 'Market Depth Chart'
          },
          scales: {
            x: {
              display: false, // Hide x-axis
            },
            y: {
              display: false, // Hide y-axis
            }
          },
          plugins: {
            legend: {
              display: false // Hide legend
            }
          }
        },
        // Set the canvas width to 400px
        plugins: [{
          beforeDraw: function (chart) {
            const ctx = chart.ctx;
            ctx.canvas.width = 400;
          }
        }]
      });
    })
    .catch(error => {
      console.error('Error fetching depth data:', error);
    });
}

// Update the chart every 5 seconds
setInterval(updateChart, 1000);
updateChart();


$(document).ready(function() {
  var carousel = $(".carousel");
  var currdeg = 0;
  var timer;

  function rotate() {
    currdeg = currdeg + 1;
    carousel.css({
      "transform": "rotateY(" + currdeg + "deg)"
    });
  }

  function startRotation() {
    timer = setInterval(rotate, 30); // Decreased interval to 50 milliseconds
  }

  function stopRotation() {
    clearTimeout(timer);
  }

  carousel.mouseover(stopRotation);
  carousel.mouseleave(startRotation);

  startRotation();
});

//Updating total in buysell bar
function updateTotal(orderType) {
  const quantityInput = document.getElementById(`${orderType}-quantity`);
  const priceInput = document.getElementById(`${orderType}-price`);
  const totalSpan = document.getElementById(`${orderType}-total`);

  const quantity = parseFloat(quantityInput.value) || 0;
  const price = parseFloat(priceInput.value) || 0;
  const total = quantity * price;

  totalSpan.textContent = total.toFixed(2);
}



// to update with lowest price in buy section







//Portfolio Pie Chart

fetch('/pie-data')
  .then(response => response.json())
  .then(data => {
    const assetNames = data.asset_name;
    const totalAmounts = data.total_amount;

    // Create pie chart
    const ctx = document.getElementById('cryptoChart').getContext('2d');
    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: assetNames,
        datasets: [{
          data: totalAmounts,
          backgroundColor: generateShadesOfColor('#01c38d', assetNames.length),
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false, // Disable maintaining aspect ratio
        width: 240, // Set the width to 240 pixels
        height: 240, // Set the height to 240 pixels
        title: {
          display: true,
          text: 'Crypto Asset Distribution'
        }
      }
    });
  });

// Function to generate shades of a color
function generateShadesOfColor(color, count) {
  const colors = [];
  const baseColor = tinycolor(color);
  for (let i = 0; i < count; i++) {
    const shade = baseColor.lighten(i * 5).toString();
    colors.push(shade);
  }
  return colors;
}


//Js code for port legends

    // Fetch data from /port-history endpoint
    fetch('/port-history')
      .then(response => response.json())
      .then(data => {
        const monthNames = data.month_names;
        const portValues = data.port_val.map(Number);

        // Create chart
        const ctx = document.getElementById('port-legends').getContext('2d');
        new Chart(ctx, {
          type: 'line',
          data: {
            labels: monthNames,
            datasets: [{
              label: 'Portfolio Net Worth',
              data: portValues,
              backgroundColor: 'rgba(1, 195, 141, 0.2)',
              borderColor: 'rgba(1, 195, 141, 1)',
              borderWidth: 3 // Increase the border width to make the line thicker
            }]
          },
          options: {
            scales: {
              x: {
                display: false
              },
              y: {
                display: false
              }
            },
            plugins: {
              legend: {
                display: false
              }
            }
          }
        });
      })
      .catch(error => {
        console.error('Error:', error);
      });



      //User Settings
      function showInputForm() {
        var selectedOption = document.querySelector('input[name="update_option"]:checked').value;
        var emailForm = document.getElementById('emailForm');
        var passwordForm = document.getElementById('passwordForm');
        var emailField = document.getElementById('email');
        var passwordField = document.getElementById('password');
  
        if (selectedOption === 'email') {
          emailForm.style.display = 'block';
          passwordForm.style.display = 'none';
          emailField.disabled = false;
          passwordField.disabled = true;
          passwordField.value = ''; // Clear the password field
          emailField.required = true;
          passwordField.required = false;
        } else {
          emailForm.style.display = 'none';
          passwordForm.style.display = 'block';
          emailField.disabled = true;
          passwordField.disabled = false;
          emailField.value = ''; // Clear the email field
          emailField.required = false;
          passwordField.required = true;
        }
      }


//NFT Marketplace

// Make an API request to fetch the NFT information
fetch('/nft-info')
  .then(response => response.json())
  .then(data => displayNFTs(data))
  .catch(error => console.error(error));

// Function to display the NFTs as cards
function displayNFTs(nfts) {
  const container = document.getElementById('nft-container'); // Assuming you have a container element with the id 'nft-container'

  // Loop through each NFT and create a card
  nfts.forEach(nft => {
    const card = document.createElement('div');
    card.classList.add('nft-card'); // Assuming you have CSS styles for 'nft-card' class

    // Create an image element and set its source
    const image = document.createElement('img');
    image.src = nft.image;
    card.appendChild(image);

    // Create a paragraph element for displaying the NFT id
    const idParagraph = document.createElement('p');
    idParagraph.textContent = `ID: ${nft.id}`;
    card.appendChild(idParagraph);

    // Create a paragraph element for displaying the NFT price
    const priceParagraph = document.createElement('p');
    priceParagraph.textContent = `Price: $${nft.price}`;
    card.appendChild(priceParagraph);

    // Append the card to the container
    container.appendChild(card);
  });
}