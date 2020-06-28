from random import sample
from flask import *
import pickle

app = Flask(__name__)

def pattern(r,c,base,side):
   return (base*(r%base)+r//base+c)%side
def shuffle(s):
   return sample(s, len(s))
@app.route('/')
def login():
   return render_template('Login.html')
@app.route('/tabel',methods=['POST','GET'])
def giriweb():
   if request.method=='POST':
      global bd
      base = 3
      side = base * base
      rBase = range(base)
      rows = rs = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
      cols = cs = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
      nums = shuffle(range(1, base * base + 1))
      board = [[nums[pattern(r, c,base,side)] for c in cols] for r in rows]
      global bc
      bc = [[nums[pattern(r, c,base,side)] for c in cs] for r in rs]
      squares = side * side
      empties = squares * 2 // 4
      for p in sample(range(squares), empties):
         board[p // side][p % side] = 0
      bd=board
      return render_template("tabel.html",board=board)

@app.route('/forpass')
def forpass():
   return render_template('forpass.html')

@app.route('/createacc')
def createacc():
   return render_template('createacc.html')
@app.route('/error',methods=['POST','GET'])
def error():
   if request.method=='POST':
      res=request.form
      d=list(res.keys())
      a=list(res.values())
      f = open('userdet.txt', 'rb')
      v = pickle.load(f)
      f.close()
      print(d,a,v)
      if d[0]=='name' and d[1]=='password':
         if a[0] in v.keys() and v[a[0]][0]==a[1]:
            global j
            j=a[0]
            return giriweb()
         else:
            return render_template('error.html')
      if d[0] == 'name' and d[1] == 'seccode':
         if a[0] in v.keys() and v[a[0]][1] == a[1]:
            return giriweb()
         else:
            return render_template('error.html')

@app.route('/reg',methods=['POST','GET'])
def reg():
   if request.method=='POST':
      res=request.form
      l=list(res.values())
      f = open('userdet.txt', 'rb')
      d=pickle.load(f)
      f.close()
      if l[0] not in d.keys():
         d[l[0]]=[l[1],l[2],0]
         f=open('userdet.txt', 'wb')
         pickle.dump(d,f)
         f.close()
         global j
         j = l[0]
         return giriweb()
      else:
         return render_template('error.html')


@app.route('/result',methods=['POST','GET'])
def result():
   if request.method == 'POST':
      res=request.form
      for i,j in res.items():
         if j!='':
            bd[int(i[0])][int(i[1])]=int(j)
      if bd==bc:
         result="Congrates you Won the game"
         f=open('userdet.txt','rb')
         l=pickle.load(f)
         f.close()
         f=open('userdet.txt','wb')
         l[j][2]+=1
         pickle.dump(l,f)
      else:
         result="Sorry you lost the game but you can win the game just try again.Don't lose your hope"
      return render_template('result.html',result=result)
if __name__ == '__main__':
   app.run(debug = True)
