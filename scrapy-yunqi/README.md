# scrapy-yunqi
这是根据书上scrapy分布式爬虫 写的 使用了 mongodb复制集群 redis去重
这里的redis 是根据书上介绍使用了 一个github开源别人编写的redis 
最终结果 有bookInfo中一千多条重复的  在bookhot中基本没有重复  
使用一些方法去重 mongodb去重 

  
##3.下面提供一种比较简单的巧方法：

    将数据导出为JSON格式存档：
    mongoexport.exe -d database_name -c collection_name -o filename.json
    清空当前集合的数据：
    db.yourcollection.remove({})
    新建唯一索引：
    db.yourcollection.createIndex({public_no:1}, {unique:true})
    导入之前存档的JSON文件数据：
    mongoimport -d database_name -c collection_name --upsert filename.json
    用到的几个参数选项说明：-d 数据库名 -c 集合名 -o 导出后的目录及文件名 --upsert 会根据唯一索引去掉重复记录

