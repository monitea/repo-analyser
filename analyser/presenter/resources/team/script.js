function getMaxOf(data){
  var max = 0;
  data.datasets.forEach((dataset)=>{
    var maximum =  Math.max(...dataset["data"]);
    max = Math.max(maximum, max)})
  return max+10
}
var ctx = document.getElementById("prChart");
var prChart = new Chart(ctx, {
    type: 'line',
    data: prdata,
    options: {
      scales: {
        yAxes: [{
          ticks: {
            min: 0,
            max: getMaxOf(prdata)
          }
        }]
      }
    }
});


function generateHostpotsLi(hostpotsList){
  var out = "";
  hostpotsList.forEach(function(element){
    out+="<tr><td>"+element.name+"</td><td>"+element.value+"</td></tr>"
  })

  if (out === ""){
    out = "No files modified in this timeframe"
  }
  return out
}

function generateComittersLi(comittersList){
  var out = "";
  comittersList.forEach(function(element){
    out+="<tr><td>"+element.name+"</td><td>"+element.commits+"</td></tr>"
  })

  if (out === ""){
    out = "No commits in this timeframe"
  }
  return out
}

function generateStaleBranchesLi(branchesList){
  var out = "";
  branchesList.forEach(function(element){
    out+="<tr><td>"+element.name+"</td><td>"+element.lastCommit+"</td><td>"+element.lastAuthor+"</td></tr>"
  })
  return out
}


//document.getElementById("date").innerHTML = "Generated " + teamdata.generation_date ;
//document.getElementById("branches").innerHTML = teamdata.branches_number + " stale: " + teamdata.stale_branches.length;
//document.getElementById("most_active").innerHTML = generateComittersLi(teamdata.top_committers)
//document.getElementById("most_active_3m").innerHTML = generateComittersLi(teamdata.top_committers_3m)
//document.getElementById("stale_branches").innerHTML = generateStaleBranchesLi(teamdata.stale_branches)


document.getElementById("name").innerHTML = teamdata.name;
document.getElementById("h1").innerHTML = teamdata.name + ' statistics';
document.getElementById("title").innerHTML = teamdata.name;

//
//document.getElementById("hotspots").innerHTML = generateHostpotsLi(teamdata.heatmap)
//document.getElementById("hotspots3m").innerHTML = generateHostpotsLi(teamdata.heatmap_3m)
