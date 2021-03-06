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
    data: timedata,
    options: {
      scales: {
        yAxes: [{
          ticks: {
            min: 0,
            max: getMaxOf(timedata)
          }
        }]
      }
    }
});


var ctx1 = document.getElementById("medianChart");
var medianChart = new Chart(ctx1, {
    type: 'line',
    data: mediandata,
    options: {
      scales: {
        yAxes: [{
          ticks: {
            min: 0,
            max: getMaxOf(mediandata)
          }
        }]
      }
    }
});

function generateCommittersLi(committersList){
  var out = "";
  committersList.forEach(function(element){
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
  if (out == ""){
    out = "<tr><td>No stale branches found</td><td></td></tr>"
  }
  return out
}

function generateStaleBranches(repositories){
  var out = "";
  repositories.forEach(function(element){
    out += "<th>" + element.name + "</th>"
    out+= generateStaleBranchesLi(element.stale_branches)
  })
  return out
}

function generateMembersList(membersList){
  var out = "";
  membersList.forEach(function(element){
    out+="<p class = \"member\">&nbsp;"+ element.name + "&nbsp;<p>"
  })
  return out
}

function generateTopCommittersLi(hostpotsList){
  var out = "";
  hostpotsList.forEach(function(element){
    out+="<tr><td>"+element.name+"</td><td>"+element.commits+"</td></tr>"
  })

  if (out === ""){
    out = "<tr><td>No files modified in this timeframe</td><td></td></tr>"
  }
  return out;
}

function generateTopCommitters3m(repositories){
  var out = "";

  repositories.forEach(function(element){
    out += "<th>"+element.name+"</th>"
    out += generateTopCommittersLi(element.top_committers_3m)
  })

  return out;
}

function generateTopCommitters(repositories){
  var out = "";

  repositories.forEach(function(element){
    out += "<th>"+element.name+"</th>"
    out += generateTopCommittersLi(element.top_committers)
  })

  return out;
}

function generateMedians(current_medians){
    var out = "";
    current_medians.forEach(function (element){
        var keys = Object.keys(element);
        keys.forEach(function(key_element){
            out += "&nbsp;<div>" + key_element + ": " + element[key_element] + "</div>&nbsp;"
        })
    })
    return out;
}

function generateHostpotsLi(hostpotsList){
  var out = "";
  if (hostpotsList){
      hostpotsList.forEach(function(element){
        out+="<tr><td>"+element.name+"</td><td>"+element.value+"</td></tr>"
      })
      if (out === ""){
        out = "<tr><td>No files modified in this timeframe</td><td></td></tr>"
      }
      return out
  }
  return "<tr><td>No files modified in this timeframe</td><td></td></tr>"
}

function generateHotspots3m(repositories){
  var out = "";

  repositories.forEach(function(element){
    out += "<th>"+element.name+"</th>"
    out += generateHostpotsLi(element.heatmap3m)
  })
  return out;
}

function generateHotspots(repositories){
  var out = "";

  repositories.forEach(function(element){
    out += "<th>"+element.name+"</th>"
    out += generateHostpotsLi(element.heatmap)
  })
  return out;
}

document.getElementById("members").innerHTML = generateMembersList(teamdata.members)
document.getElementById("name").innerHTML = teamdata.name;
document.getElementById("h1").innerHTML = teamdata.name + ' statistics';
document.getElementById("title").innerHTML = teamdata.name;
document.getElementById("topcommitters3m").innerHTML = generateTopCommitters3m(teamdata.repositories)
document.getElementById("topcommitters").innerHTML = generateTopCommitters(teamdata.repositories)
document.getElementById("stale").innerHTML = generateStaleBranches(teamdata.repositories)
document.getElementById("medians").innerHTML = generateMedians(teamdata.current_medians)
document.getElementById("heatmap").innerHTML = generateHotspots(teamdata.repositories)
document.getElementById("heatmap3m").innerHTML = generateHotspots3m(teamdata.repositories)