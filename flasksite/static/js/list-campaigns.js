//ajax posts query string to flask
function campSearch() {
  //first remove any results form old search
  ds.removeChildren("campaignlist_div");
  //get search str
  var search_str = document.getElementById("campaign_searchbox").value;

  $.post('/campaignsearch', {search_str: search_str},
    function(result) {
      var campaigns = JSON.parse(result['campaigns']);

      var list = document.getElementById("campaignlist_div");
      //create div with p fro each result
      for (i=0; i<campaigns.length; i++) {
        var elem = document.createElement("div");
        var p = document.createElement("p");
        var textnode = document.createTextNode(campaigns[i].title);
        p.appendChild(textnode);
        elem.appendChild(p)
        list.appendChild(elem);
      }
    })
  .done(
    function (x){
      //set button to flash 'Success!'
      document.getElementById("campaign_searchbtn").value='Success!';
      setTimeout(function(){document.getElementById("campaign_searchbtn").value='Find';}, 200);
    }
  )
  .fail(
    function (x){
      //set button to warn on failure
      document.getElementById("campaign_searchbtn").value='Server Error, Not Submitted!';
    }
  );
}
//make p clickable
var main_div = document.getElementById('campaignlist_div');

main_div.addEventListener('click', function(e) {

    if (e.target.tagName === 'P'){
      var div_content = e.target.textContent.replace('#','^&^').replace('?','^^^');
      window.location = '/' + div_content;
    }
});