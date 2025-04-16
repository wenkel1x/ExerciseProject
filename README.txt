# ExerciseProject
# for collect some Excel data
# 统计Excel文件路径: 输入收集文件的文件路径，包括导出的文件和要统计的文件，除此外非必要不要放置额外文件
# 开始月份: excel文件中统计的rack列开始月份，一般为当前月份,除非月初时统计有上个月数据。 
# 统计月份个数: 需要向后看几个月的数据,一般为向后统计4个月的交期
# 编辑配置文件：非必要不修改
# 被统计文件格式应参考FAB model, Excel 表格sheet应以厂区名命名,如QMF QCG QMN, 所有表格sheet名称应注意不能有空格
# sheet 表格内的表头应放在第一行 Apr	May	Jun	Jul	  Apr MB QTY	May MB QTY	 Jun MB QTY	  Jul MB QTY. 注意AMA 表头是在第二行且格式不一样。
配置文件详解：
"output_sheet_name":"Loading by model", #输出文件到loading sheet的名称,也可更改为Loading by Output
"fac_name":["QMF","QMN","QCG"],  #loading A列合并单元格的所有名称
"model_name":["FAB","MSF","AMA","QCT","NTA","SEL"], #loading B列所有名称合集
#export_loading_index 是loading表格输出的行索引，以QMF FAB:{"rack":3,"server":4,"mb":5,"sb":6,"fa":8}为例：rack loading为第三行，server load为第四行,以此类推。后续可根据实际行号更改
"export_loading_index":{
    "QMF":{
        "FAB":{"rack":3,"server":4,"mb":5,"sb":6,"fa":8},
        "MSF":{"rack":10,"server":11,"mb":12,"sb":13},
        "QCT":{"rack":15,"server":16},
        "NTA":{"rack":18,"server":19}
    },
    "QMN":{
        "FAB":{"rack":21,"server":22,"mb":23,"sb":24},
        "AMA":{"rack":26,"server":27,"mb":28,"sb":29},
        "SEL":{"rack":32,"server":33,"mb":34,"sb":35}
    },
    "QCG":{
        "FAB":{"rack":37,"server":38,"mb":39,"sb":40},
        "AMA":{"rack":42,"server":43,"mb":44,"sb":45},
        "MSF":{"rack":47,"server":48,"mb":49,"sb":50}
    }
},

#后续为要统计表格列的关键词，当前默认是空值，当为空时程序默认抓取rack列即输入的开始月份,例如 Apr.
#rack_key_word="Apr"
#server_key_word="Apr Server QTY"
#MB_key_word="Apr MB QTY"
#SB_Key_word="Apr SB QTY"
#后续以此类推，后面如果统计表更改可以填入更改的列名称
"FAB":{
    "rack_key_word": "",
    "server_key_word": "",
    "MB_key_word": "",
    "SB_Key_word": ""
},
"AMA":{
    "rack_key_word": "",
    "server_key_word": "",
    "MB_key_word": "",
    "SB_Key_word": ""
},
"MSF":{
    "rack_key_word": "",
    "server_key_word": "",
    "MB_key_word": "",
    "SB_Key_word": ""
},
"QCT":{
    "rack_key_word":"",
    "server_key_word": "",
    "MB_key_word": "",
    "SB_Key_word": ""
},
"NTA":{
    "rack_key_word":"",
    "server_key_word": "",
    "MB_key_word": "",
    "SB_Key_word": ""
},
"SEL":{
    "rack_key_word":"",
    "server_key_word": "",
    "MB_key_word": "",
    "SB_Key_word": ""
}