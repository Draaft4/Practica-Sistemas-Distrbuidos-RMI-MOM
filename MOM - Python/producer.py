import pika
import time
from threading import Thread
from tkinter import *

def receiver():

    def llamada(ch, method, propreties, body):
        msg_list.insert(END, "persona2:   "+ body.decode())
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue1')

    if (channel.basic_consume(queue='task_queue1', on_message_callback= llamada, auto_ack=True)):
        msg_list.insert(END,"iniciando... ")
        time.sleep(2)
        msg_list.delete(0,END)

    channel.start_consuming()
    connection.close()

def send():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue2')

    live = entry_field.get()
    msg_list.insert(END, "yo:   " + live)
    
    channel.basic_publish(exchange='', routing_key='task_queue2', body= live)    
    connection.close()


janela = Tk()
janela.title("persona 1")
janela.geometry("350x275+700+100")
  
def salir():
    msg_list.delete(0,END)
    janela.destroy()
    
boton_salir = Button(janela, text = "Salir", command= salir )
boton_salir.pack(side = TOP, anchor = NE, pady = 5, padx = 5)


messages_frame = Frame(janela)       
scrollbar = Scrollbar(messages_frame) 
msg_list = Listbox(messages_frame, height=10, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side= RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messages_frame.pack()


boton_frame = Frame(janela)
lb = Label(boton_frame,text = "Escribir aqui: ")
lb.pack(side = LEFT, anchor= S, padx = 5)
entry_field = Entry(boton_frame, textvariable = '')
#entry_field.bind("<Return>", send)
entry_field.pack(side = LEFT, anchor = SE,pady=  5)


send_button = Button(boton_frame, text= "Enviar mensaje", command= send)
send_button.pack(side = LEFT, anchor = S, pady = 5, padx = 5)

boton_frame.pack()

receive_thread = Thread(target= receiver)
sender_thread = Thread(target= send)
receive_thread.start()
sender_thread.start()
janela.mainloop()