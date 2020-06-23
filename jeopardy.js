// categories is the main data structure for the app; it looks like this:

//  [
//    { title: "Math",
//      clues: [
//        {question: "2+2", answer: 4, showing: null},
//        {question: "1+1", answer: 2, showing: null}
//        ...
//      ],
//    },
//    { title: "Literature",
//      clues: [
//        {question: "Hamlet Author", answer: "Shakespeare", showing: null},
//        {question: "Bell Jar Author", answer: "Plath", showing: null},
//        ...
//      ],
//    },
//    ...
//  ]
// jservice.io/api/categories?count=100&offset=1300
// returns 100 categories do random offset up to 1500 by 100s and then random category from that 100 section

let catIds = [];
let catInfo = [];

/** Get NUM_CATEGORIES random category from API.
 *
 * Returns array of category ids
 */

async function getCategoryIds() {
// random number for page offset in query
    const randOffset = (Math.floor(Math.random()*15)+1)*100;
// gets list of 100 categories with random page offset
    let catList = await axios.get('http://jservice.io/api/categories?', {params:{
        count: 100,
        offset: randOffset
    }});
// loops through list of categories and selects 5 at random to place into categories array
    for (let list of catList.data){
        while(catIds.length<6){
            catIds.push(catList.data[Math.floor(Math.random()*100)].id)
        }
    }
    return catIds;
}

/** Return object with data about a category:
 *
 *  Returns { title: "Math", clues: clue-array }
 *
 * Where clue-array is:
 *   [
 *      {question: "Hamlet Author", answer: "Shakespeare", showing: null},
 *      {question: "Bell Jar Author", answer: "Plath", showing: null},
 *      ...
 *   ]
 */
// create object for wanted params of a clue
 function getClueObj(clueInfo){
 
     const clueInfoEdit ={
         question: clueInfo.question,
         answer: clueInfo.answer,
         showing: null
     }

     return clueInfoEdit;
 }

//  loop through each object in array containing clues and adding category title and clue array to the object
async function getCategory(catId) {

    const cluesData = await axios.get(`http://jservice.io/api/clues?category=${catId}`);
    let length = cluesData.data.length;
    let i=0;
    let clues5 = [];
    while(i<5){
        clues5.push(cluesData.data[i])
        i++;
    }
    let catData = {};
    let clueArr = [];
    for (let clueInfo of clues5){
        clueArr.push(getClueObj(clueInfo));
        catData = {
            title: clueInfo.category.title,
            clues: clueArr
        }
    }
    return catData;
}

/** Fill the HTML table#jeopardy with the categories & cells for questions.
 *
 * - The <thead> should be filled w/a <tr>, and a <td> for each category
 * - The <tbody> should be filled w/NUM_QUESTIONS_PER_CAT <tr>s,
 *   each with a question for each category in a <td>
 *   (initally, just show a "?" where the question/answer would go.)
 */
function makeTitles(catInfo){
    let i = 0;
    const $body = $('body');
    const $div = $(`<div class="container">`);
    const $table = $('<table class="table">');
    const $tHead = $('<thead class="tableHead">');
    const $headRow = $('<tr class="headRow">');

    for (let info of catInfo){
        const $title = $(`<th id="${i}">${info.title}</th>`)
        $headRow.append($title)
        i++;
    }
    $tHead.append($headRow);
    $table.append($tHead);
    $div.append($table);
    $body.append($div);
}

function makeBody(){
    const $body = $('body');
    const $div = $(`<div class="container">`);
    const $table = $('<table class="table">');
    const $tBody = $('<tbody class="tableBody">');

    for (let y = 0; y < 5; y++){
        const $tr = $(`<tr id="${y}">`)
        for (let x = 0; x < 6; x++){
            const $td = $(`<td id="${x}-${y}" class="null">?</td>`)
            $tr.append($td);
        }
        $tBody.append($tr);
    }

    
    $table.append($tBody);
    $div.append($table);
    $body.append($div);
}

async function fillTable() {
    let afterHide = setTimeout( async function(){
        let catInfo = await setupAndStart();
    
    makeTitles(catInfo);
    
    makeBody();

    const $tBody = $('.tableBody');
    $tBody.on('click',handleClick);
    }, 3100) 
}

/** Handle clicking on a clue: show the question or answer.
 *
 * Uses .showing property on clue to determine what to show:
 * - if currently null, show question & set .showing to "question"
 * - if currently "question", show answer & set .showing to "answer"
 * - if currently "answer", ignore click
 * */

async function handleClick(e) {
    let target = e.target;
    let x = e.target.id[0];
    let y = e.target.id[2];
    const $td = $(`td #${x}-${y}`);
    
    if(target.classList.contains('null')){
        target.classList.remove('null');
        target.classList.add('Q');
        target.innerHTML = catInfo[x].clues[y].question;
    } else if (target.classList.contains('Q')){
        target.classList.remove('Q');
        target.classList.add('A');
        target.innerHTML = catInfo[x].clues[y].answer;
    } else if (target.classList.contains('A')){
        $td.off('click', '$tBody', handleClick)
    }

}

/** Wipe the current Jeopardy board, show the loading spinner,
 * and update the button used to fetch data.
 */

function showLoadingView() {
    const img = document.createElement('img');
    img.src = 'https://media2.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif?cid=11a5632ed3f09dd6fe6302808ffd99ba1a330c047230e92f&rid=giphy.gif';
    const body = document.querySelector('body');
    body.append(img);
}

/** Remove the loading spinner and update the button used to fetch data. */

function hideLoadingView() {
    let hide = setTimeout(function(){
        const img = document.querySelector('img');
        const body = document.querySelector('body');
        body.removeChild(img);
    },3000) 
}

/** Start game:
 *
 * - get random category Ids
 * - get data for each category
 * - create HTML table
 * */

async function setupAndStart() {
    catInfo = [];
    
    let catIds = await getCategoryIds();
    
    for (let catId of catIds){
        catInfo.push(await getCategory(catId));
    }
    return catInfo;
}

/** On click of start / restart button, set up game. */

$('#startBtn').on('click', function(e){
    
    showLoadingView();
    hideLoadingView();
    
    fillTable();
    $('#startBtn').html('Restart');
    catIds = [];
    clues5 = [];
    catData = {};
    clueArr = [];
    catInfo = [];
    $('div').empty();
})


// add click effect to start/restart button

$('#startBtn').on('mousedown', function(e){
    $('#startBtn').removeClass('norm')
    $('#startBtn').addClass('click')
});
$('#startBtn').on('mouseup', function(e){
    $('#startBtn').removeClass('click')
    $('#startBtn').addClass('norm')
});

// on page load set up board
$('#startBtn').trigger('click');