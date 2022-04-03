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

var ctx3 = document.getElementById("mergeChart");
var mergeChart = new Chart(ctx3, {
  type: 'line',
  data: mergedata,
  options: {
    scales: {
      yAxes: [{
        ticks: {
          min: 0,
          max: getMaxOf(mergedata)
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


document.getElementById("date").innerHTML = "Generated " + repodata.generation_date ;
document.getElementById("owner").innerHTML = repodata.owner;
document.getElementById("total_prs").innerHTML = repodata.total_prs;
document.getElementById("open_prs").innerHTML = repodata.total_open_prs_now;
document.getElementById("long_living_prs").innerHTML = repodata.open_prs_long_living_now;
document.getElementById("created").innerHTML = repodata.created_at;
document.getElementById("branches").innerHTML = repodata.branches_number + " stale: " + repodata.stale_branches.length;
document.getElementById("most_active").innerHTML = generateComittersLi(repodata.top_committers)
document.getElementById("most_active_3m").innerHTML = generateComittersLi(repodata.top_committers_3m)
document.getElementById("stale_branches").innerHTML = generateStaleBranchesLi(repodata.stale_branches)

if(repodata.oldest_pr_link!=null){
  document.getElementById("oldest_pr_link").href = repodata.oldest_pr_link;
  document.getElementById("oldest_pr_link").innerHTML = "Oldest PR, age:" + repodata.oldest_pr_age;
}else{
  document.getElementById("oldest_pr").innerHTML = "No open PRs";
}
document.getElementById("name").innerHTML = repodata.name;
document.getElementById("h1").innerHTML = repodata.name + ' statistics';
document.getElementById("title").innerHTML = repodata.name;

document.getElementById("hotspots").innerHTML = generateHostpotsLi(repodata.heatmap)
document.getElementById("hotspots3m").innerHTML = generateHostpotsLi(repodata.heatmap_3m)
