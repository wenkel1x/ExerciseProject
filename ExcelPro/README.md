# ExerciseProject
### 当前项目用于统计 Execel 特定cell的数据,具体用法如下:

* 统计Excel文件路径: 输入收集文件的文件路径，包括导出的文件和要统计的文件，除此外非必要不要放置额外文件.
* 开始月份: excel文件中统计的rack列开始月份，一般为当前月份,除非月初时统计有上个月数据.
* 统计月份个数: 需要向后看几个月的数据,一般为向后统计4个月的交期.
* 编辑配置文件：非必要不修改, 被统计文件格式应参考`FAB model`.
* Excel表格sheet应以厂区名命名, 如`QMF QCG QMN`, 所有表格sheet名称应注意不能有空格.sheet表格内的区分月份的表头应放在第一行.AMA表头是在第二行且格式不一样,需要修改。例: `Apr May Jun Jul Apr MB QTY May MB QTY Jun MB QTY Jul MB QTY`

#### 配置文件详解:
```json
{
    "output_sheet_name":"Loading",
    "fac_name":["QMF","QMN","QCG"],
    "model_name":["FAB","MSF","AMA","QCT","NTA","SEL"],
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
}
```
| 字段名 | 说明           |
|--------|-----------------|
| output_sheet_name   | 输出excel sheet名称`loading` |
| fac_name    | 厂区名称 对应loading表格中厂区列|
| model_name  | excel数据源表格名称`FAB,MSF,AMA,QCT,NTA,SEL`,名称需包含关键字|
|export_loading_index| 输出数据到loading表格对应的行号，列为月份|
|FAB    | FAB execl表中sheet `QMF,QMN,QCG`|
|└─rack_key_word | 抓rack数据 列头关键字(默认): `currency_month_abbr` 或 `选取的开始月份`.|
|└─server_key_word|抓server数据 列头关键字(默认)`currency_month_abbr` Server QTY 或 `选取的开始月份` Server QTY |
|└─MB_key_word|抓MB数据 列头关键字(默认)`currency_month_abbr` Server QTY 或 `选取的开始月份` MB QTY |
|└─SB_key_word|抓SB数据 列头关键字(默认)`currency_month_abbr` Server QTY 或 `选取的开始月份` SB QTY|
|AMA|同FAB|
|MSF|同FAB|
|QCT|同FAB|
|NTA|同FAB|
|SEL|同FAB|

#### 抓不到数据请检查excel表格式是否与FAB相同，此代码根据FAB excel统计表格式所制作。