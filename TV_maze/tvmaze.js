/** Given a query string, return array of matching shows:
 *     { id, name, summary, episodesUrl }
 */


/** Search Shows
 *    - given a search term, search for tv shows that
 *      match that query.  The function is async show it
 *       will be returning a promise.
 *
 *   - Returns an array of objects. Each object should include
 *     following show information:
 *    {
        id: <show id>,
        name: <show name>,
        summary: <show summary>,
        image: <an image from the show data, or a default imege if no image exists, (image isn't needed until later)>
      }
 */

// setting variable for image source if null
let Missing_Url = 'https://store-images.s-microsoft.com/image/apps.65316.13510798887490672.6e1ebb25-96c8-4504-b714-1f7cbca3c5ad.f9514a23-1eb8-4916-a18e-99b1a9817d15?mode=scale&q=90&h=300&w=300'
async function searchShows(query) {
  // get input text value and create array of objects containing shows and wanted parameters

  let searchQuery = document.querySelector('#search-query').value;

  let response = await axios.get('http://api.tvmaze.com/search/shows?', {params: {
    q: searchQuery
  }})
  
  const shows = [];

  for (let show of response.data) {
    let showEdit = {
      id: show.show.id,
      name: show.show.name,
      summary: show.show.summary, 
      image: show.show.image ? show.show.image.original : Missing_Url,
    }
    shows.push(showEdit);
  }
  
  return shows;
}



/** Populate shows list:
 *     - given list of shows, add shows to DOM
 */

function populateShows(shows) {
  const $showsList = $("#shows-list");
  $showsList.empty();

  for (let show of shows) {
    let $item = $(
      `<div class="col-md-6 col-lg-3 Show" data-show-id="${show.id}">
         <div class="card" data-show-id="${show.id}">
           <div class="card-body">
             <h5 class="card-title">${show.name}</h5>
             <p class="card-text">${show.summary}</p>
             <img class="card-img-top" src="${show.image}" onerror="this.src='https://store-images.s-microsoft.com/image/apps.65316.13510798887490672.6e1ebb25-96c8-4504-b714-1f7cbca3c5ad.f9514a23-1eb8-4916-a18e-99b1a9817d15?mode=scale&q=90&h=300&w=300'">
             <button class="btn btn-primary episodesBtn">Episodes</button>
           </div>
         </div>
       </div>
      `);

    $showsList.append($item);
  }
}


/** Handle search form submission:
 *    - hide episodes area
 *    - get list of matching shows and show in shows list
 */

$("#search-form").on("submit", async function handleSearch (evt) {
  evt.preventDefault();

  let query = $("#search-query").val();
  if (!query) return;

  $("#episodes-area").hide();

  let shows = await searchShows(query);

  populateShows(shows);
  // emptying text input
  let empty = document.querySelector('#search-query');
  empty.value = '';
});


/** Given a show ID, return list of episodes:
 *      { id, name, season, number }
 */

async function getEpisodes(id) {

  let response = await axios.get(`http://api.tvmaze.com/shows/${id}/episodes`);

  let episodes = [];

  for (let episode of response.data){
    let episodeEdit = {
      id: episode.id,
      name: episode.name,
      season: episode.season,
      number: episode.number
    }
    episodes.push(episodeEdit);
  }

  return episodes;
}

function populateEpisodes(episodes){

  // creating new li elements to hold episode info,assigning id, appending to col and list
  const $episodeList = $('#episodes-list');
// emptying list in order to replace episodes instaed of adding on when another episode button is clicked
  $episodeList.empty();

  for (let episode of episodes){

    const newLi = document.createElement('li');
    newLi.classList.add(episode.id);
    const newCol = document.createElement('col-sm');
    newLi.innerText = `${episode.name} (season ${episode.season}, number ${episode.number})`

    newCol.append(newLi);
    $episodeList.append(newCol);
  }
  
  $("#episodes-area").show();
}

// getting episode id to use in getEpisodes func, getting episodes to use in populateEpisodes, populating the episode list

$('#shows-list').on('click','.episodesBtn', async function handleClick(e){
  let id = $(e.target).closest('div.card').data();
  let episodes = await getEpisodes(id.showId);

  populateEpisodes(episodes);
  
})