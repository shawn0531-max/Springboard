// jwhshOzYUEupkzsVjLGHuBn4DOgald7W GIPHY KEY

// what search looks like
// https://api.giphy.com/v1/gifs/search?api_key=jwhshOzYUEupkzsVjLGHuBn4DOgald7W&q=dog&limit=25&offset=0&rating=G&lang=en

const form = document.querySelector('#submitForm');
const input = document.querySelector('#inputText');
const $col1 = $('#col1');
const $col2 = $('#col2');
const $col3 = $('#col3');
const remove = document.querySelector('#removeBtn');
let colNum = 1;

function makeImg(res) {
    
    const randGifNum = Math.floor(Math.random()*25);
    const img = document.createElement('img');
    img.classList.add('newImg')
    img.src = res.data[randGifNum].images.original.url;
    
    if(colNum ===1){
        $col1.append(img);
        colNum = 2;
    } else if (colNum === 2) {
        $col2.append(img);
        colNum = 3;
    } else if (colNum === 3) {
        $col3.append(img);
        colNum = 1;
    }

};



form.addEventListener('submit', async function(e){
    e.preventDefault();

    let searchVal = input.value;
    input.value = ''; 

    const response = await axios.get('https://api.giphy.com/v1/gifs/search', {params: {
        q: searchVal,
        api_key: 'jwhshOzYUEupkzsVjLGHuBn4DOgald7W'
    }});

    makeImg(response.data);

});

$("#removeBtn").on("click", function() {
    $col1.empty();
    $col2.empty();
    $col3.empty();
  });