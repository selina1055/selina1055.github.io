# atestcenter.py
from adb import DB

class TestCenter():
    def __init__(self):
        self.menu_title = '測驗中心'
        self.menu = {
            'a':'單字建檔查詢',
            'b':'選擇題型設定',
            'c':'填充題型設定',
            'd':'參測考生列表',
            'e':'測驗成績統計',
            'f':'個人成績查詢',
            'q':'離開',
        }
        self.menu_func = {
            'a': lambda db, ft: self.create_words(db, ft),
            'b': lambda db, ft: self.set_multiple_choice(db, ft),
            'c': lambda db, ft: self.set_fill_in_the_blank(db, ft),
            'd': lambda db, ft: self.examinees(db, ft),
            'e': lambda db, ft: self.summary(db, ft),
            'f': lambda db, ft: self.score_list(db, ft),
        }
        self.divider = '='*20

    def show_menu(self):
        """ 主選單
        """
        print(self.divider)
        print(self.menu_title)
        print(self.divider)
        for fid, fname in self.menu.items():
            print('%s:%s' % (fid, fname))
        print(self.divider)
        opt = input('請選擇: ').lower()
        if opt in self.menu.keys():
            return opt, self.menu[opt]
        else:
            return '', '無此功能！'

    def create_words(self, db, func_title):
        """ 單字建檔查詢
        """
        while True:
            subopt = input('1.增修 2.查詢 3.刪除 4.列表 exit.離開: ')
            if subopt == 'exit':
                break
            else:
                print('單字數:', db.count_words())

                if subopt == '4':
                    db.list_all_words()
                    continue
                
                if subopt in ('1', '2', '3'):
                    in_word = input('單字: ')

                if subopt == '1':
                    in_def = input('定義: ')
                    db.insert_or_update_word(in_word, in_def)
                    db.check_word_out(in_word)
                elif subopt == '2':
                    db.check_word_out(in_word)
                elif subopt == '3':
                    db.delete_word(in_word)
                else:
                    db.check_word_out(subopt)
        return func_title

    def set_multiple_choice(self, db, func_title):
        """ 選擇題型設定
        """
        set_type = 'multiple_choice'
        while True:
            db.get_settings(set_type, 'show')
            subopt = input('3.三選一 4.四選一 5.五選一 exit.離開: ')
            if subopt == 'exit':
                break
            else:
                qnum = input('請輸入題數: ')
                if qnum.isdigit() and subopt in('3', '4', '5'):
                    db.update_settings(set_type, int(qnum), int(subopt))
                else:
                    print('設定錯誤')            
        return func_title

    def set_fill_in_the_blank(self, db, func_title):
        """ 填充題型設定
        """
        set_type = 'fill_in_the_blank'
        while True:
            db.get_settings(set_type, 'show')
            subopt = input('1.提示首字母 2.提示首尾字母 exit.離開: ')
            if subopt == 'exit':
                break
            else:
                qnum = input('請輸入題數: ')
                if qnum.isdigit() and subopt in('1', '2'):
                    db.update_settings(set_type, int(qnum), int(subopt))
                else:
                    print('設定錯誤')   
        return func_title

    def examinees(self, db, func_title):
        """ 參測考生列表
        """
        db.list_all_examinees()
        return func_title

    def summary(self, db, func_title):
        """ 測驗成績統計
        """
        db.score_summary()
        return func_title

    def score_list(self, db, func_title):
        """ 個人成績查詢
        """
        while True:
            qaccount = input('請輸入帳號 (exit.離開): ')
            if qaccount == 'exit':
                break
            db.list_scores_by_account(qaccount)
        return func_title    

# entry point
with DB() as db:
    atestcenter = TestCenter()
    while True:
        func_id, func_name = atestcenter.show_menu()
        if func_id == 'q':
            break
        elif func_id == '':
            print(func_name)
        else:
            atestcenter.menu_func[func_id](db, func_name)
        print()