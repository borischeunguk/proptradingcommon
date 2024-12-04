# proptradingcommon
Common code for prop trading
```
Requirements:
    tested on python 3.9.16
    Trader Workstation (TWS) is required to run the code
    Please refer to TWS API documentation for more details
     https://interactivebrokers.github.io/tws-api/
 
Steps to create python virtual env:
    python3.9 -m venv <yourvirtualenvname>
    source <yourvirtualenvname>/bin/activate

interactivebrokerscripts
    example code to download historical data from interactive broker
    
ssh setup command: 
    ssh-keygen -t ed25519 -C "example.email@icloud.com"
    cat example_github_ssh.pub
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/example_github_ssh
    ssh -T git@github.com
    
    git remote -v
    git remote set-url origin git@github.com:borischeunguk/proptradingcommon.git
    ssh-add -l
    ssh-add /Users/xinyue/.ssh/borischeunguk_github_ssh
    git push origin master
    
twsapi_macunix
    example code about IBKR API for Mac
```