from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,LocationSendMessage
)
class Msg_Paser:
    def __init__(self):
        self.event=[]
        self.location=LocationSendMessage(
        title='我的位置',
        address='806高雄市前鎮區瑞政街56號',
        latitude=22.598579999999998,
        longitude=120.324364
        )
        self.msg_dict={
        '級職':'二兵',
        '姓名':'吳仰航',
        '體溫':'35.5',
        '1.時間':'19:00',
        '2.交通方式':'機車',
        '3.地點':'家',
        '4.密切接觸者':'家人'
        }
    def msg_parse(self,msg):
        if 'add' in msg:
            self.add_event(msg)
        elif 'query' in msg:
            self.query_event(msg)
        elif 'delet' in msg:
            self.delet_event(msg)
    def delet_event(self):

    def query_event(self):
        return self.event

    def add_event(self,event):
        try:
            self.event.append(event)
            return 'Sucess'
        except:
            return 'Fail'
    def get_event(self):
        return
