# AI工具-自动化采集页面数据工具
### 1.先安装环境：（当前目录运行管理员cmd）
```bash
pip install -r requirements.txt
```
### 2.运行[gemini_login.py](gemini_login.py)后先扫码登录根据提示操作：
```bash
python gemini_login.py
```
### 3.运行[gemini_server.py](gemini_server.py)主程序根据提示查看[Gemini.md](Gemini.md)：
```bash
python gemini_login.py
```

### 4.查看[Gemini.md](Gemini.md)数据：
```commandline
{
  "products": [
    {
      "store_name": "天猫超市",
      "product_name": "娃哈哈纯净水596ml*24瓶整箱装开会出行小瓶饮用非矿泉水哇",
      "price": "￥32.8",
      "discounted_price": "￥59",
      "quantity": "15.305kg",
      "specifications": "限购99件",
      "promotions": [
        "信用卡支付",
        "直降26.2元",
        "15天价保",
        "次日达",
        "破损包退",
        "极速退款"
      ],
      "image_url": "//gw.alicdn.com/imgextra/i3/6000000000195/O1CN0115J6NE1DJMJ82VXln_!!6000000000195-0-sm.jpg"
    },
    {
      "store_name": "天猫超市",
      "product_name": "可心柔婴儿云柔巾40抽40包",
      "price": "￥79.01",
      "discounted_price": "￥89.9",
      "quantity": "2.24kg",
      "specifications": "聚划算 8月31日23:59结束",
      "promotions": [
        "信用卡支付",
        "直降10元",
        "消费券",
        "次日达",
        "破损包退",
        "极速退款"
      ],
      "image_url": "//gw.alicdn.com/imgextra/i4/6000000004688/O1CN01KHgmHk1kV9peffXZC_!!6000000004688-0-sm.jpg"
    },
    {
      "store_name": "天猫超市",
      "product_name": "babycare婴儿小熊巾面膜柔巾加厚干湿两用绵柔巾非棉柔巾非湿巾",
      "price": "￥86.9",
      "discounted_price": "￥109.9",
      "quantity": "2.636kg",
      "specifications": "包数：1组，颜色分类：【小熊巾升级款】80抽*12包",
      "promotions": [
        "信用卡支付",
        "直降22元",
        "消费券",
        "次日达",
        "破损包退",
        "极速退款"
      ],
      "image_url": "//gw.alicdn.com/imgextra/i3/725677994/O1CN01fUYEF328vJBZBGtJQ_!!725677994.png"
    },
    {
      "store_name": "天猫超市",
      "product_name": "可心柔母婴云柔保湿纸巾100抽64包",
      "price": "￥244.61",
      "discounted_price": "￥319.8",
      "quantity": "10.452kg",
      "specifications": "包数：64包",
      "promotions": [
        "信用卡支付",
        "直降27元",
        "消费券",
        "次日达",
        "破损包退",
        "极速退款"
      ],
      "image_url": "//gw.alicdn.com/imgextra/i3/6000000006060/O1CN014iKm2Y1udXEZsvUUG_!!6000000006060-0-sm.jpg"
    },
    {
      "store_name": "无卡工坊旗舰店",
      "product_name": "【整箱囤货微瑕】无卡工坊冰淇淋香草味苏打气泡水0糖0卡无糖饮料",
      "price": "￥43.65",
      "discounted_price": "￥45",
      "quantity": "距加入降￥1.35",
      "specifications": "口味：【网红爆品】冰淇淋香草苏打气泡水330mL*24罐",
      "promotions": [
        "信用卡支付",
        "6期免息",
        "满2件9.5折",
        "淘金币",
        "破损包退",
        "极速退款",
        "7天无理由退换"
      ],
      "image_url": "//gw.alicdn.com/imgextra/i4/2212886586528/O1CN01gmf2MP1y5sN5zoBYI_!!2212886586528.jpg"
    }
  ],
  "summary": {
    "total_products": 5,
    "total_price": "￥0",
    "promotions": [
      "部分商品满2件打9.50折"
    ]
  }
}
```