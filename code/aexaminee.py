# aexaminee.py
from adb import DB

class Examinee():
    def __init__(self):
        self.menu_title = '參測考生'
        self.account = ''
        self.menu = {
            'a':'登入．註冊',
            'b':'選擇題測驗',
            'c':'填充題測驗',
            'd':'個人成績查詢',
            'e':'個人資料修改',
            'f':'亂數播放單字',
            'q':'離開',
        }
        self.menu_func = {
            'a': lambda db, ft: self.login_or_signup(db, ft),
            'b': lambda db, ft: self.test_multiple_choice(db, ft),
            'c': lambda db, ft: self.test_fill_in_the_blank(db, ft),
            'd': lambda db, ft: self.score_list(db, ft),
            'e': lambda db, ft: self.profile(db, ft),
            'f': lambda db, ft: self.show_words_randomly(db, ft),
        }
        self.divider = '='*20

    def show_menu(self, account=''):
        """ 主選單
        """
        print(self.divider)
        if self.account == '':
            print(self.menu_title, '尚未登入')
        else:
            print(self.menu_title, self.account)
        print(self.divider)
        for fid, fname in self.menu.items():
            print('%s:%s' % (fid, fname))
        print(self.divider)
        opt = input('請選擇: ').lower()
        if opt in self.menu.keys():
            return opt, self.menu[opt]
        else:
            return '', '無此功能！'

    def login_or_signup(self, db, func_title):
        """ 登入．註冊
        """
        account_input = input('請輸入帳號: ')
        if db.check_if_examinee_existed(account_input):
            self.account = account_input
            db.print_examinee_info(self.account)
        else:
            if db.insert_or_update_examinee(account_input, 'insert'):
                print('註冊成功，可立即參加測驗')

    def test_multiple_choice(self, db, func_title):
        """ 選擇題測驗
        """
        from random import choice, randint
        set_type = 'multiple_choice'
        qtype, qnums = db.get_settings(set_type, 'read')
        list_all_words = db.generate_dict_words()
        list_questions = []
        # 設定題目及答案
        for i in range(qnums):
            qitem = choice(list_all_words)
            if qitem not in list_questions:
                list_questions.append(qitem)
        # print(list_questions)

        # 出卷
        right_count = 0
        for qindex, qitem in enumerate(list_questions):
            # 出題
            print('第 %s 題: %s' % (qindex+1, qitem['WORD']))
            qitem_ans = randint(1, qtype)
            for i in range(1, qtype+1):
                if i == qitem_ans:
                    print('%s. %s' % (i, qitem['DEFS']))
                else:
                    while True:
                        qitem_other = choice(list_all_words)
                        if qitem_other != qitem:
                            print('%s. %s' % (i, qitem_other['DEFS']))
                            break
            # 答題
            ex_choice = input('請選答 (exit.中止): ')
            if ex_choice == 'exit':
                return func_title
            elif ex_choice == str(qitem_ans):
                right_count += 1
            print('>'*3)

        # 計算答對題數及分數
        score = round(right_count/qnums*100)
        print('答對題數 %s/%s 分數 %s' % (right_count, qnums, score))
        db.insert_score(self.account, set_type, score)
        return func_title

    def test_fill_in_the_blank(self, db, func_title):
        """ 填充題測驗 
        """
        from random import choice
        set_type = 'fill_in_the_blank'
        qtype, qnums = db.get_settings(set_type, 'read')
        list_all_words = db.generate_dict_words()
        list_questions = []
        # 設定題目及答案
        for i in range(qnums):
            qitem = choice(list_all_words)
            if qitem not in list_questions:
                list_questions.append(qitem)
        # print(list_questions)

        # 出卷
        right_count = 0
        for qindex, qitem in enumerate(list_questions):
            # 出題
            qitem_ans = qitem['WORD']
            if qtype == 1:
                qword = qitem_ans[0] + '-'*(len(qitem_ans)-qtype)
            elif qtype == 2:
                qword = qitem_ans[0] + '-'*(len(qitem_ans)-qtype) + qitem_ans[-1]
            print('第 %s 題: %s (%s)' % (qindex+1, qword, qitem['DEFS']))
            
            # 答題
            ex_input = input('請選答 (exit.中止): ')
            if ex_input == 'exit':
                return func_title
            elif ex_input == qitem_ans:
                right_count += 1
            print('正確為:', qitem_ans)
            print('>'*3)

        # 計算答對題數及分數
        score = round(right_count/qnums*100)
        print('答對題數 %s/%s 分數 %s' % (right_count, qnums, score))
        db.insert_score(self.account, set_type, score)
        return func_title

    def score_list(self, db, func_title):
        """ 個人成績查詢 
        """
        db.list_scores_by_account(self.account)
        return func_title

    def profile(self, db, func_title):
        """ 個人資料修改
        """
        if db.insert_or_update_examinee(self.account, 'update'):
            print('--- 資料已更新 ---')
            db.print_examinee_info(self.account)
        else:
            print('--- 資料未更新 ---')
        return func_title

    def show_words_randomly(self, db, func_title):
        """ 亂數播放單字
        """
        import time
        from random import choice
        word_num = input('請輸入單字數量 (10~30): ')
        sleep_sec = input('請輸入停頓秒數 (0~5): ')
        if word_num.isdigit() and sleep_sec.isdigit():
            word_num = int(word_num)
            sleep_sec = int(sleep_sec)
            if sleep_sec not in range(6):
                sleep_sec = 0

            if word_num in range(10, 31):
                list_all_words = db.generate_dict_words()
                for i in range(word_num):
                    w = choice(list_all_words)
                    # 停頓
                    if sleep_sec > 0:
                        time.sleep(sleep_sec)
                    print(w['WORD'], ':', w['DEFS'])
            else:
                print('範圍錯誤')
        else:
            print('輸入錯誤')
        return func_title

# entry point
with DB() as db:
    aexaminee = Examinee()
    while True:
        func_id, func_name = aexaminee.show_menu()
        if func_id == 'q':
            break
        elif func_id == '':
            print(func_name)
        else:
            if aexaminee.account == '':
                func_id = 'a'
                print('請先登入或註冊')
            aexaminee.menu_func[func_id](db, func_name)
        print()