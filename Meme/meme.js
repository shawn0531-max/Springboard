const memeForm = document.querySelector('#memeForm');
const submitForm = document.querySelector('#submitMeme');
const removeBtn = document.querySelector('#removeBtn');
const submitBtn = document.querySelector('#submitBtn');
const topMemeText = document.querySelector('#topMemeText');
const bottomMemeText = document.querySelector('#bottomMemeText');
const completedMemesDiv = document.querySelector('#completedMemesDiv');
const image = document.querySelector('#image');

memeForm.addEventListener('submit', function(e){
    e.preventDefault();

    let input = document.querySelector('#link');
    let inputValue = input.value;

    if (inputValue === ""){
        alert("Please enter a valid picture link!")
    } else {
        let inputText = inputValue.toString();
        image.src = inputText;
        removeBtn.style.visibility = "visible";
        submitBtn.style.visibility = "visible";
        topMemeText.style.visibility = "visible";
        bottomMemeText.style.visibility = "visible";
    }
});

topMemeText.addEventListener('input', updateTop);
function updateTop(e){
    let topDiv = document.querySelector('#topDiv');
    topDiv.innerText = e.target.value; 
};

bottomMemeText.addEventListener('input', updateBottom);
function updateBottom(e){
    let bottomDiv = document.querySelector('#bottomDiv');
    bottomDiv.innerText = e.target.value;
};

submitForm.addEventListener('submit', function(e){
    e.preventDefault();

    let newImage = document.createElement('img');
    let newDiv = document.createElement('div');
    let newTopDiv = document.createElement('div');
    let newBottomDiv = document.createElement('div');
    let newRemoveBtn = document.createElement('button');
    let input = document.querySelector('#link');
    let inputValue = input.value;
    let inputText = inputValue.toString();
    newImage.src = inputText;

    newDiv.classList.add("newDiv");
    newTopDiv.classList.add("newTopDiv");
    newBottomDiv.classList.add("newBottomDiv");
    newRemoveBtn.classList.add("newRemoveBtn");

    newTopDiv.innerText = topDiv.innerText;
    newBottomDiv.innerText = bottomDiv.innerText;
    newRemoveBtn.innerText = "X";
    
    newDiv.append(newImage);
    newDiv.append(newTopDiv);
    newDiv.append(newBottomDiv);
    newDiv.append(newRemoveBtn);
    completedMemesDiv.append(newDiv);

})

removeBtn.addEventListener('click', function(e){
    let input = document.querySelector('#link');
    input.value = "";
    topMemeText.value = "";
    bottomMemeText.value = "";
    image.src = "";
    topDiv.innerText = "";
    bottomDiv.innerText = "";
    removeBtn.style.visibility = "hidden";
    submitBtn.style.visibility = "hidden";
    topMemeText.style.visibility = "hidden";
    bottomMemeText.style.visibility = "hidden";
});

completedMemesDiv.addEventListener('click', function(e){
    let clicked = e.target;
    if (clicked.tagName === "BUTTON"){
        clicked.parentElement.remove();
    }
})