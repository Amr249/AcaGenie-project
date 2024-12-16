css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 15%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://static.vecteezy.com/system/resources/previews/035/977/687/large_2x/ai-generated-portrait-of-a-senior-male-teacher-standing-in-front-of-a-blackboard-a-distinguished-professor-in-front-of-a-classic-blackboard-ai-generated-free-photo.jpg" >
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://www.tenforums.com/attachments/user-accounts-family-safety/322690d1615743307-user-account-image-log-user.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''