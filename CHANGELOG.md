# 版本修改紀錄

## v2.0 (2019-04-12)
* 修改各程式輸出格式
* 資料庫模組：get_examinee_info() 更名 print_examinee_info()
* 資料庫模組：新增 sql_case_type() 轉換題型名稱
* 資料庫模組：新增 show_one_score() 顯示一筆成績
* 更新使用說明分頁
* 更新程式碼分頁
---

## v1.9 (2019-01-16)
* 刪除 words_in.txt / cleanup.py / words_out.txt
* 單字表改用 toeic-words.txt
---

## v1.8 (2017-10-30)
* 測驗中心/參測考生：修改為類別，函式加上註解
* 資料庫類別設定 Context Manager
---

## v1.7 (2017-10-30)
* 參測考生：完成選擇題測驗 test_multiple_choice()
* 參測考生：完成填充題測驗 test_fill_in_the_blank()
* 參測考生：完成個人成績查詢 score_list()
* 參測考生：登入後選單顯示帳號 show_menu()
* 測驗中心：完成測驗成績統計 summary()
* 測驗中心：完成個人成績查詢，可用帳號模糊查詢 score_list()
* 測驗中心/參測考生：分隔線符號改用 '='
---

## v1.6 (2017-10-30)
* 測驗中心：完成選擇題型設定 set_multiple_choice()
* 測驗中心：完成填充題型設定 set_fill_in_the_blank()
* 參測考生：完成個人資料修改 profile()
---

## v1.5 (2017-10-30)
* dbinit.py 增加單字批次新增程式
* 測驗中心：完成單字建檔查詢 create_words()
* 測驗中心：完成參測考生列表 examinees()
* 參測考生：完成登入/註冊 login_or_enroll()
---

## v1.4 (2017-10-30)
* 新增 adb.py (資料庫類別程式模組 DB)
* 測驗中心/參測考生：均使用 DB 類別產生物件
---

## v1.3 (2017-10-30)
* 新增 dbinit.py > toeic.db (資料庫初始化程式)
* 新增 dblist.py (資料庫查詢列表程式)
* 定義查詢列表函式 show_all_rows()
---

## v1.2 (2017-10-30)
* 新增 words_in.txt > cleanup.py > words_out.txt
---

## v1.1 (2017-10-30)
* 測驗中心/參測考生：依選單定義各功能函式
* 設定 menu_func 以依選單代碼執行對應函式
---

## v1.0 (2017-10-30)
* 新增 aexaminee.py
* 新增 atestcenter.py
* 測驗中心/參測考生：設定選單項目
* 測驗中心/參測考生：定義選單函式 show_menu()