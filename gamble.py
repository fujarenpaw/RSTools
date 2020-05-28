import random
# 乱数がrate以下ならTrue より大きかったらFalseを返す
def probability(rate):
    if random.random() <= rate:
        return True
    else:
        return False

class Item:
    baseItemNumber = 0 # 必要なベースの数
    optionItemNumber = 0 # 必要なオプションの数
    blackBox = 0 # 必要な異次元ボックス
    mirror = 0 # 必要な鏡
    base = 0 # 1の時,狙ったベース
    op = [0, 0, 0] # 1の時、狙ったOP
    
    # 事前に計算したn回連続で30%を当てるのに必要な回数 10万回試行した平均を使用
    spendMirror = [0, 2.32, 13.47, 50.79]
    spendOption = [1, 2.32, 10.13, 23.27]
    
    def init(self):
        self.base = 0
        self.op = [0, 0, 0]
        
    def actMirror(self):
        self.mirror += 1
        
        if probability(0.3):
            return True
        else:
            return False
    
    def box(self, opNum):
        self.blackBox += 1
        if probability(0.5):
            self.base = 0
        else:
            self.base = 1
            
        for i in range(opNum):
            if probability(0.5):
                self.op[i] = True
            else:
                self.op[i] = False
                
    # 異次元用の素材を確保
    def offerItem(self, opNum):
        self.optionItemNumber += self.spendOption[opNum]
        self.mirror += self.spendMirror[opNum]
        self.baseItemNumber += 1
        
    # num = 素材のOPの数
    # targeOpNum = 目的のベースにつけたいopの数
    def calc(self, num, targetOpNum):
        skipflg = False
        while 1:
            self.init()
            # num個 OPがついたアイテムを生成
            if skipflg:
                skipflg = False
            else:
                self.offerItem(num - 1)
            
            self.box(num)
            # 異次元結果のベースが目的のベースの場合
            if self.base:
                # 3op乗った
                if sum(self.op) >= targetOpNum:
                    break
                # 0op
                elif sum(self.op) == 0:
                    # Uが残ったので、帳尻を合わせるために-1
                    self.baseItemNumber -= 1
                else:
                    flg = True
                    for i in range(targetOpNum - sum(self.op)):
                        if self.actMirror() == False:
                            flg = False
                            break
                    # 目的ベースのopが乗ったものに鏡をn回成功したら目的達成
                    if flg:
                        break
            # 素材ベースの時
            else:
                # 0op
                if sum(self.op) == 0:
                    pass
                elif sum(self.op) >= num:
                    skipflg = True
                    self.baseItemNumber += 1
                else:
                    flg = True
                    for i in range(num - sum(self.op)):
                        if self.actMirror() == False:
                            flg = False
                            break
                    if flg:
                        skipflg = True
                        self.baseItemNumber += 1
        return self.baseItemNumber, self.optionItemNumber, self.blackBox, self.mirror


# 価格 相場に合わせて
box = 6
mirror = 6
base = 40
op = 20

loopCnt = 10000
for i in range(1, 4):
    itemSum = 0
    opSum = 0
    boxSum = 0
    mirrorSum =0
    for j in range(loopCnt):
        item = Item()
        itemCnt, optionCnt, boxCnt, mirrorCnt = item.calc(i, 3)
        itemSum += itemCnt
        opSum += optionCnt
        boxSum += boxCnt
        mirrorSum += mirrorCnt
        
    print("%d OP異次元の場合:ベースの数=%f, OPの数=%f 異次元の数=%f, 鏡の数=%f"% (i, itemSum / loopCnt, opSum / loopCnt , boxSum / loopCnt, mirrorSum / loopCnt))
    print("総価格 = %f" % ((base * itemSum + op * opSum + box * boxSum + mirror * mirrorSum) / loopCnt))
    

            
        
        
            