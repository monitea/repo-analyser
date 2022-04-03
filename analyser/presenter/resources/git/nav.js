function getLinks(){
    links_text = ""
    if (links) {
        links_text = "<a href=\"" + links.repository_statistics_github_pages + "\">Repository statistics github pages</a>\n"
        links_text += "<a href=\"" + links.repository_statistics_jenkins + "\">Repository statistics jenkins job</a>\n"
        return links_text
    }
    else return ""
}


document.getElementById("nav").innerHTML = getLinks() ;