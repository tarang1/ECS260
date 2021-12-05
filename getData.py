from github import Github
import os
from pprint import pprint
import requests
from datetime import datetime

project_list = ["apache/beam",
"apache/iceberg",
"apache/arrow",
"apache/flink",
"apache/druid",
"apache/hadoop",
"apache/tvm",
"apache/cassandra",
"apache/kafka",
"apache/hudi",
"apache/incubator-mxnet",
"apache/pinot",
"apache/trafficserver",
"apache/nifi",
"apache/libcloud",
"apache/cordova-ios",
"apache/solr",
"apache/arrow-rs",
"apache/camel",
"apache/incubator-nuttx",
"apache/lucene",
"apache/shardingsphere",
"apache/rocketmq",
"apache/cloudstack",
"apache/groovy",
"apache/zeppelin",
"apache/ignite",
"apache/dubbo",
"apache/skywalking",
"apache/hive",
"apache/jclouds",
"apache/avro",
"apache/skywalking-java",
"apache/arrow-datafusion",
"apache/lucene-solr",
"apache/storm",
"apache/thrift",
"apache/parquet-mr",
"apache/superset",
"apache/apisix",
"apache/incubator-shenyu",
"apache/cordova-plugin-camera",
"apache/phoenix",
"apache/activemq-artemis",
"apache/cxf",
"apache/impala",
"apache/ozone",
"apache/bigtop",
"apache/maven-surefire",
"apache/cordova-docs"]

def get_merged_PRs(contributor,repo_name):
    search_url = "https://api.github.com/search/issues?q=is:pr+is:merged+repo:" + repo_name + "+author:" + contributor + "&per_page=100"

    prs = requests.get(search_url).json()
    list_of_sha = []
    for pr in prs['items']:
        pulls_url = "https://api.github.com/repos/" + repo_name + "/pulls/" + str(pr['number'])
        sha = requests.get(pulls_url).json()
        list_of_sha.append(sha['head']['sha'])
    return list_of_sha

def get_dict(token, start, end, dct) :
    #print(token)
    g = Github(token)
    #repos = ['apache/kafka','misterokaygo/MapAssist']
    #d10_20 = {}
    for each_repo in project_list[start:end]:
        dct[each_repo] = {}
        repo = g.get_repo(each_repo)
        print(repo.contributors_url)
        #print(repo.contributors_url.count)
        print(g.rate_limiting)
    #repo = g.get_repo('misterokaygo/MapAssist')
        urls = repo.contributors_url + '?per_page=100'
        print(type(urls))
        #commits = repo.get_commits(author='niket-goel')
        #fc = list(commits)[6]
        #print(list(commits)[0])
        #author = repo.get_commit(commits[1].sha).author
        #print(author)
        # for each_commit in commits:
        #     print("******", each_commit)
        #print(repo.commits_url)
        issues_url = repo.issues_url[:-16]
        #print(repo.full_name)
        #print(len(issues_url))
        dct[each_repo]['issues'] = requests.get(issues_url).json()['open_issues_count']
    #print(dct)
        r = requests.get(urls)
        j = 0
        if len(r.links) !=0:
            max_page = int(r.links.get('last')['url'].split('=')[-1])
        else:
            max_page =1
        print(type(max_page))
        #dct[each_repo]['contributors'] = []
        dct[each_repo]['contributors'] = {}
        while(j<max_page):
            r = requests.get(urls)
            # print(r.links)
            # print(int(r.links.get('last')['url'].split('=')[1]))
            #print(r.headers['Link'])
            #r2 = requests.get(issues_url)
            #print(r2.text)
            # commits = repo.get_commits(author='junrao')
            # print(commits.totalCount)
            # print(len(list(commits)))
            # first_commit_time = (list(commits)[commits.totalCount - 1]).last_modified
            # last_commit_time = (list(commits)[0]).last_modified
            # print('ableegoldman', 'first commit time:' + first_commit_time, 'last_commit_time:' + last_commit_time)
            # break
            for i in r.json():
                #print(i)
                if(i == 'message'):
                    print('FO')
                    print(r.json()[i])
                else:
                    print(i['login'])
                    dct[each_repo]['contributors'][i['login']] = {}
                    urls = repo.contributors_url
                    shas = get_merged_PRs(i['login'],each_repo)
                    print(shas)
                    print(urls)
                    #commits = repo.get_commits(author=str(i['login']))
                    commits = repo.get_commits(author=str(i['login']))
                    print(commits.totalCount)
                    if len(list(commits)) == 0:
                        continue
                    #print(commits.totalCount)
                    #print(len(list(commits)))
                    dct[each_repo]['contributors'][i['login']] = {}
                    first_commit_time = (list(commits)[len(list(commits))-1]).last_modified
                    last_commit_time = (list(commits)[0]).last_modified
                    d1 = datetime.strptime(last_commit_time,'%a, %d %b %Y %H:%M:%S GMT')
                    d2 = datetime.strptime(first_commit_time,'%a, %d %b %Y %H:%M:%S GMT')
                    dct[each_repo]['contributors'][i['login']]['lifespan'] = (d1-d2).days + 1
                    dct[each_repo]['contributors'][i['login']]['commits'] = commits.totalCount
                    print((d1-d2).days)
                    #print(i['login'],'first commit time:'+first_commit_time, 'last_commit_time:'+last_commit_time )
            if r.links.get('next'):
                urls = r.links.get('next')['url']
            j += 1
    print(dct)
    return dct


token = os.getenv('GITHUB_TOKEN', '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')
dict_test={}
get_dict(token,5,10,dict_test)


