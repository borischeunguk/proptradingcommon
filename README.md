# proptradingcommon
Common code for prop trading
```
China Stock Future Market Data:
    1. Sample Data available in resources/china_stock_futures_1min
    2. Full 202411 data available in Baidu Netdisk as follows:
        通过网盘分享的文件：10-11月1min股指期货数据.zip
        链接: https://pan.baidu.com/s/1zQkb_-28llTPP4R-xSPsKg?pwd=qeqg 提取码: qeqg 
        --来自百度网盘超级会员v6的分享

Requirements:
    tested on python 3.9.16
    Trader Workstation (TWS) is required to run the code
    Please refer to TWS API documentation for more details
     https://interactivebrokers.github.io/tws-api/
 
Steps to create python virtual env:
    python3.9 -m venv <yourvirtualenvname>
    source <yourvirtualenvname>/bin/activate
    pip install -r requirements.txt

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