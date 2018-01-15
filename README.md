# NYC-Taxi

data source: https://www.kaggle.com/c/nyc-taxi-trip-duration/data
參考分析資料: https://www.kaggle.com/headsortails/nyc-taxi-eda-update-the-fast-the-curious
NYC Taxi EDA - Update: The fast & the curious?
https://www.kaggle.com/headsortails/nyc-taxi-eda-update-the-fast-the-curious

【想法】關於散布圖
1. 由圖，粗估速率大概在15-72 km/hr
分析造成速率差距這麼大的主因是
(1) 距離其實不準，直線或對角線的部分，如果實際是走兩邊和的直線但我們的最短距離是採對角線(直覺的兩地直線距離)，就會造成推估的時速偏快。
→也許可以由那個powerful的地圖網站，算一般開車會走的距離，但他的API不知道要怎麼用，如果要研究很久或太難取得的話，這個方案勢必得放棄。
OSRM website(return duration time) Open Source Routing Machine:
http://map.project-osrm.org/?z=8&center=58.325357%2C-105.342407&loc=58.836490%2C-104.166870&loc=58.342659%2C-104.326172&hl=en&alt=0
=> 想放棄 QQ


(2) 上車地點，因為我們的資料分佈大抵只有在
A. 曼哈頓區
B. 機場(John F. Kennedy International Airport) JFK Airport Latitude/Longitude: 40.6441666667, -73.7822222222
C. 機場(LaGuardia Airport) LGA Latitude/Longitude: 40.7769271,-73.87396590000003
推測在機場上/落車的人，目的都是去/來自曼哈頓，這樣也許會開比較久，要由「經緯度」去取，來做推測是否正確的 ##驗證。
他有兩個機場 半徑都取4.5km?當作機場範圍

機場:以機場為中心，取適當距離，範圍內都當做是機場


(3) 在不改距離的前提下，分析資料，研究時速的差異來自何處

=> 先把尖峰時刻的因素加上去
現在有個小問題 尖峰時間有分 第一大尖峰 大二大....
尖峰時間=時速慢??? ##驗證
TLC的統計資料 尖峰的時段 https://www.quora.com/What-times-are-considered-rush-hour-in-New-York-City
平日: 7,8,9,18,19,20
星期六: 0,1,18,19,20,22,23
星期日: 0,1,17,18,19
後來決定畫一週每日每時的speed比較，看是否與TLC的載客量趨勢吻合


機場 <-> 曼哈頓地區
	(情況一)將大尖峰時間的資料取出算平均時速
	(情況二)將小尖峰時間的資料取出算平均時速
	(一二結合?但可能會猜得比較不準)
	--> 猜測這邊不用考慮人數因素
	
曼哈頓地區內移動
	(面向一)如上，分別計算大小尖峰平均時速
	(面向二)人數和搭乘時間是否有直接關係
	-->看單一面向or兩個一起考慮


(4) 或取平均時速，直接assign給未知值（想必結果應該很不好，但想不出方法可以先這樣交差）
=> 懶惰的方法覺得可以~ (備案咩~)


(5) 加入尖峰時刻可能開比較慢，或者特定經緯度會塞車等條件(研究POI?)
=> ㄅ是很想研究POI, 頂多加尖峰時刻(懶惰鬼)


(6) "人數"越多開越久，所以對於時間上的影響力也加進去(？)
=> 一定正相關 but i don't know how QQ (思考中)

