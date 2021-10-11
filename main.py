import time
import random
import threading
N = 5 
TIEMPO_TOTAL = 3
class filosofo(threading.Thread):
    semaforo = threading.Lock() 
    estado = [] 
    tenedores = [] 
    count=0
    def __init__(self):
        super().__init__()     
        self.id=filosofo.count 
        filosofo.count+=1 
        filosofo.estado.append('pensando') 
        filosofo.tenedores.append(threading.Semaphore(0)) 
        print("FILOSOFO ({0}) pensando".format(self.id))
    
    def __del__(self):
        print("FILOSOFO ({0}) Se levanta de la mesa".format(self.id))  
    
    def pensar(self):
        time.sleep(random.randint(0,5)) #CADA 
    
    def derecha(self,i):
        return (i-1)%N 
    
    def izquierda(self,i):
        return(i+1)%N 
    
    def verificar(self,i):
        if filosofo.estado[i] == 'hambriento' and filosofo.estado[self.izquierda(i)] != 'comiendo   ' and filosofo.estado[self.derecha(i)] != 'comiendo  ':
            filosofo.estado[i]='comiendo   '
            filosofo.tenedores[i].release()  
    
    def tomar(self):
        filosofo.semaforo.acquire() 
        filosofo.estado[self.id] = 'hambriento'
        self.verificar(self.id) 
        filosofo.semaforo.release() 
        filosofo.tenedores[self.id].acquire() 
    
    def soltar(self):
        filosofo.semaforo.acquire() 
        filosofo.estado[self.id] = 'pensando'
        self.verificar(self.izquierda(self.id))
        self.verificar(self.derecha(self.id))
        filosofo.semaforo.release() 
    
    def comer(self):
        print("FILOSOFO ({}) comiendo   ".format(self.id))
        time.sleep(2) 
        print("FILOSOFO ({}) terminó de comer".format(self.id))
    
    def run(self):
        for i in range(TIEMPO_TOTAL):
            self.pensar() 
            self.tomar() 
            self.comer() 
            self.soltar() 

def main():
    lista=[]
    for i in range(N):
        lista.append(filosofo()) 

    for f in lista:
        f.start() 

    for f in lista:
        f.join() 

if __name__=="__main__":
    main()