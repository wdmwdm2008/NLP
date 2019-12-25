## Linux常用命令

- 文件相关命令  
  ls: 列出当前目录文件  
  ls -l: 列出当前目录文件及文件属性,权限等数据  
  ls -a: 列出当前目录文件(包含隐含文件)  

  cp: 复制文件或目录  
  cp source_file target_file  
  cp -r source_dir target_dir  

  rm: 删除文件  
  rm -r:删除目录及文件  

  cat: 展示全部内容  
  cat -n file_name  

  翻页查看文件内容：  
  more/less file_name  

  数据选取:  
  head -n number file_name: 只选取前几行  
  tail -n number file_name: 只选取后几行  
  **tail -f file_name: 持续查看file的输出(超高频)**  

  文件查找：  
  find/whereis file/dir： 查找文件/目录  
  locate keyward  

  压缩解压：  
  tar zxvf filename.tar.gz  
  tar zcvf filename.tar.gz DirName  

  如果需要bz2格式的文件，讲z改写为j  


- 权限相关命令  
  chmod:改变文件/目录的读写执行权限  
  读：r -- 4  
  写：w -- 2  
  执行：x -- 1  
  可读可写可执行： 4 + 2 + 1 = 7  
  chmod  [-R]  xyz file/dir

  chown:改变文件所有者
  chown  [-R] user:group file/dir


- 字符串相关命令
  - 字符串选取:grep str file
  - 排序命令:sort file or stdin
  - 去重命令:uniq [-ic]  -i:忽略大小写 –c:进行计数
  - 统计命令:wc [-lwm] –l:统计行数 –w:统计词频 –m:统计字符数




- 系统信息相关命令
  - top
  - ps
  - ps -ef： 查看进程
  - pstree
  - kill
  - free      


## 常见问题分析

- 功能问题

  - 实际表现:功能最终结果与预期不同
  - 可能原因:
    1. 需求理解不到位
    2. 代码实现存在问题  
    3. 在某些特殊场景下功能不可使用  
  - 出现阶段:
    1.需求验收阶段
    2.线上服务阶段

  - 解决思路:
    1. 通过日志记录定位到问题所在  
    2. 通过问题分析找到根因并制定解决方案  
    
  - 实例现象:  
    在某次请求过程中,无法读取到缓存数据.
    
    
- 性能问题
    实际表现:  
      系统响应时间与预期不符  
      系统吞吐量与预期不符  

    可能原因:  
      1. 系统资源问题  
      2. 高流量高并发冲击下暴露的问题  
      3. 特殊场景问题  

    出现阶段:
      1.线上服务阶段  

    解决思路:
      1. 资源问题 --- 通过linux命令观察系统资源变化
      2.特殊场景需要构造和稳定复现该场景
    实例现象:  
      系统在某一天的固定时刻会出现OOM.   

- 稳定性问题

  实际表现:服务无法正常工作

  可能原因:
    1.硬件及系统资源
    2.系统设计及编码

   出现阶段:
     1.需求验收阶段

    解决思路:
      1. 先确实是否是资源问题
      2. 看出现场景和频率

    实例现象:  
      系统在压测过程中经常出现coredump.  



## 代码风格与代码质量

- Google Code Style  
https://zh-google-styleguide.readthedocs.io/en/latest/

- PEP8  
https://docs.bk.tencent.com/code/PEP8.html

- 静态检查工具  
Lint、Compile Warning、Coverity、Fortify

