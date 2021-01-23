# adb.py
class DB():
    def __init__(self):
        self.conn = None
        self.cur = None
        self.title_side = '-'*12

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def open(self):
        """ 開啟資料庫連線
        """
        if self.conn is None:
            import sqlite3
            self.conn = sqlite3.connect('toeic.db')
            self.cur = self.conn.cursor()
        return True

    def close(self):
        """ 關閉資料庫連線
        """
        if self.conn is not None:
            self.conn.close()
            self.conn = None
        return True

    def count_words(self):
        """ 計算單字數
        """
        self.cur.execute("SELECT COUNT(*) FROM WORDS")
        return self.cur.fetchone()[0]

    def get_max_id(self, arg_table):
        """ 取得資料最新編號
        """
        self.cur.execute("SELECT MAX(ID) FROM {}".format(arg_table))
        return self.cur.fetchone()[0] + 1

    def list_all_words(self):
        """ 單字列表
        """
        self.cur.execute("SELECT * FROM WORDS")
        all_rows = self.cur.fetchall()
        for row in all_rows:
            print('{:3} {:20} {}'.format(*row))
        print()

    def generate_dict_words(self):
        """ 設定單字字典
        """
        self.cur.execute("SELECT WORD, DEFINITIONS FROM WORDS")
        all_words = self.cur.fetchall()
        list_words = [dict(WORD=row[0], DEFS=row[1]) for row in all_words]
        return list_words

    def insert_or_update_word(self, arg_word, arg_def):
        """ 增修單字
        """
        words_max_id = self.get_max_id('WORDS')
        self.cur.execute("SELECT COUNT(*) FROM WORDS WHERE WORD=?", (arg_word,))
        count_result = self.cur.fetchone()[0]
        if count_result == 0:
            self.cur.execute("INSERT INTO WORDS VALUES (?, ?, ?)", 
                (words_max_id, arg_word, arg_def))
        elif count_result > 0:
            self.cur.execute("UPDATE WORDS SET DEFINITIONS=? WHERE WORD=?", (arg_def, arg_word))
        return self.conn.commit()

    def check_word_out(self, arg_word):
        """ 查詢單字
        """
        self.cur.execute("SELECT * FROM WORDS WHERE WORD=?", (arg_word,))
        result = self.cur.fetchone()
        if result:
            print('編號: {}  單字: {}  定義: {}\n'.format(*result))
        else:
            print('查無此字\n')

    def delete_word(self, arg_word):
        """ 刪除單字
        """         
        self.cur.execute("DELETE FROM WORDS WHERE WORD=?", (arg_word,))
        return self.conn.commit()

    def get_settings(self, arg_type, arg_opt):
        """ 擷取題型設定
        """
        self.cur.execute("SELECT OPTION, NUM_OF_QUESTIONS FROM SETTINGS WHERE TYPE=?", (arg_type,))
        settings = self.cur.fetchone()
        print('設定選項:%s 題數:%s' % settings)
        if arg_opt == 'read':
            return settings

    def update_settings(self, arg_type, arg_qnum, arg_opt):
        """ 更新題型設定
        """
        self.cur.execute("UPDATE SETTINGS SET NUM_OF_QUESTIONS=?, OPTION=? WHERE TYPE=?", 
            (arg_qnum, arg_opt, arg_type))
        return self.conn.commit()

    def list_all_examinees(self):
        """ 考生列表
        """
        self.cur.execute("SELECT * FROM EXAMINEES")
        all_rows = self.cur.fetchall()
        print('{:3} {:8} {:18} {:4} {:6}'.format('ID', '帳號', '姓名', '性別', '出生年'))
        print('-'*50)
        for row in all_rows:
            print('{:3} {:10} {:20} {:<4} {:6}'.format(*row))
        print()

    def check_if_examinee_existed(self, arg_account):
        """ 檢查考生是否註冊
        """
        self.cur.execute("SELECT COUNT(*) FROM EXAMINEES WHERE ACCOUNT=?", (arg_account,))
        if self.cur.fetchone()[0] == 1:
            return True
        else:
            return False

    def insert_or_update_examinee(self, account_id, action):
        """ 增修考生
        """
        data_ok = True
        full_name = input('姓名: ')
        if full_name == 'q':
            return False

        gender = input('性別(F.女性 M.男性): ').upper()
        if gender not in ('F', 'M'):
            data_ok = False

        birth_year = input('出生年: ')
        if birth_year.isdigit():
            birth_year = int(birth_year)
            if birth_year not in range(1950, 2007):
                data_ok = False
        else:
            data_ok = False

        # 資料無誤，准許註冊
        if data_ok:
            if action == 'insert':
                examinees_max_id = self.get_max_id('EXAMINEES')
                self.cur.execute("INSERT INTO EXAMINEES VALUES (?, ?, ?, ?, ?)", 
                    (examinees_max_id, account_id, full_name, gender, birth_year))
            elif action == 'update':
                self.cur.execute("UPDATE EXAMINEES SET NAME=?, GENDER=?, BIRTH_YEAR=? WHERE ACCOUNT=?", 
                    (full_name, gender, birth_year, account_id))
            self.conn.commit()
            return True
        else:
            return False
                        
    def print_examinee_info(self, account):
        """ 查詢考生資訊
        """
        self.cur.execute("SELECT * FROM EXAMINEES WHERE ACCOUNT=?", (account,))
        examinee = self.cur.fetchone()
        print('編號: {}  帳號: {}\n姓名: {}\n性別: {}\n出生年: {}'.format(*examinee))

    def insert_score(self, account, ex_type, ex_score):
        """ 增修單字
        """
        scores_max_id = self.get_max_id('SCORES')
        self.cur.execute("INSERT INTO SCORES VALUES (?, ?, ?, ?, date('now'))", 
            (scores_max_id, account, ex_type, ex_score))
        return self.conn.commit()

    def sql_case_type(self):
        return '''CASE TYPE WHEN 'multiple_choice' THEN '選擇題' 
                            WHEN 'fill_in_the_blank' THEN '填空題' END TYPE'''
    
    def show_one_score(self, row):
        print('{:3} {:10} {:3} {:4} {:10}'.format(*row))

    def list_scores_by_account(self, account):
        """ 個人成績查詢
        """
        case_type = self.sql_case_type()
        account_like = ''.join(('%', account, '%'))

        self.cur.execute('''SELECT ID, ACCOUNT, {}, SCORE, DATE_TIME FROM SCORES 
            WHERE ACCOUNT LIKE ? ORDER BY DATE_TIME DESC'''.format(case_type), (account_like,))
        all_rows = self.cur.fetchall()
        if len(all_rows):
            for row in all_rows:
                self.show_one_score(row)
        else:
            print(account, '查無任何成績')

    def score_summary(self):
        """ 測驗成績統計
        """
        case_type = self.sql_case_type()

        print(self.title_side, '測驗人數及平均分數', self.title_side)
        sql = "SELECT {}, COUNT(*), AVG(SCORE) FROM SCORES GROUP BY TYPE"
        self.cur.execute(sql.format(case_type))
        all_rows = self.cur.fetchall()
        if len(all_rows):
            for row in all_rows:
                print('{:3} {:4} {:6}'.format(*row))
        print(self.title_side, '成績列表依日期降冪', self.title_side)
        sql = "SELECT ID, ACCOUNT, {}, SCORE, DATE_TIME FROM SCORES ORDER BY DATE_TIME DESC"
        self.cur.execute(sql.format(case_type))
        all_rows = self.cur.fetchall()
        if len(all_rows):
            for row in all_rows:
                self.show_one_score(row)

if __name__ == '__main__':
    print('This is the DB class.')