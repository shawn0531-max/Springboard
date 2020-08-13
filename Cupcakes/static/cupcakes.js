window.addEventListener('load', addLi())
window.addEventListener('load', addButton())
formDiv = $('#cupcake')
window.addEventListener('load', formDiv.hide())

async function addLi() {
    // Adds list item for each cupcake in table in DB
    const c_ul = document.querySelector('ul');

    const resp = await axios.get('/api/cupcakes')

    for (let cupcake of resp.data.cupcakes){
        const newLi = document.createElement('li')
        newLi.append(cupcake.flavor)
        c_ul.append(newLi)
    }
}

function addButton() {
    // Adds button on page to load form
    const div = document.querySelector('#divBtn');

    const newButton = document.createElement('button')
    newButton.innerText = 'New Cupcake'
    newButton.className = 'btn btn-success'

    div.append(newButton)

}

$('button').on('click', function(e){
        $('.btn').hide();
        $('#cupcake').show();
        $('#addBtn').show();
});

$('#add-cupcake-form').on('submit', async function(e){
    e.preventDefault()

    let flavor = $('#flavor').val();
    let size = $('#size').val();
    let rating = $('#rating').val();
    let image = $('#image').val();

    if (image ==- ''){
        image = "https://tinyurl.com/demo-cupcake"
    }

    await axios.post('/api/cupcakes', {
        'flavor':flavor,
        'size':size, 
        'rating':rating,
        'image':image
      })
      .then(function (response) {
        console.log(response);
      })

    $('.btn').show();
    $('#cupcake').hide();
    $('#addBtn').hide();

    window.location.reload()
})


//handle new cupcake posts with axios on page and update API