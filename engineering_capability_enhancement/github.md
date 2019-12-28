## 基本操作
- 增删改  
  1. git add file  
  2. git commit -m <descrption>

- 查  
  1. git status   --- 查看仓库状态  
  2. git diff  file     ---- 查看文件修改内容.file 可选~若不填，则显示全部修改

- 撤销  
  git checkout -- filename


- 代码回退  
   1. git log  （--pretty=oneline）--- 查看提交日志和commit id  
   2. git reset --hard HEAD  --- 回退第一个提交  
   3. git reset --hard commitID  --- 回退该commitID前的全部提交  

- 回退的回退  
  git reflog  

- 改了又改  
  git commit -a -- amend  

## 分支创建  
- 1. 创建并切换分支  
  git checkout -b branch_name

- 2. 查看当前分支  
  git branch

- 3. 切换分支  
  git checkout branch_name

- 4. 合并分支  
  git merge branch_name

- 5. 删除分支  
  git branch -d branch_name


## 分支管理

1. master 分支 --- stable分支，所有软件版本都从master出

2. dev 分支 --- 开发分支, 用来开发的分支,需要发布版本时, 将dev分支像master分支合并

3. 个人本地分支 ---- 个人开发分支，开发完毕后合并到dev分支

4. 修复bug时, 切回待修复分支, 创建bug分支,修改然后merge~


## 多人协作

1.查看远程仓库  
  git remote -v

2.查看远程分支  
  git branch -r

3.在本地拉取远程分支  
 git checkout -b remote_branch_name  origin/remote_branch_name

**work-flow:**

1. 查看远程分支

2. 本地建立需要修改的远程分支

3. 进行需求开发或者bug修复

4. git push origin remote_branch_name

5. 如果冲突~git pull同步远程分支

6. git diff 查看冲突内容,修复冲突，重新git push

**高频秘籍**

工作中常见场景:  
        正在开发需求~突然来了一个紧急bug~开发的代码要怎么办?

1. git diff  commiitID >  diff.patch 将修改内容打成一个diff.patch

2. 切出去修bug

3. bug休完 执行 git apply diff.patch

但是diff.patch 会被我们误删除~~~ 这个时候就很痛苦~

git stash 命令闪亮登场~~~

1. git stash

2.切出去改bug

3.切回来,git stash pop

在A分支修的Bug如何merge到B分支呢?

在B分支上执行 git cherry-pick commitId

1.sourcetree  ---  超级好用~~ 支持mac和windows~
https://www.sourcetreeapp.com/

2.gerrit --- 代码仓库管理工具~~~基本每个公司都有~~可以用来code review和构建自动化流水线  
https://www.gerritcodereview.com/  
https://www.jianshu.com/p/b77fd16894b6  


