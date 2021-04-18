from app import db, ma
from model import *
import flask
import io
import base64, json
class Conver(db.Model):
    __table_args__ = {'extend_existing': True}
    conversation_id = db.Column(db.Integer, primary_key=True)
    intent = db.Column(db.String(50))
    hero = db.Column(db.String(50))
    skill = db.Column(db.String(50))
    action = db.Column(db.String(50))
    def __repr__(self):
        return '<Conver {}>'.format(self.intent)
class Message(db.Model):
    __table_args__ = {'extend_existing': True}
    # id = db.Column(db.Integer, primary_key=True)
    hero = db.Column(db.String(50), primary_key=True)
    build_item = db.Column(db.String(100))
    support_socket = db.Column(db.LargeBinary)
    counter = db.Column(db.String(100))
    be_countered = db.Column(db.String(100))
    skill_up = db.Column(db.LargeBinary)
    how_to_play = db.Column(db.String(1000))
    combo = db.Column(db.String(500))
    combine_with = db.Column(db.String(100))
    how_to_use_skill = db.Column(db.String(1000))
    introduce = db.Column(db.String(1000))
    def __repr__(self):
        return '<Message {}>'.format(self.hero)     
class ConverSchema(ma.Schema):
    class Meta:
        fields = ("conversation_id", "intent", "hero", "skill", "action")
        model = Conver        
# Message.__table__.drop(db)
def get_action(intent, acc, hero, skill, pre_conv):
    if acc < 0.9 or intent == 'fall_back':
        return "action_ask_intent"
    if hero == '' and intent == "how_to_use_skill" and skill == "":
        return "action_ask_hero_and_skill"
    if hero == '':  
        return "action_ask_hero"
    if intent == "how_to_use_skill" and skill == "":
        return "action_ask_skill"
    if get_data(Message.query.get(hero), intent, hero, skill) == "no_answer":
        return "action_no_answer"
    return "action_"+intent
def get_message(action, intent, hero, skill):
    if action == "action_ask_intent":
        return "Mình chưa rõ câu hỏi của bạn lắm, bạn hãy cung cấp câu hỏi rõ ràng hơn để mình hỗ trợ nhé!"
    if action == "action_ask_hero":
        return "Bạn muốn mình hỗ trợ về tướng nào nhỉ?"
    if action == "action_ask_skill":
        return "Bạn muốn hỏi về skill nào nhỉ?"
    if action == "action_ask_hero_and_skill":
        return "Bạn muốn hỏi tướng nào và skill gì nhỉ?"
    if action == "action_no_answer":
        return "Rất xin lỗi bạn hiện mình chưa có thông tin cho câu hỏi này. Mình sẽ báo anh chủ cập nhật sớm nhất có thể ạ!"
    return get_data(Message.query.get(hero), intent, hero, skill)
    

def get_data(query, intent, hero, Skill):
    
        try:
            hero = hero.capitalize()
            skill = Skill.capitalize()
            # print (intent, hero, skill)
            if intent == 'build_item':
                item = query.build_item
                if item == '':
                    return 'no_answer'
                return "Bạn cứ lên đồ như này là auto win nhé:<br>"+item
            if intent == 'support_socket':
                return query.support_socket
            if intent == 'counter':
                count = query.counter
                if count == '':
                    return 'no_answer'
                return "{} đè được mấy con này nè:<br>".format(hero)+count
            if intent == 'be_countered':
                count = query.be_countered
                if count == '':
                    return 'no_answer'
                return "{} bị mấy con này khắc chế lại nè:<br>".format(hero)+count
            if intent == 'skill_up':
                return query.skill_up
            if intent == 'how_to_play':
                how = query.how_to_play
                if how == '':
                    return 'no_answer'
                return "Chơi {} như này là auto win nhé:<br>".format(hero)+how
            if intent == 'combo':
                com = query.combo
                if com == '':
                    return 'no_answer'
                return "Combo {} như này là nhiều dame nhất nè:<br>".format(hero)+com
            if intent == 'combine_with':
                combine = query.combine_with
                if combine == '':
                    return 'no_answer'
                return "Cầm {} đi cùng mấy con này thì max ping bạn ơi:<br>".format(hero)+combine
            if intent == 'how_to_use_skill':
                how = query.how_to_use_skill
                how = eval(how)
                how = how[Skill]
                if how == '':
                    return 'no_answer'
                return "Đây là chi tiết {} con {} bạn nha:<br>".format(skill,hero)+how
            if intent == 'introduce':
                if query.introduce != '':
            	    return "Giới thiệu {}:<br>".format(hero)+query.introduce
                else:
                    return 'no_answer'
        except:
            return 'no_answer'
def process_request(args, model):
    id = args['conversation_id']
    message = args['message']
    pre_conv  = Conver.query.get(id)
    intent, acc, hero, skill = process_data(model, message)
    print (intent, acc, hero, skill)
    if acc < 0.9:
        pre_action = pre_conv.action
        if pre_action == 'action_ask_hero' or pre_action == 'action_ask_skill' or pre_action == 'action_ask_hero_and_skill':
            intent = pre_conv.intent
            acc = 1.0
        if hero != '' and pre_conv.intent != '':
            intent = pre_conv.intent
            acc = 1.0
    if hero == '':
        hero = pre_conv.hero
    if skill == '':
        skill = pre_conv.skill
    action = get_action(intent, acc, hero, skill, pre_conv)
   
    mess_response = get_message(action, intent, hero, skill)
    print (mess_response)
    if isinstance(mess_response, str) == False:
        mess_response = base64.encodebytes(mess_response).decode('ascii')
        print (mess_response)
    if acc < 0.8: intent = 'fall_back'
    
    pre_conv.intent = intent
    pre_conv.hero = hero
    pre_conv.skill = skill
    pre_conv.action = action
    db.session.commit()

    return {'intent':intent, 'action': action, 'message':mess_response}
    
        
