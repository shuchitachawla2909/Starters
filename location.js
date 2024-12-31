var requestOptions = {
  method: 'GET',
};

fetch("https://api.geoapify.com/v1/geocode/autocomplete?text=Mosco&apiKey=5453fd136f59455389f1b49116c65013", requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));