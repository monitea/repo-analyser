This software does statistical analysis of git and github-based repositories.
It will accept a list of repositories to analyse (with credentials if necessary) and talk both to github and check out code to do analysis.

# Logic
While some of those statistics can be obtained from github or git, it is not very simple and not really team oriented.
This software allows you to understand trends happening 

# Input data and formats
Configuration files must be placed in `analyser/input` folder.
Following files are allowed:
1. `repos.json`
This expects you to define following entries:
 ```json
[
    {
        "server": "github.com",
        "api": "api.github.com/graphql",
        "owner": "organization",
        "name": "org-repo",
        "token":"<token_with_repo_access>",
        "protocol": "https",
        "ignore_list": [ "pom.xml", "yarn.lock", "package.json", "package-lock.json" ], //files in your repo to ignore during analysis
        "long_living_branches": ["develop","master"], //long living branches of your repo, will never be marked as stale, they are also counted as a separate data point when analysing PR statistics
        "main_branches": ["production"], //main branches of your repo, will never be marked as stale 
        "stale_branch_after": 30 //days of no activity after which branch is set to stale
    },
      {
        "server": "github.com",
        "api": "api.github.com/graphql",
        "owner": "user",
        "name": "user-repo",
        "token":"<token_with_repo_access>",
        "protocol": "https",
        "ignore_list": [ "pom.xml", "yarn.lock", "package.json", "package-lock.json" ],
        "long_living_branches": ["develop","master"],
        "main_branches": ["production"],
        "stale_branch_after": 30
    }
]
```
2. `teams.json`
```json
[
    {
      "name": "Team1", 
      "color": "#1A8FE3", //color to be used when drawing graphs
      "members": [
        {
          "name": "John",
          "email": "john@mail.com",
          "login": "johnny"
        },
        {
          "name": "Jane",
          "email": "jane@gmail.com",
          "login": "jane-coder"
        }
      ]
    }  
]
```
3. `mailmap` file in ```.mailmap``` format that will be used as default mailmap if no mailmap file is available in your repository. See https://git-scm.com/docs/gitmailmap. Optional. If your repository contains its own `.mailmap` file, it will be used. If your repository does not have `.mailmap`
file, but you provide `mailmap` file in `input` folder, this will be used. Not providing `.mailmap` file may result in confusing results, as different user emails will be recognized as different users. See linked document. `Here file name must be WITHOUT leading dot`

# Folder structure
`data_loader` python sources for analyser
`input` configuration files go here
`input_samples` self explanatory
`output` results of analyser will go here
`presenter` python sources for report generation. If you want to implement your own, feel free to use data from `output` folder.\
`reports` HTML reports generated by presenter go here

# Running
Using `analyser` as root folder, start `analyser.py` script.
It will check out the repository into `repos` folder and run analysis using both git and github capabilities.

Once the analysis is completed, run `presenter.py` script to generate html reports.

If you don't want to use defualt reports, feel free to use extracted data placed in `output` folder to create your own reports.

# Using with docker
It is recommended to mount both `input` and `reports` folders into your image for easy configuration and report storage.

# Known issues and quirks
To perform the analysis, this software must check out the repository being analysed.
At the moment the `repos` folder, where repositories to analyse are placed, is not being cleaned up. If you want to 
analyse multiple large repositories, be mindful of available space.

# So how does it look like?
See it for yourself, [sample_report](sample_report.zip) is there for you.

It contains analysis executed on cypress repo with two main committers added in a sample team.